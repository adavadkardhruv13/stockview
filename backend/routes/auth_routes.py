from fastapi import Depends, APIRouter, Response
from backend.models import User, Otp
from backend.database import users_collection, otp_collection
from backend.auth import hash_password, verify_password, create_jwt
from backend.utils.email_service import generate_otp, send_otp_email
import datetime
from fastapi.responses import JSONResponse



router = APIRouter()

@router.post("/register")
def register(user: User):
    if users_collection.find_one({"email": user.email}):
        return JSONResponse(status_code=400, content={'detail':"User already exists"})
    
    user_data = user.dict(exclude_unset=True)  # Avoid inserting extra metadata
    user_data["password"] = hash_password(user.password)
    user_data["created_at"] = datetime.datetime.utcnow()  # Add timestamp

    result = users_collection.insert_one(user_data)
    
    return JSONResponse(content={"message": "User registered successfully", "id": str(result.inserted_id)}, status_code=201)



@router.post("/login")
def login(email:str, password:str):
    user = users_collection.find_one({"email":email})
    
    if not user or not verify_password(password, user["password"]):
        return Response(status_code=400, details="Invalid credentials")
    
    token = create_jwt(email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/send-otp")
def send_otp(email: str):
    try:
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return Response(status_code=400, content={"detail": "User already exists"})
        
        otp = generate_otp()
        
        otp_collection.insert_one({
            "email": email,
            "otp": otp,
            "expire_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        })
        
        sent = send_otp_email(email, otp)
        if sent:
            return {"message": "OTP sent successfully"}
        else:
            return JSONResponse(status_code=500, content={"detail": "Failed to send OTP"})
    except Exception as e:
        print(f"ERROR in send-otp: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Internal server error: {str(e)}"})
    
    
@router.post("/verify-otp")
def verify_otp(request: Otp):
    otp_entry = otp_collection.find_one({"email": request.email})

    if not otp_entry:
        return JSONResponse(status_code=400, content={"detail": "Invalid OTP"})

    # # Debugging: Print stored document
    # print(f"Stored OTP Entry: {otp_entry}")

    # Ensure OTP is correctly compared
    if str(otp_entry.get("otp", "")) != str(request.otp):  # Use .get() to avoid KeyError
        return JSONResponse(status_code=400, content={"detail": "Invalid OTP"})

    # Handle missing expires_at
    expires_at = otp_entry.get("expire_at")  # Use .get() to avoid KeyError

    if not expires_at:
        return JSONResponse(status_code=400, content={"detail": "OTP does not have an expiry time"})


    if datetime.datetime.utcnow() > expires_at:
        return JSONResponse(status_code=400, content={"detail": "OTP expired"})

    otp_collection.delete_one({"email": request.email})
    return {"message": "OTP verified successfully"}
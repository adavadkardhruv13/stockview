import bcrypt, jwt, os, datetime
from fastapi import Depends
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import jwt.exceptions
from fastapi.responses import JSONResponse


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str)-> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password:str, hashed_password:str)-> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_jwt(email:str):
    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={'detail':"Token expired"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={'detail':"Invalid token"})
from fastapi import  APIRouter
import requests, os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()


@router.get("/")
def get_mf():
    try:
        url = "https://indian-stock-exchange-api2.p.rapidapi.com/mutual_funds"
        
        headers = {
            "x-rapidapi-key": os.getenv("x-rapidapi-key"),
	        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
        }
        
        responses=requests.get(url, headers=headers)
        return JSONResponse(responses.json())
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
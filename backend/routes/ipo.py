from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import requests, os, logging
from dotenv import load_dotenv
from datetime import date, timedelta
import yfinance as yf

router = APIRouter()
load_dotenv()
logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
today_date = date.today().strftime('%Y-%m-%d')
yesterday_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')


IPO_API_KEY = os.getenv("IPO_API_KEY") 

headers = {
    "Authorization": f"Bearer {IPO_API_KEY}"
}

@router.get("/ipo-open")
def get_ipo_details():
    try:
        response = requests.get("https://api.ipoalerts.in/ipos?status=open", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"detail":response.text})
    except ValueError as e:
        return JSONResponse(status_code=500, content={"detail":f"JSON decoding failed: {e}"})
    
@router.get("/ipo-closed")
def get_ipo_details_closed():
    try:
        response = requests.get("https://api.ipoalerts.in/ipos?status=closed", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"detail":response.text})
    except ValueError as e:
        return JSONResponse(status_code=500, content={"detail":f"JSON decoding failed: {e}"})
    
        
## similarly can add for upcoming ipos, listed ipos, etc 


## need to impement the stock market calendar

# trade_API_KEY = "65b235c30740468:3y8ywr3sgsqgfva"

# @router.get("/calendar")
# def get_calendar_update():
#     url = f'https://api.tradingeconomics.com/calendar/country/india?c={trade_API_KEY}'
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return JSONResponse(status_code=response.status_code, content={"detail":response.text})

# @router.get("/news")
# def news():
#     url = "https://livemint-api.p.rapidapi.com/news"

#     querystring = {"name":"news"}

#     headers = {
#         "x-rapidapi-key": "59e73d2989msh8aadda9651e459cp1cef8bjsn49d2fbb8ccbe",
#         "x-rapidapi-host": "livemint-api.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)

#     return JSONResponse(response.json())

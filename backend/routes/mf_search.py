from fastapi import  APIRouter, Query
import requests, os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()


@router.get("/")
def get_mf(fund_type: str = Query(all, description="Filter by fund type(Equity, Hybrid, Index, All)")):
    try:
        url = "https://indian-stock-exchange-api2.p.rapidapi.com/mutual_funds"
        
        headers = {
            "x-rapidapi-key": os.getenv("x-rapidapi-key"),
	        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
        }
        
        responses=requests.get(url, headers=headers)
        data = responses.json()
        
        if fund_type == 'Equity' and 'Equity' in data:
            return JSONResponse(data['Equity'])
        elif fund_type == 'Hybrid' and 'Hybrid' in data:
            return JSONResponse(data['Hybrid'])
        elif fund_type == 'Index' and 'Index Funds' in data:
            return JSONResponse(data['Index Funds'])
        elif fund_type == "All":
            return JSONResponse(data)
        else:
            return JSONResponse(status_code=404, content={"detail": f"Fund type '{fund_type}' not found."})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
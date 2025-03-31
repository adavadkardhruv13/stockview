from fastapi import  APIRouter, Query
import requests, os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()


@router.get("/")
def get_mf(fund_type: str = Query("All", description="Filter by fund type (Equity, Hybrid, Index, All)")):
    try:
        url = "https://stock.indianapi.in/mutual_funds"
        
        headers = {
            "X-Api-Key": os.getenv("X-Api-Key") ,
            # "x-rapidapi-host": "stock.indianapi.in"
        }
        
        responses = requests.get(url, headers=headers)

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

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"detail": f"Request error: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=500, content={"detail": f"Invalid JSON response: {str(e)}"})
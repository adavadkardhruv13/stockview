from fastapi import  APIRouter, Query
from pymongo import MongoClient
import requests, os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from backend.models import Mf


router = APIRouter()
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MONGO_URL = os.getenv("MONGO_URL_HOSTED")
client = MongoClient(MONGO_URL)
db = client["stockviewmain"]
mf_collection = db["mutual_funds"]


CACHE_EXPIRATION = 24

def map_api_fields_to_model(api_data: dict) -> dict:
    mapping = {
        '1_month_return': 'one_month_return',
        '3_month_return': 'three_month_return',
        '6_month_return': 'six_month_return',
        '1_year_return': 'one_year_return',
        '3_year_return': 'three_year_return',
        '5_year_return': 'five_year_return',
        'asset_size' : "asset_size"
    }
    mapped_data = {}
    for api_field, model_field in mapping.items():
        if api_field in api_data:
            mapped_data[model_field] = api_data[api_field]
    return mapped_data


@router.get("/")
def get_mf(fund_type: str = Query("Equity", description="Filter by fund type (Equity, Hybrid, Index Funds)")):
    try:
        
        cached_data = mf_collection.find_one({"fund_type": fund_type})

        if cached_data:
            last_updated = datetime.strptime(cached_data["last_updated"], "%Y-%m-%dT%H:%M:%S.%f")

            # If cache is still valid, return it
            if datetime.utcnow() - last_updated < timedelta(hours=CACHE_EXPIRATION):
                logging.info("Returning cached data from MongoDB")
                
                return JSONResponse(content=[
    {**Mf(**mf).dict(), "last_updated": mf["last_updated"].isoformat()} for mf in cached_data["data"]
])


        # Fetch fresh data from API
        url = "https://stock.indianapi.in/mutual_funds"
        api_key = os.getenv("X-Api-Key")
        headers = {"X-Api-Key": api_key}

        logging.info(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("Hitting the API")
        data = response.json()

        # Ensure requested fund_type exists in API response
        if fund_type != "All" and fund_type not in data:
            return JSONResponse(status_code=404, content={"detail": f"Fund category '{fund_type}' not found."})

        
        filtered_data = data if fund_type == "All" else data.get(fund_type, {})


        mf_objects = []
        
        if fund_type == "All":
            for category, funds in filtered_data.items(): 
                if isinstance(funds, list): 
                    for fund in funds:
                        try:
                            mapped_fund = {**fund, **map_api_fields_to_model(fund)}
                            mapped_fund["fund_type"] = category
                            mf_objects.append(Mf(**mapped_fund))
                        except TypeError as e:
                            logging.error(f"Error creating Mf object: {e}, fund: {fund}")
                            continue
                else:
                    logging.error(f"Error, funds is not a list: {funds}")
        else:
            if isinstance(filtered_data, list):
                for fund in filtered_data:
                    try:
                        fund["fund_type"] = fund_type 
                        mf_objects.append(Mf(**fund))
                    except TypeError as e:
                        logging.error(f"Error creating Mf object: {e}, fund: {fund}")
                        continue
            else:
                for funds in filtered_data.values():
                    if isinstance(funds, list):
                        for fund in funds:
                            try:
                                mapped_fund = {**fund, **map_api_fields_to_model(fund)}
                                mapped_fund["fund_type"] = fund_type
                                mf_objects.append(Mf(**mapped_fund))
                            except TypeError as e:
                                logging.error(f"Error creating Mf object: {e}, fund: {fund}")
                                continue
                    else:
                        logging.error(f"Error, funds is not a list: {funds}")

        
        mf_collection.update_one(
            {"fund_type": fund_type},
            {"$set": {"data": [mf.dict() for mf in mf_objects], "last_updated": datetime.utcnow().isoformat()}},
            upsert=True
        )

        logging.info(f"Updated cache for category: {fund_type}")

        
        if cached_data and "data" in cached_data and cached_data["data"]:
            mf_collection.update_one(
                {"fund_type": fund_type},
                {"$set": {
                    "data": [mf.dict() for mf in mf_objects], 
                    "last_updated": datetime.utcnow().isoformat() 
                }},
                upsert=True
            )
        else:
            logging.warning(f"No cached data found for fund type: {fund_type}")

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"detail": f"Request error: {str(e)}"})
    except ValueError as e:
        return JSONResponse(status_code=500, content={"detail": f"Invalid JSON response: {str(e)}"})

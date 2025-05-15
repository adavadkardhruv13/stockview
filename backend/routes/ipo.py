from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import requests, os, logging
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import yfinance as yf
from pymongo.errors import ConnectionFailure
from backend.models import Ipo
from typing import List
# from backend.utils.ipo_update import update_ipo_data



load_dotenv()
router = APIRouter()
logger = logging.getLogger(__name__)



MONGO_URL = os.getenv("MONGO_URL_HOSTED")
client = MongoClient(MONGO_URL)
logger.info("Connected to MongoDB Atlas")
db = client["stockviewmain"]
ipo_collection = db["ipos"]
    
    

# Cache Expiration Time (in hours)
CACHE_EXPIRATION = 24


def fetch_ipo_data():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/ipo"
    headers = {
        "x-rapidapi-key": os.getenv("IPO_RAPID_API_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    try:
        logging.info(f"Fetching IPO data from API: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Debug: Check API response
        # logging.info(f"IPO API Response: {data}")

        return data if data else {}  
    except requests.RequestException as e:
        logging.error(f"Failed to fetch IPO data: {str(e)}")
        return {}




# def serialize_dates(ipo_data):
#      """Convert date fields to ISO 8601 format if they exist."""
#      for key in ["bidding_start_date", "bidding_end_date", "listing_date", "last_updated"]:
#          if key in ipo_data and isinstance(ipo_data[key], (datetime, date)):
#              ipo_data[key] = ipo_data[key].isoformat()
#      return ipo_data



@router.get("/")
def get_ipos(category: str = Query("active", description="Filter by IPO category (e.g., active, upcoming, listed)")):
    try:
        # Retrieve cached data
        cached_data = ipo_collection.find_one({"category": category})

        if cached_data:
            last_updated = datetime.strptime(cached_data["last_updated"], "%Y-%m-%dT%H:%M:%S.%f")

            # If cache is valid, return it
            if datetime.utcnow() - last_updated < timedelta(hours=CACHE_EXPIRATION):
                logging.info(f"Returning cached IPO data for category: {category}")
                return JSONResponse(content={"category": category, "ipos": cached_data.get("data", [])})

        # Fetch fresh data from API
        data = fetch_ipo_data()


        if category not in data:
            logging.warning(f"Category '{category}' not found in API response. Returning empty list.")
            return JSONResponse(content={"category": category, "ipos": []})

        
        

        ipo_objects = []
        for ipo in data[category]:  
            token = os.getenv('LOGO_API')
            company_name = ipo.get("name")
            company_query = company_name.replace(" ", "").lower()
            logo_url = f"https://img.logo.dev/{company_query}.com?token={token}&retina=true"
            
            ipo_data = {
                "category": category,
                "symbol": ipo.get("symbol", "N/A"),
                "name": ipo.get("name", "N/A"),
                "status": ipo.get("status", "N/A"),
                "is_sme": ipo.get("is_sme", False),
                "additional_text": ipo.get("additional_text", ""),
                "min_price": ipo.get("min_price", 0),
                "max_price": ipo.get("max_price", 0),
                "issue_price": ipo.get("issue_price", 0),
                "listing_gains": ipo.get("listing_gains", 0),
                "listing_price": ipo.get("listing_price", 0),
                "bidding_start_date": ipo.get("bidding_start_date"),
                "bidding_end_date": ipo.get("bidding_end_date"),
                "listing_date": ipo.get("listing_date"),
                "lot_size": ipo.get("lot_size", 0),
                "document_url": ipo.get("document_url", ""),
                "logo_url": logo_url,
                "last_updated": datetime.utcnow().isoformat()
            }
            ipo_objects.append(ipo_data)

        
        ipo_collection.update_one(
            {"category": category},
            {"$set": {"data": ipo_objects, "last_updated": datetime.utcnow().isoformat()}},
            upsert=True
        )

        logging.info(f"Updated IPO cache for category: {category}")

        return JSONResponse(content={"category": category, "ipos": ipo_objects})

    except requests.exceptions.RequestException as e:
        logging.error(f"IPO API request failed: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Request error: {str(e)}"})

    except ValueError as e:
        logging.error(f"Invalid JSON response from IPO API: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Invalid JSON response: {str(e)}"})
        

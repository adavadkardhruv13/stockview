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
from backend.utils.ipo_update import update_ipo_data



load_dotenv()
router = APIRouter()
logger = logging.getLogger(__name__)



MONGO_URL = os.getenv("MONGO_URL_HOSTED")
client = MongoClient(MONGO_URL)
logger.info("Connected to MongoDB Atlas")
db = client["stockviewmain"]
ipo_collection = db["ipos"]
    
    
    

def fetch_ipo_data():
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/ipo"

    headers = {
        "x-rapidapi-key": os.getenv("IPO_RAPID_API_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        logger.info("API hit")
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        logger.error(f"Failed to fetch IPO data: {str(e)}")
        return {}

def serialize_dates(ipo_data):
    """Convert date fields to ISO 8601 format if they exist."""
    for key in ["bidding_start_date", "bidding_end_date", "listing_date", "last_updated"]:
        if key in ipo_data and isinstance(ipo_data[key], (datetime, date)):
            ipo_data[key] = ipo_data[key].isoformat()
    return ipo_data

@router.get("/{category}", response_model=List[Ipo])
async def get_ipos(category: str):
    valid_categories = ["upcoming", "listed", "active", "closed"]
    if category not in valid_categories:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid category. Choose from 'upcoming', 'listed', 'active', 'closed'."}
        )

    # Check last update time to determine if a refresh is needed
    last_updated_entry = ipo_collection.find_one({}, {"last_updated": 1, "_id": 0}, sort=[("last_updated", -1)])
    last_updated = last_updated_entry.get("last_updated") if last_updated_entry else None

    if not last_updated or (datetime.utcnow() - last_updated) > timedelta(days=2):
        logger.info("IPO data is outdated. Triggering update...")
        update_ipo_data()

    # Retrieve IPOs from database
    ipos = list(ipo_collection.find({'category': category}, {"_id": 0}))

    if ipos:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"category": category, "ipos": [serialize_dates(ipo) for ipo in ipos]}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"category": category, "ipos": []}  # No IPOs found for this category
    )
    
        

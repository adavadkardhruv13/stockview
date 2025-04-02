from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import requests, os, logging
from dotenv import load_dotenv
from datetime import datetime, date
import yfinance as yf
from pymongo.errors import ConnectionFailure
from backend.models import Ipo
from typing import List



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
    
    ipos = list(ipo_collection.find({'category': category}, {"_id": 0})) 

    if ipos:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"category": category, "ipos": [serialize_dates(ipo) for ipo in ipos]}
        )

    # Fetch only if the entire database is empty
    existing_ipo_count = ipo_collection.count_documents({})
    if existing_ipo_count == 0:
        logger.info("No IPO data in DB. Fetching from API...")
        data = fetch_ipo_data()
        new_ipos = []

        for category_name, category_data in data.items():
            for ipo in category_data:
                ipo_data = {
                    "category": category_name,
                    "symbol": ipo.get("symbol"),
                    "name": ipo.get("name"),
                    "status": ipo.get("status"),
                    "is_sme": ipo.get("is_sme"),
                    "additional_text": ipo.get("additional_text"),
                    "min_price": ipo.get("min_price"),
                    "max_price": ipo.get("max_price"),
                    "issue_price": ipo.get("issue_price"),
                    "listing_gains": ipo.get("listing_gains"),
                    "listing_price": ipo.get("listing_price"),
                    "bidding_start_date": ipo.get("bidding_start_date"),
                    "bidding_end_date": ipo.get("bidding_end_date"),
                    "listing_date": ipo.get("listing_date"),
                    "lot_size": ipo.get("lot_size"),
                    "document_url": ipo.get("document_url"),
                    "last_updated": datetime.utcnow(),
                }

                ipo_data = serialize_dates(ipo_data)
                
                ipo_collection.update_one(
                    {"symbol": ipo.get("symbol")},
                    {"$set": ipo_data},
                    upsert=True
                )

                new_ipos.append(Ipo(**ipo_data))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"category": category, "ipos": [serialize_dates(ipo.dict()) for ipo in new_ipos]}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"category": category, "ipos": []}  # No IPOs found for this category
    )
    
        

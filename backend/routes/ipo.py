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
print("🔗 MONGO_URL:", MONGO_URL)
try:
    client = MongoClient(MONGO_URL)
    client.admin.command('ping') #check connection.
    logger.info("Connected to MongoDB Atlas")
    db = client["stockviewmain"]
    ipo_collection = db["ipos"]
except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB Atlas: {e}")
    client = None #set client to None, so that the rest of the application knows that the connection failed.
except Exception as e:
    logger.error(f"An unexpected error occured when connecting to MongoDB: {e}")
    client = None

if client:
    # Your MongoDB operations here
    # example. ipo_collection.insert_one({"example": "test"})
    pass
else:
    logger.error("The rest of the program, that uses the database, will not be executed.")
    
    
    
    
    

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
    
    ipos = list(ipo_collection.find({'category': category}, {"_id": 0}))  # 🔥 Don't return `_id`

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

                ipo_data = serialize_dates(ipo_data)  # Convert date fields

                # 🔥 FIXED: Corrected update_one syntax
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


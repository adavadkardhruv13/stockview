from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
from pymongo import MongoClient
import requests, os, logging
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
import atexit



load_dotenv()
logger = logging.getLogger(__name__)

MONGO_URL = os.getenv("MONGO_URL_HOSTED")
# print("🔗 MONGO_URL:", MONGO_URL)


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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Failed: {e}")
        return None
    
def serialize_dates(ipo_data):
    """Convert date fields to ISO 8601 string format if they are datetime objects."""
    for key in ["bidding_start_date", "bidding_end_date", "listing_date", "last_updated"]:
        if isinstance(ipo_data.get(key), (datetime, date)):
            ipo_data[key] = ipo_data[key].isoformat()
    return ipo_data

def update_ipo_data():
    """Fetches and updates IPO data in MongoDB every 2 days."""
    data = fetch_ipo_data()
    if not data:
        logger.warning("No data fetched from IPO API.")
        return

    for category_name, category_data in data.items():
        for ipo in category_data:
            symbol = ipo.get("symbol")
            if not symbol:
                logger.warning("Skipping IPO entry with missing symbol.")
                continue  

            ipo_data = {
                "category": category_name,
                "symbol": symbol,
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
                "last_updated": datetime.utcnow()
            }

            ipo_data = serialize_dates(ipo_data)

            existing_data = ipo_collection.find_one({"symbol": symbol}, {"_id": 0})
            if existing_data and existing_data == ipo_data:
                logger.info(f"Skipping update for {symbol}, no changes detected.")
                continue  
            
            ipo_collection.update_one({"symbol": symbol}, {"$set": ipo_data}, upsert=True)
            logger.info(f"Updated IPO data for {symbol}")

# Schedule auto-update every 2 days
scheduler = BackgroundScheduler()
scheduler.add_job(update_ipo_data, "interval", days=2)
scheduler.start()

# Ensure graceful shutdown
atexit.register(lambda: scheduler.shutdown(wait=False))
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["stockviewmain"]
users_collection = db["users"]
otp_collection = db["otps"]
ipo_collection = db["ipos"]
mf_collection = db["mutual_funds"]
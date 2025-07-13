from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("TIL_MONGO_URL")

try:
    client = MongoClient(db_url)
except Exception as e:
    print("error", e)

db = client.TIL_db

collection_name = db["TIL_collection"]
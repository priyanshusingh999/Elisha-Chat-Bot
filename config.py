from flask import config
from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "")
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["elishachatbot"]
config = db["variables"].find_one() or {}

class Variables:
    BOT_TOKEN = os.getenv('BOT_TOKEN', "") or config.get('BOT_TOKEN', "")
    OWNER_ID = os.getenv('OWNER_ID', "") or config.get('OWNER_ID', "")
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', "") or config.get('GEMINI_API_KEY', "")
    
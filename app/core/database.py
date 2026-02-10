from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
from app.core.config import MONGO_URI, DATABASE_NAME

class MongoDB:
    client: Optional[MongoClient] = None
    db: Optional[Database] = None

mongodb = MongoDB()

def connect_to_mongo():
    if not MONGO_URI or not DATABASE_NAME:
        raise RuntimeError("MongoDB config missing")
    mongodb.client = MongoClient(MONGO_URI)
    mongodb.db = mongodb.client[DATABASE_NAME]
    print("MongoDB connected")

def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("MongoDB disconnected")
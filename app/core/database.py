from pymongo import MongoClient
from app.core.config import MONGO_URI, DATABASE_NAME

class MongoDB:
    client: MongoClient = None # type: ignore
    db = None

mongodb = MongoDB()

def connect_to_mongo():
    mongodb.client = MongoClient(MONGO_URI)
    mongodb.db = mongodb.client[DATABASE_NAME] # type: ignore
    print("MongoDB connected")

def close_mongo_connection():
    mongodb.client.close()
    print("MongoDB disconnected")
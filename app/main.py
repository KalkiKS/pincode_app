from fastapi import FastAPI
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes.pincode_routes import router as pincode_router

app = FastAPI(title="Pincode Management API")

@app.on_event("startup")
def start_db_client():
    connect_to_mongo()

@app.on_event("shutdown")
def shutdown_db_client():
    close_mongo_connection()

app.include_router(pincode_router)

@app.get("/")
def root():
    return {"message": "Pincode API is running"}
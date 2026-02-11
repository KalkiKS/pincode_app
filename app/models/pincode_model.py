from datetime import datetime
from app.core.database import mongodb


class PincodeModel:

    @staticmethod
    def collection():
        return mongodb.db["pincodes"] # type: ignore
    
    @staticmethod
    def create_pincode(data: dict):
        data["is_active"] = True
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return PincodeModel.collection().insert_one(data)
    

    @staticmethod
    def find_by_pincode(pincode: int):
        return PincodeModel.collection().find_one(
            {"pincode": pincode, "is_active": True},
            {"_id": 0}
        )
    
    @staticmethod
    def find_by_location(query: str):

        if not query:
            return {
                "success": False,
                "message": "Query cannot be empty"
            }
        
        mongo_query = {
            "$or": [
                {"district": query},
                {"state": query},
                {"post_offices.name": query}
            ]
        }

        result = list(PincodeModel.collection().find(mongo_query, {"_id": 0}))

        if not result:
            return {
                "success": False,
                "message": f"No data found for {query}"
            }
        
        if result:
            return {
                "success": True,
                "count": len(result),
                "data": result
            }
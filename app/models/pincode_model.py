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
    def find_by_state(query, skip, limit):

        pipelines = [
            {
                "$match": {
                    "state": query
                }
            },
            {
                "$group": {
                    "_id": "$district",
                    "pincodes": { "$addToSet": "$pincode" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "district": "$_id",
                    "pincodes": 1
                    
                }
            },
            {
                "$sort": {
                    "district": 1
                }
            },
            { "$skip": skip },
            { "$limit": limit }
        ]

        data = PincodeModel.collection().aggregate(pipelines)
        return list(data)
    
    @staticmethod
    def count_state_districts(query):
        pipeline = [
            {"$match": {"state": query}},
            {"$group": {"_id": "$district"}},
            {"$count": "total"}
        ]

        result = PincodeModel.collection().aggregate(pipeline)
        return result.next().get("total", 0) if result else 0

    @staticmethod
    def find_by_district(query: str, page: int, limit: int):
        pass

    @staticmethod
    def find_by_postoffice(query: str, page: int, limit: int):
        pass
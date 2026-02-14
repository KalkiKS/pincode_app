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


class LocationModel:
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

        result = list(PincodeModel.collection().aggregate(pipeline))
        return result[0]["total"] if result else 0



    @staticmethod
    def find_by_district(query, skip, limit):
        pipelines = [
            {
                "$match": {
                    "district": query
                }
            },
            {
                "$unwind": "$post_offices"
            },
            {
                "$group": {
                    "_id": "$pincode",
                    "post_offices": {
                        "$push": {
                            "name": "$post_offices.name",
                            "delivery": "$post_offices.delivery"
                        }
                    },
                    "post_offices_count": { "$sum": 1 }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "pincode": "$_id",
                    "post_offices_count": 1,
                    "post_offices": 1
                }
            },
            {
                "$sort": {
                    "pincode":1,
                }
            },
            { "$skip": skip },
            { "$limit": limit }
        ]

        data = PincodeModel.collection().aggregate(pipelines)
        return list(data)

    @staticmethod
    def count_district_pincodes(query):
        pipeline = [
            {"$match": {"district": query}},
            {"$group": {"_id": "$pincode"}},
            {"$count": "total"}
        ]

        result = list(PincodeModel.collection().aggregate(pipeline))
        return result[0]["total"] if result else 0

    @staticmethod
    def find_by_postoffice(query: str):

        query = query.upper().replace(" ", "")
        
        pipeline = [
            {
                "$unwind": "$post_offices"
            },
            {
                "$match": {
                    "post_offices.normalize_name": query
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "pincode": 1,
                    "district": 1,
                    "state": 1,
                    "country": 1,
                    "region": 1,
                    "division": 1,
                    "area": "$area",
                    "post_office": {
                        "name": "$post_offices.name",
                        "type": "$post_offices.type",
                        "delivery": "$post_offices.delivery",
                        "latitude": "$post_offices.latitude",
                        "longitude": "$post_offices.longitude"
                    }
                }
            }
        ]

        data = PincodeModel.collection().aggregate(pipeline)
        
        return list(data)
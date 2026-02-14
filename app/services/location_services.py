from app.models.validate_location import ValidateLocation
from app.models.pincode_model import PincodeModel
from fastapi import HTTPException, status


class LocationService:
    @staticmethod
    def get_state_details(query, page, limit):
        valid = ValidateLocation.validate_state(query)
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="State not found"
            )
        
        # Fetch and return state details from the database
        if page < 1:
            page = 1
        if limit > 50:
            limit = 50
        skip = (page - 1) * limit
        data = PincodeModel.find_by_state(query=query, skip=skip, limit=limit)

        total_district = PincodeModel.count_state_districts(query)

        total_pages = (total_district + limit - 1) // limit  # Calculate total pages
        return {
            "success": True,
            "page": page,
            "limit": limit,
            "total_districts": total_district,
            "total_pages": total_pages,
            "count": len(data),
            "data": data
        }

        
        # Example: return StateModel.find_by_name(query)


    @staticmethod
    def get_district_details(query: str, page: int, limit: int):
        if not ValidateLocation.validate_district(query):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="District not found"
            )
        
        # Fetch and return district details from the database
        skip = (page - 1) * limit
        # Example: return DistrictModel.find_by_name(query)


    @staticmethod
    def get_postoffice_details(query: str):
        if not ValidateLocation.validate_postoffice(query):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post office not found"
            )
        return {
            "postoffice": query,
            "details": "Post office details would be fetched from the database here."
        }
        # Fetch and return post office details from the database

        # Example: return PostOfficeModel.find_by_name(query)
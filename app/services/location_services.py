from app.models.validate_location import ValidateLocation
from app.models.pincode_model import LocationModel
from app.schemas.pincode_schema import StateBase, StateResponseSchema, DistrictBase, DistrictResponseSchema, PostOfficeDetailSchema, PostOfficeResponseSchema
from fastapi import HTTPException, status


class LocationService:
    @staticmethod
    def get_state_details(query, page, limit):

        query = query.upper().strip()

        if not ValidateLocation.validate_state(query):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="State not found"
            )
        
        skip = (page - 1) * limit
        data = LocationModel.find_by_state(query=query, skip=skip, limit=limit)

        district_objects = [StateBase(**item) for item in data]

        total_district = LocationModel.count_state_districts(query)
        total_pages = (total_district + limit - 1) // limit  # Calculate total pages

        return StateResponseSchema(
            success=True,
            page=page,
            limit=limit,
            total_districts=total_district,
            total_pages=total_pages,
            count=len(data),
            data=district_objects
            )

        # Example: return StateModel.find_by_name(query)


    @staticmethod
    def get_district_details(query: str, page: int, limit: int):

        query = query.upper().strip()

        if not ValidateLocation.validate_district(query):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="District not found"
            )
        
        skip = (page - 1) * limit

        data = LocationModel.find_by_district(query=query, skip=skip, limit=limit)

        district_objects = [DistrictBase(**item) for item in data]
        
        total_pincodes = LocationModel.count_district_pincodes(query)
        total_pages = (total_pincodes + limit - 1) // limit

        return DistrictResponseSchema(
            success=True,
            page=page,
            limit=limit,
            total_pincode=total_pincodes,
            total_pages=total_pages,
            count=len(data),
            data=district_objects
        )



    @staticmethod
    def get_postoffice_details(query: str):

        query = query.upper().replace(" ", "")

        if not ValidateLocation.validate_postoffice(query):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post office not found"
            )
        
        data = LocationModel.find_by_postoffice(query)

        postoffice_objects = [PostOfficeDetailSchema(**item) for item in data]

        return PostOfficeResponseSchema(
            success=True,
            data=postoffice_objects)
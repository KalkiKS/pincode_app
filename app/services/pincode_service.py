from app.models.pincode_model import PincodeModel
from app.schemas.pincode_schema import PincodeCreate
from fastapi import HTTPException, status

class PincodeService:

    @staticmethod
    def get_pincode_details(pincode: int):
        pincode_data = PincodeModel.find_by_pincode(pincode)

        if not pincode_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pincode not found"
            )
        
        return pincode_data
    
    @staticmethod
    def create_pincode(pincode_data: PincodeCreate):
        existing = PincodeModel.find_by_pincode(pincode_data.pincode)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pincode already exists"
            )
        
        return PincodeModel.create_pincode(pincode_data.dict())
    
    @staticmethod
    def get_location_details(query: str):

        location_data = PincodeModel.find_by_location(query)

        if not location_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=location_data["message"] # type: ignore
            )

        if location_data:
            return location_data
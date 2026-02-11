from fastapi import APIRouter, status
from app.services.pincode_service import PincodeService
from app.schemas.pincode_schema import PincodeCreate


router = APIRouter(
    prefix="/pincode",
    tags=["Pincode"]
)

@router.get(
        "/search",
        status_code=status.HTTP_200_OK
)
def search_qerry(location: str):
    try:
        if type(int(location)) == int:
            return PincodeService.get_pincode_details(int(location))
    except ValueError:
        pass

    location = str(location)
    location = location.upper().strip()
    if not location:
        return {
            "success": False,
            "message": "Invalid Input"
        }

    return PincodeService.get_location_details(location)


@router.get(
    "/{pincode}",
    status_code=status.HTTP_200_OK
)
def get_pincode(pincode: int):
    if pincode < 100000 or pincode > 999999:
        return {
            "success": False,
            "message": "Invalid pincode"
        }
    data = PincodeService.get_pincode_details(pincode)
    return {
        "success": True,
        "data": data
    }


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_pincode(pincode_data: PincodeCreate):
    """
    Add a new pincode
    """
    result = PincodeService.create_pincode(pincode_data)
    
    return {
        "success": True,
        "message": "Pincode created successfully",
        "pincode_id": str(result.inserted_id)
    }
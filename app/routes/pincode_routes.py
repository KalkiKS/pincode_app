from fastapi import APIRouter, status
from app.services.pincode_service import PincodeService
from app.schemas.pincode_schema import PincodeCreate
from app.services.location_services import LocationService


router = APIRouter(
    prefix="/pincode",
    tags=["Pincode"]
)

@router.get(
        "/state/{name}",
        status_code=status.HTTP_200_OK
)
def state_qerry(state: str, page: int = 1, limit: int =10):
    if page < 1 or limit > 10 and limit <= 100 :
        return {
            "success": False,
            "message": "Page must be greater than 0 and limit must be at least 10 or at most 100"
        }
    if not state:
        return {
            "success": False,
            "message": "State name is required"
        }
    query = state.upper().strip()
    data = LocationService.get_state_details(query, page, limit)
    return data

@router.get(
        "/district/{name}",
        status_code=status.HTTP_200_OK
)
def district_query(district: str, page: int = 1, limit: int =10):
    if page < 1 or limit > 10 and limit <= 100 :
        return {
            "success": False,
            "message": "Page must be greater than 0 and limit must be at least 10 or at most 100"
        }
    if not district:
        return {
            "success": False,
            "message": "District name is required"
        }
    query = district.upper().strip()
    data = LocationService.get_district_details(query, page, limit)
    return data

@router.get(
        "/postoffice/{name}",
        status_code=status.HTTP_200_OK
)
def postoffice_query(postoffice: str):
    if not postoffice:
        return {
            "success": False,
            "message": "Post office name is required"
        }
    query = postoffice.upper().strip()
    data = LocationService.get_postoffice_details(query)
    return data


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
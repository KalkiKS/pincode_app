from fastapi import APIRouter, status, Query, Path
from app.services.pincode_service import PincodeService
from app.schemas.pincode_schema import PincodeCreate, StateResponseSchema, DistrictResponseSchema, PostOfficeResponseSchema
from app.services.location_services import LocationService


router = APIRouter(
    prefix="/pincode",
    tags=["Pincode"]
)


@router.get(
        "/state/{state}",
        status_code=status.HTTP_200_OK
)
def state_qerry(state: str,
                page: int = Query(1, ge=1),
                limit: int = Query(10, ge=10, le=50)
            ):
    if not state:
        return {
            "success": False,
            "message": "State name is required"
        }
    return LocationService.get_state_details(state, page, limit)
    



@router.get(
        "/district/{district}",
        status_code=status.HTTP_200_OK
)
def district_query(district: str,
                page: int = Query(1, ge=1),
                limit: int = Query(10, ge=10, le=50)
            ):

    if not district:
        return {
            "success": False,
            "message": "District name is required"
        }
    return LocationService.get_district_details(district, page, limit)




@router.get(
        "/postoffice/{postoffice}",
        status_code=status.HTTP_200_OK
)
def postoffice_query(postoffice: str):
    if not postoffice:
        return {
            "success": False,
            "message": "Post office name is required"
        }

    return LocationService.get_postoffice_details(postoffice)





@router.get(
    "/{pincode}",
    status_code=status.HTTP_200_OK
)
def get_pincode(pincode: int = Path(..., ge=100000, le=999999)):
    
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
from fastapi import APIRouter, status, Query, Path, Depends
from app.services.pincode_service import PincodeService
from app.schemas.pincode_schema import PincodeCreate, StateResponseSchema, DistrictResponseSchema, PostOfficeResponseSchema, PaginationParams
from app.services.location_services import LocationService


router = APIRouter(
    prefix="/pincode",
    tags=["Pincode"]
)


@router.get(
        "/state/{state}",
        response_model=StateResponseSchema,
        status_code=status.HTTP_200_OK
)
def state_qerry(
                state: str = Path(..., min_length=2),
                pagination: PaginationParams = Depends()
            ):
    if not state:
        return {
            "success": False,
            "message": "State name is required"
        }
    return LocationService.get_state_details(state, pagination.page, pagination.limit)
    



@router.get(
        "/district/{district}",
        response_model=DistrictResponseSchema,
        status_code=status.HTTP_200_OK
)
def district_query(
                district: str = Path(..., min_length=2),
                pagination: PaginationParams = Depends()
            ):

    if not district:
        return {
            "success": False,
            "message": "District name is required"
        }
    return LocationService.get_district_details(district, pagination.page, pagination.limit)




@router.get(
        "/postoffice/{postoffice}",
        response_model=PostOfficeResponseSchema,
        status_code=status.HTTP_200_OK
)
def postoffice_query(postoffice: str = Path(..., min_length=2)):
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
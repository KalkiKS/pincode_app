from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DeliveryStatusEnum(str, Enum):
    DELIVERY = "Delivery"
    NOT_DELIVERY = "Non Delivery"


class PincodeBase(BaseModel):
    pincode: int = Field(..., ge=100000, le=999999)
    post_office: str = Field(...)
    area: Optional[str] = None
    district: str = Field(...)
    state: str = Field(...)
    country: str = "India"
    region: Optional[str] = None
    delivery_status: DeliveryStatusEnum = Field(...)

    @field_validator('district', 'state', 'post_office')
    @classmethod
    def validate_no_digits(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError('Must not contain digits')
        return v

class PincodeCreate(PincodeBase):
    pass
    
class PincodeResponse(PincodeBase):
    is_active: bool
    created_at: datetime
    updated_at: datetime


class StateBase(BaseModel):
    district: str
    pincodes: List[int]


class StateResponseSchema(BaseModel):
    success: bool
    page: int
    limit: int
    total_districts: int
    total_pages: int
    count: int
    data: List[StateBase]

class PostOfficeBase(BaseModel):
    name: str
    delivery: DeliveryStatusEnum

class DistrictBase(BaseModel):
    pincode: int
    post_offices: List[PostOfficeBase]

class DistrictResponseSchema(BaseModel):
    success: bool
    page: int
    limit: int
    total_pincode: int
    total_pages: int
    count: int
    data: List[DistrictBase]

class PostOffice(BaseModel):
    name: str
    type: Optional[str] = None
    delivery: DeliveryStatusEnum
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PostOfficeDetailSchema(BaseModel):
    pincode: int
    district: str
    state: str
    country: str
    region: str
    division: str
    area: Optional[str] = None
    post_office: PostOffice


class PostOfficeResponseSchema(BaseModel):
    success: bool
    data: List[PostOfficeDetailSchema]
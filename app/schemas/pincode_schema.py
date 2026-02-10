from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class DeliveryStatusEnum(str, Enum):
    DELIVERY = "Delivery"
    NOT_DELIVERY = "Not Delivery"


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
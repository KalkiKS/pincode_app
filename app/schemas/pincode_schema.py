from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PincodeBase(BaseModel):
    pincode: str = Field(...)
    post_office: str
    area: Optional[str] = None
    district: str
    state: str
    country: str = "India"
    region: Optional[str] = None
    delivery_status: str = Field(...)

class PincodeCreate(PincodeBase):
    pass

class PincodeResponse(PincodeBase):
    is_active: bool
    created_at: datetime
    updated_at: datetime
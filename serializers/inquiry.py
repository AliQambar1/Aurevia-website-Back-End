# serializers/inquiry.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InquiryCreate(BaseModel):
    listing_id: int
    full_name: str
    phone_number: str
    message: str

class InquiryUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    message: Optional[str] = None

class InquiryResponse(BaseModel):
    id: int
    listing_id: int
    full_name: str
    phone_number: str
    message: str
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
# serializers/inquiry.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InquiryCreate(BaseModel):
    listing_id: int
    full_name: str
    phone_number: str
    message: str

class InquiryResponse(InquiryCreate):
    id: int
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
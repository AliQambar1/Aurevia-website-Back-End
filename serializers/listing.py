# serializers/listing.py
from pydantic import BaseModel
from typing import Optional, Literal

class ListingBase(BaseModel):
    make: str
    model_year: int
    spec: Literal["US", "GCC", "EU"] # إجبار المستخدم على اختيار أحد هذه فقط
    exterior: str
    interior: str
    price: float
    notes: Optional[str] = None
    images: Optional[str] = None
    status: Literal["Available", "Sold"] = "Available"

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    
    make: Optional[str] = None
    model_year: Optional[int] = None
    spec: Optional[Literal["US", "GCC", "EU"]] = None
    exterior: Optional[str] = None
    interior: Optional[str] = None
    price: Optional[float] = None
    notes: Optional[str] = None
    images: Optional[str] = None
    status: Optional[Literal["Available", "Sold"]] = None

class ListingResponse(ListingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
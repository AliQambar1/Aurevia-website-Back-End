from pydantic import BaseModel
from typing import Optional, List, Literal

class ListingBase(BaseModel):
    make: str
    model_year: int
    mileage: Optional[int] = None
    spec: Literal["US", "GCC", "EU"]
    exterior: str
    interior: str
    price: float
    notes: Optional[str] = None
    images: Optional[List[str]] = []
    status: Literal["Available", "Sold"] = "Available"

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    make: Optional[str] = None
    model_year: Optional[int] = None
    mileage: Optional[int] = None
    spec: Optional[Literal["US", "GCC", "EU"]] = None
    exterior: Optional[str] = None
    interior: Optional[str] = None
    price: Optional[float] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[Literal["Available", "Sold"]] = None

class ListingResponse(ListingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

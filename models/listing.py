# models/listing.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class SpecEnum(str, enum.Enum):
    US = "US"
    GCC = "GCC"
    EU = "EU"

class StatusEnum(str, enum.Enum):
    Available = "Available"
    Sold = "Sold"

class ListingModel(BaseModel):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)       
    model_year = Column(Integer, nullable=False) 
    
   
    spec = Column(String, nullable=False)       
    status = Column(String, default="Available") 

    exterior = Column(String, nullable=False)   
    interior = Column(String, nullable=False)   
    price = Column(Float, nullable=False)
    
    notes = Column(String, nullable=True)
    images = Column(String, nullable=True)      

    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="listings")
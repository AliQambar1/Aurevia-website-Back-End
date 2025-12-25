# models/listing.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class ListingModel(BaseModel):
    __tablename__ = "listings"

    make = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    mileage = Column(Integer)
    spec = Column(String, nullable=False)
    exterior = Column(String, nullable=False)
    interior = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String)
    notes = Column(String)
    images = Column(ARRAY(String)) 
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="listings")
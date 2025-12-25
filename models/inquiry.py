# models/inquiry.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import BaseModel

class InquiryModel(BaseModel):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    message = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    listing = relationship("ListingModel") 

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("UserModel", back_populates="inquiries")
# models/inquiry.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class InquiryModel(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    # Contact information
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    message = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    # Link inquiry to a specific car
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    listing = relationship("ListingModel", backref="inquiries")

    # Link inquiry to the user who asked 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("UserModel", backref="inquiries")
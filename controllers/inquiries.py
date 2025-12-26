# controllers/inquiries.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.inquiry import InquiryModel
from models.user import UserModel
from serializers.inquiry import InquiryCreate, InquiryResponse, InquiryUpdate
from dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/api/inquiries", tags=["Inquiries"])

# Submit an Inquiry 
@router.post("/", response_model=InquiryResponse)
def create_inquiry(
    inquiry_data: InquiryCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[UserModel] = Depends(get_current_user)
):
    # Make sure user_id is set if user is logged in
    new_inquiry = InquiryModel(
        listing_id=inquiry_data.listing_id,
        full_name=inquiry_data.full_name,
        phone_number=inquiry_data.phone_number,
        message=inquiry_data.message,
        user_id=current_user.id if current_user else None
    )
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    
    print(f" Created inquiry with user_id: {new_inquiry.user_id}")  # Debug
    return new_inquiry

# Get All Inquiries Admin Only
@router.get("/", response_model=list[InquiryResponse])
def get_all_inquiries(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Security Check Only Admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
    
    return db.query(InquiryModel).all()

#  Get Inquiries for a Specific Listing (Admin sees all, User sees their own)
@router.get("/listing/{listing_id}", response_model=list[InquiryResponse])
def get_listing_inquiries(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Admin can see all inquiries for this listing
    if current_user.role == "admin":
        inquiries = db.query(InquiryModel).filter(
            InquiryModel.listing_id == listing_id
        ).order_by(InquiryModel.created_at.desc()).all()
    else:
        # Regular users can only see their own inquiries for this listing
        inquiries = db.query(InquiryModel).filter(
            InquiryModel.listing_id == listing_id,
            InquiryModel.user_id == current_user.id
        ).order_by(InquiryModel.created_at.desc()).all()
    
    return inquiries

#  Update an Inquiry (User who created it or Admin)
@router.put("/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(
    inquiry_id: int,
    inquiry_data: InquiryUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    inquiry = db.query(InquiryModel).filter(InquiryModel.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Inquiry not found"
        )
    
    # Check if user is the owner or admin
    if inquiry.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own inquiries"
        )
    
    # Update fields
    for key, value in inquiry_data.dict(exclude_unset=True).items():
        setattr(inquiry, key, value)
    
    db.commit()
    db.refresh(inquiry)
    return inquiry

# Delete an Inquiry (User who created it or Admin)
@router.delete("/{inquiry_id}")
def delete_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    inquiry = db.query(InquiryModel).filter(InquiryModel.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Inquiry not found"
        )
    
    # Check if user is the owner or admin
    if inquiry.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own inquiries"
        )
        
    db.delete(inquiry)
    db.commit()
    return {"message": "Inquiry deleted successfully"}
# controllers/inquiries.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.inquiry import InquiryModel
from models.user import UserModel
from serializers.inquiry import InquiryCreate, InquiryResponse
from dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/api/inquiries", tags=["Inquiries"])

# Submit an Inquiry 
@router.post("/", response_model=InquiryResponse)
def create_inquiry(
    inquiry_data: InquiryCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[UserModel] = Depends(get_current_user)
):
    new_inquiry = InquiryModel(
        **inquiry_data.dict(),
        user_id=current_user.id if current_user else None
    )
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry

#Get All Inquiries Admin Only
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

# Delete an Inquiry Admin Only
@router.delete("/{inquiry_id}")
def delete_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Security Check Only Admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
        
    inquiry = db.query(InquiryModel).filter(InquiryModel.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Inquiry not found"
        )
        
    db.delete(inquiry)
    db.commit()
    return {"message": "Inquiry deleted successfully"}
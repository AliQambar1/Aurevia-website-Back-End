# controllers/listings.py
from fastapi import APIRouter, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json 

from database import get_db
from models.listing import ListingModel
from models.user import UserModel
from serializers.listing import ListingResponse, ListingUpdate
from dependencies.get_current_user import get_current_user 

router = APIRouter(prefix="/api/listings", tags=["Listings"])


def check_admin_role(user: UserModel):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action (Admin only)."
        )


@router.get("/", response_model=list[ListingResponse])
def get_listings(db: Session = Depends(get_db)):
    return db.query(ListingModel).all()


@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


# UPDATED: Parse images from JSON string
@router.post("/", response_model=ListingResponse)
def create_listing(
    make: str = Form(...),
    model_year: int = Form(...),
    mileage: Optional[int] = Form(None),
    spec: str = Form(...),
    exterior: str = Form(...),
    interior: str = Form(...),
    price: float = Form(...),
    status: str = Form("Available"),
    images: str = Form(...),  # ✅ Changed from List[str] to str
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_admin_role(current_user)

    # Parse the JSON string into a list
    try:
        image_list = json.loads(images)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid images format. Expected JSON array."
        )

    new_listing = ListingModel(
        make=make,
        model_year=model_year,
        mileage=mileage,
        spec=spec,
        exterior=exterior,
        interior=interior,
        price=price,
        status=status,
        images=image_list,  #  Use parsed list
        notes=notes,
        owner_id=current_user.id
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing

@router.put("/{listing_id}", response_model=ListingResponse)
def update_listing(
    listing_id: int,
    listing_data: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_admin_role(current_user)

    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    for key, value in listing_data.dict(exclude_unset=True).items():
        setattr(listing, key, value)

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_admin_role(current_user)

    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted successfully"}

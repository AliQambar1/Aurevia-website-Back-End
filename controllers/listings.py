# controllers/listings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.listing import ListingModel
from models.user import UserModel
from serializers.listing import ListingCreate, ListingResponse, ListingUpdate
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


@router.post("/", response_model=ListingResponse)
def create_listing(
    listing: ListingCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    
    check_admin_role(current_user)

    new_listing = ListingModel(**listing.dict(), owner_id=current_user.id)
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

    listing_query = db.query(ListingModel).filter(ListingModel.id == listing_id)
    db_listing = listing_query.first()

    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    
    update_data = listing_data.dict(exclude_unset=True)
    listing_query.update(update_data)
    
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_admin_role(current_user)

    db_listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(db_listing)
    db.commit()
    return {"message": "Listing deleted successfully"}
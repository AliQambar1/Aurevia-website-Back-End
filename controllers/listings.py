# controllers/listings.py

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models.listing import ListingModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user
from pydantic import BaseModel
import json

router = APIRouter(prefix="/api/listings", tags=["Listings"])

# Pydantic models
class ListingUpdate(BaseModel):
    make: str
    model_year: int
    mileage: int
    spec: str
    exterior: str
    interior: str
    price: float
    status: str
    images: List[str]
    notes: Optional[str] = None

class ListingResponse(BaseModel):
    id: int
    make: str
    model_year: int
    mileage: int
    spec: str
    exterior: str
    interior: str
    price: float
    status: str
    images: List[str]
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

# Get all listings
@router.get("/", response_model=List[ListingResponse])
def get_all_listings(db: Session = Depends(get_db)):
    listings = db.query(ListingModel).all()
    
    # Ensure images is always a list
    for listing in listings:
        if isinstance(listing.images, str):
            try:
                listing.images = json.loads(listing.images)
            except:
                listing.images = []
        elif not isinstance(listing.images, list):
            listing.images = []
    
    return listings

# Get single listing by ID
@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    print(f"\n🔍 GET Listing {listing_id}")
    print(f"📸 Images from DB (raw): {listing.images}")
    print(f"📸 Images type: {type(listing.images)}")
    
    # Fix the images field
    if listing.images:
        if isinstance(listing.images, str):
            print(f"⚠️ Images is string, parsing...")
            try:
                parsed = json.loads(listing.images)
                # Check if it resulted in a string again
                if isinstance(parsed, str):
                    # Split by comma
                    listing.images = [url.strip() for url in parsed.split(',') if url.strip()]
                else:
                    listing.images = parsed
                print(f"✅ Parsed to: {listing.images}")
            except Exception as e:
                print(f"❌ Parse failed: {e}")
                listing.images = []
        elif isinstance(listing.images, list):
            # Check if it's a list of single characters (the bug!)
            if len(listing.images) > 10 and all(isinstance(item, str) and len(item) == 1 for item in listing.images):
                print(f"🔧 Fixing character list...")
                joined = ''.join(listing.images)
                # Remove curly braces
                joined = joined.strip('{}')
                # Split by comma
                listing.images = [url.strip() for url in joined.split(',') if url.strip()]
                print(f"✅ Fixed to: {listing.images}")
            else:
                # Filter to keep only valid URLs
                listing.images = [img for img in listing.images if isinstance(img, str) and img.startswith('http')]
        else:
            listing.images = []
    else:
        listing.images = []
    
    print(f"📤 Returning images: {listing.images}")
    print(f"📊 Count: {len(listing.images)}\n")
    
    return listing

# Create new listing (FormData)
@router.post("/", response_model=ListingResponse)
def create_listing(
    make: str = Form(...),
    model_year: int = Form(...),
    mileage: int = Form(0),
    spec: str = Form(...),
    exterior: str = Form(...),
    interior: str = Form(...),
    price: float = Form(...),
    status: str = Form(...),
    images: str = Form(...),  # JSON string
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Parse images JSON string
    try:
        image_list = json.loads(images)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid images format"
        )
    
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create listings"
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
        images=image_list,
        notes=notes
    )
    
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    
    print(f"✅ Created new listing {new_listing.id}")
    return new_listing

# Update listing (JSON)
@router.put("/{listing_id}", response_model=ListingResponse)
def update_listing(
    listing_id: int,
    listing_data: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    print(f"\n{'='*50}")
    print(f"🔄 UPDATE REQUEST for listing {listing_id}")
    print(f"{'='*50}")
    print(f"👤 User: {current_user.id} | Role: {current_user.role}")
    print(f"📦 Data received:")
    print(f"   - Make: {listing_data.make}")
    print(f"   - Year: {listing_data.model_year}")
    print(f"   - Price: {listing_data.price}")
    print(f"   - Status: {listing_data.status}")
    print(f"📸 Images:")
    print(f"   - Type: {type(listing_data.images)}")
    print(f"   - Is List: {isinstance(listing_data.images, list)}")
    print(f"   - Count: {len(listing_data.images)}")
    if listing_data.images:
        for i, img in enumerate(listing_data.images):
            print(f"   - Image {i+1}: {img[:80]}..." if len(img) > 80 else f"   - Image {i+1}: {img}")
    print(f"{'='*50}\n")
    
    # Find the listing
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    
    if not listing:
        print(f"❌ Listing {listing_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    # Only admins can update listings
    if current_user.role != "admin":
        print(f"🚫 Authorization failed - user is not admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update listings"
        )
    
    # Update all fields
    print(f"📝 Updating listing fields...")
    listing.make = listing_data.make
    listing.model_year = listing_data.model_year
    listing.mileage = listing_data.mileage
    listing.spec = listing_data.spec
    listing.exterior = listing_data.exterior
    listing.interior = listing_data.interior
    listing.price = listing_data.price
    listing.status = listing_data.status
    listing.images = listing_data.images
    listing.notes = listing_data.notes
    
    # Commit to database
    try:
        db.commit()
        db.refresh(listing)
        print(f"✅ Listing {listing_id} updated successfully!")
        print(f"✅ Updated images count: {len(listing.images)}")
        print(f"{'='*50}\n")
    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    return listing

# Delete listing
@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    # Only admins can delete listings
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete listings"
        )
    
    db.delete(listing)
    db.commit()
    
    print(f"🗑️ Listing {listing_id} deleted successfully")
    return {"message": "Listing deleted successfully"}
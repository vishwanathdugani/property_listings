from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token, security
from app.core.auth import oauth2_scheme, get_current_user
from app.crud.crud_property import (
    create_property_db, get_property_db, update_property_db, delete_property_db,
    get_properties_db, get_filtered_properties_db
)
from app.db.session import get_db
from app.schemas.property import (
    PropertyCreate, PropertyUpdate, PropertyBase,
    PropertyListings, PropertyListing, PaginatedPropertyListingsResponse
)


router = APIRouter()


@router.post("/token")
async def login_for_access_token(credentials: HTTPBasicCredentials = Depends(security)):
    """Generate an access token for authenticated users."""
    user = authenticate_user(credentials)
    access_token_expires = timedelta(minutes=5)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/properties/", response_model=PropertyCreate, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(property_: PropertyBase, db: Session = Depends(get_db),
                             token: str = Depends(get_current_user)):
    """Endpoint to create a new property."""
    return create_property_db(db=db, property=property_)


@router.get("/properties/", response_model=List[PropertyBase], status_code=status.HTTP_200_OK)
def read_properties_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                             token: str = Depends(get_current_user)):
    """Endpoint to retrieve a list of properties."""
    properties = get_properties_db(db, skip=skip, limit=limit)
    return properties


@router.get("/properties_listings/", response_model=PaginatedPropertyListingsResponse,
            status_code=status.HTTP_200_OK)
def read_property_listings_endpoint(
    full_address: str = None, class_description: str = None,
    estimated_market_value_min: int = None, estimated_market_value_max: int = None,
    bldg_use: str = None, building_sq_ft_min: int = None, building_sq_ft_max: int = None,
    skip: int = 0, limit: int = 25, db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    """Endpoint to retrieve a filtered list of property listings."""
    properties = get_filtered_properties_db(
        db, full_address=full_address, class_description=class_description,
        estimated_market_value_min=estimated_market_value_min, estimated_market_value_max=estimated_market_value_max,
        bldg_use=bldg_use, building_sq_ft_min=building_sq_ft_min, building_sq_ft_max=building_sq_ft_max,
        skip=skip, limit=limit
    )

    properties_models = [PropertyListings.from_orm(prop) for prop in properties]
    more_exists = len(properties) == limit
    return PaginatedPropertyListingsResponse(properties=properties_models, moreExists=more_exists)


@router.get("/properties/{property_id}", response_model=PropertyListing, status_code=status.HTTP_200_OK)
def read_property_endpoint(property_id: int, db: Session = Depends(get_db),
                           token: str = Depends(get_current_user)):
    """Endpoint to retrieve details of a specific property."""
    db_property = get_property_db(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return jsonable_encoder(db_property)


@router.put("/properties/{property_id}", response_model=PropertyUpdate, status_code=status.HTTP_200_OK)
def update_property_endpoint(property_id: int, property_: PropertyUpdate, db: Session = Depends(get_db),
                             token: str = Depends(get_current_user)):
    """Endpoint to update details of a specific property."""
    db_property = update_property_db(db=db, property_id=property_id, property=property_)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


@router.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_endpoint(property_id: int, db: Session = Depends(get_db),
                             token: str = Depends(get_current_user)):
    """Endpoint to delete a specific property."""
    success = delete_property_db(db, property_id=property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")

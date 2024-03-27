from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token, security
from app.core.auth import oauth2_scheme, get_current_user
from app.db.session import get_db

from app.crud.crud_property import get_filtered_properties, create_property_db, create_property_classification,\
    create_sales_appeal, create_assessment, create_property_feature, create_misc_info, get_slider_ranges_crud, get_property_details
from app.schemas.property import  PropertyQuerySchema, PropertyCreateResponse, PropertyCreateRequest, PropertyClassificationCreate, \
    AssessmentCreate, SalesAppealCreate, PropertyFeatureCreate, MiscInfoCreate, PaginatedPropertyResponse, SliderRangeResponse, PropertyDetailResponse

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


@router.post("/properties/", response_model=PropertyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(property_: PropertyCreateRequest, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    """Endpoint to create a new property."""
    created_property = create_property_db(db=db, property_data=property_)
    return created_property


@router.get("/properties_listings/", response_model=PaginatedPropertyResponse,
            status_code=status.HTTP_200_OK)
async def read_property_listings_endpoint(query: PropertyQuerySchema = Depends(), db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    properties, more_exists = get_filtered_properties(db, query)

    return {"data": properties, "more_exists": more_exists}


@router.get("/properties/range", response_model=SliderRangeResponse)
def get_slider_ranges(db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return get_slider_ranges_crud(db)


@router.post("/property_classifications/", status_code=status.HTTP_201_CREATED)
def create_property_classification_endpoint(classification_data: PropertyClassificationCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return create_property_classification(db=db, classification_data=classification_data)


@router.post("/assessments/", status_code=status.HTTP_201_CREATED)
def create_assessment_endpoint(assessment_data: AssessmentCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return create_assessment(db=db, assessment_data=assessment_data)


@router.post("/sales_appeals/", status_code=status.HTTP_201_CREATED)
def create_sales_appeal_endpoint(sales_appeal_data: SalesAppealCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return create_sales_appeal(db=db, sales_appeal_data=sales_appeal_data)


@router.post("/property_features/", status_code=status.HTTP_201_CREATED)
def create_property_feature_endpoint(feature_data: PropertyFeatureCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return create_property_feature(db=db, feature_data=feature_data)


@router.post("/misc_info/", status_code=status.HTTP_201_CREATED)
def create_misc_info_endpoint(misc_info_data: MiscInfoCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    return create_misc_info(db=db, misc_info_data=misc_info_data)


@router.get("/properties/{property_id}", response_model=PropertyDetailResponse)
def read_property_details(property_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)) -> Any:
    return get_property_details(property_id=property_id, db=db)

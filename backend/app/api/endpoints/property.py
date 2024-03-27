from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token, security
from app.db.session import get_db
from app.crud.crud_property import (
    get_filtered_properties, create_property_db, create_property_classification,
    create_sales_appeal, create_assessment, create_property_feature,
    create_misc_info, get_slider_ranges_crud, get_property_details
)
from app.schemas.property import (
    PropertyQuerySchema, PropertyCreateResponse, PropertyCreateRequest,
    PropertyClassificationCreate, AssessmentCreate, SalesAppealCreate,
    PropertyFeatureCreate, MiscInfoCreate, PaginatedPropertyResponse,
    SliderRangeResponse, PropertyDetailResponse
)

router = APIRouter()


@router.post("/token")
async def login_for_access_token(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Generate an access token for authenticated users.

    Args:
        credentials (HTTPBasicCredentials): The credentials for authentication.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user = authenticate_user(credentials)
    access_token_expires = timedelta(minutes=5)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/properties/", response_model=PropertyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_property_endpoint(property_: PropertyCreateRequest, db: Session = Depends(get_db)):
    """
    Endpoint to create a new property.

    Args:
        property_ (PropertyCreateRequest): The property creation request schema.
        db (Session): The database session.

    Returns:
        PropertyCreateResponse: The response schema for property creation.
    """
    created_property = create_property_db(db=db, property_data=property_)
    return created_property


@router.get("/properties_listings/", response_model=PaginatedPropertyResponse, status_code=status.HTTP_200_OK)
async def read_property_listings_endpoint(query: PropertyQuerySchema = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to list properties based on a query.

    Args:
        query (PropertyQuerySchema): The property query parameters.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the listed properties and a flag indicating if more properties exist.
    """
    properties, more_exists = await get_filtered_properties(db, query)
    return {"data": properties, "more_exists": more_exists}


@router.get("/properties/range", response_model=SliderRangeResponse)
def get_slider_ranges(db: Session = Depends(get_db)):
    """
    Get the slider ranges for property filters.

    Args:
        db (Session): The database session.

    Returns:
        SliderRangeResponse: The slider range response schema.
    """
    return get_slider_ranges_crud(db)


@router.post("/property_classifications/", status_code=status.HTTP_201_CREATED)
def create_property_classification_endpoint(classification_data: PropertyClassificationCreate,
                                            db: Session = Depends(get_db)):
    """
    Endpoint to create a new property classification.

    Args:
        classification_data (PropertyClassificationCreate): The classification creation schema.
        db (Session): The database session.

    Returns:
        dict: The created property classification.
    """
    return create_property_classification(db=db, classification_data=classification_data)


@router.post("/assessments/", status_code=status.HTTP_201_CREATED)
def create_assessment_endpoint(assessment_data: AssessmentCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new assessment.

    Args:
        assessment_data (AssessmentCreate): The assessment creation schema.
        db (Session): The database session.

    Returns:
        dict: The created assessment.
    """
    return create_assessment(db=db, assessment_data=assessment_data)


@router.post("/sales_appeals/", status_code=status.HTTP_201_CREATED)
def create_sales_appeal_endpoint(sales_appeal_data: SalesAppealCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new sales appeal.

    Args:
        sales_appeal_data (SalesAppealCreate): The sales appeal creation schema.
        db (Session): The database session.

    Returns:
        dict: The created sales appeal.
    """
    return create_sales_appeal(db=db, sales_appeal_data=sales_appeal_data)


@router.post("/property_features/", status_code=status.HTTP_201_CREATED)
def create_property_feature_endpoint(feature_data: PropertyFeatureCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new property feature.

    Args:
        feature_data (PropertyFeatureCreate): The property feature creation schema.
        db (Session): The database session.

    Returns:
        dict: The created property feature.
    """
    return create_property_feature(db=db, feature_data=feature_data)


@router.post("/misc_info/", status_code=status.HTTP_201_CREATED)
def create_misc_info_endpoint(misc_info_data: MiscInfoCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create miscellaneous property information.

    Args:
        misc_info_data (MiscInfoCreate): The miscellaneous info creation schema.
        db (Session): The database session.

    Returns:
        dict: The created miscellaneous information.
    """
    return create_misc_info(db=db, misc_info_data=misc_info_data)


@router.get("/properties/{property_id}", response_model=PropertyDetailResponse)
async def read_property_details(property_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Read the details of a specific property.

    Args:
        property_id (int): The unique identifier of the property.
        db (Session): The database session.

    Returns:
        PropertyDetailResponse: The detailed information about the property.
    """
    property_ = await get_property_details(property_id=property_id, db=db)
    return property_

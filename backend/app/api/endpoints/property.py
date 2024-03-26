from datetime import timedelta
from typing import List, Any

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token, security
from app.core.auth import oauth2_scheme, get_current_user
from app.db.session import get_db

from app.crud.crud_property import get_filtered_properties, create_property_db, create_property_classification,\
    create_sales_appeal, create_assessment, create_property_feature, create_misc_info
from app.schemas.property import  PropertyQuerySchema, PropertyCreateResponse, PropertyCreateRequest, PropertyClassificationCreate, \
    AssessmentCreate, SalesAppealCreate, PropertyFeatureCreate, MiscInfoCreate, PaginatedPropertyResponse, SliderRangeResponse, PropertyDetailResponse
from app.models.models import Assessment, PropertyFeature, Property, PropertyClassification, SalesAppeal, MiscInfo

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
    emv_min, emv_max = db.query(
        func.min(Assessment.estimated_market_value), func.max(Assessment.estimated_market_value)
    ).first()

    sq_ft_min, sq_ft_max = db.query(
        func.min(PropertyFeature.building_sq_ft), func.max(PropertyFeature.building_sq_ft)
    ).first()

    return SliderRangeResponse(
        estimated_market_value={"min": emv_min or 0, "max": emv_max or 10000000},
        building_sq_ft={"min": sq_ft_min or 0, "max": sq_ft_max or 20000},
    )


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
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    # Assuming single object relationships (for simplicity)
    property_classification = db.query(PropertyClassification).filter(
        PropertyClassification.property_id == property_id).first()
    assessment = db.query(Assessment).filter(Assessment.property_id == property_id).first()
    sales_appeal = db.query(SalesAppeal).filter(SalesAppeal.property_id == property_id).first()
    property_feature = db.query(PropertyFeature).filter(PropertyFeature.property_id == property_id).first()
    misc_info = db.query(MiscInfo).filter(MiscInfo.property_id == property_id).first()

    response_data = {
        "id": property_obj.id,
        "longitude": property_obj.longitude,
        "latitude": property_obj.latitude,
        "zip": property_obj.zip,
        "house_no": property_obj.house_no,
        "dir": property_obj.dir,
        "street": property_obj.street,
        "suffix": property_obj.suffix,
        "apt": property_obj.apt,
        "city": property_obj.city,
    }

    if property_classification:
        response_data.update({
            "class_description": property_classification.class_description,
            "ovac_ls": property_classification.ovac_ls,
            "res_type": property_classification.res_type,
            "bldg_use": property_classification.bldg_use,
            "apt_desc": property_classification.apt_desc,
        })

    if assessment:
        response_data.update({
            "current_land": assessment.current_land,
            "current_building": assessment.current_building,
            "current_total": assessment.current_total,
            "estimated_market_value": assessment.estimated_market_value,
            "prior_land": assessment.prior_land,
            "prior_building": assessment.prior_building,
            "prior_total": assessment.prior_total,
        })

    if sales_appeal:
        response_data.update({
            "multi_sale": sales_appeal.multi_sale,
            "deed_type": sales_appeal.deed_type,
            "sale_date": sales_appeal.sale_date,
            "sale_amount": sales_appeal.sale_amount,
        })

    if property_feature:
        response_data.update({
            "comm_units": property_feature.comm_units,
            "ext_desc": property_feature.ext_desc,
            "full_bath": property_feature.full_bath,
            "half_bath": property_feature.half_bath,
            "bsmnt_desc": property_feature.bsmnt_desc,
            "attic_desc": property_feature.attic_desc,
            "ac": property_feature.ac,
            "fireplace": property_feature.fireplace,
            "gar_desc": property_feature.gar_desc,
            "age": property_feature.age,
            "building_sq_ft": property_feature.building_sq_ft,
            "land_sq_ft": property_feature.land_sq_ft,
        })

    if misc_info:
        response_data.update({
            "rec_type": misc_info.rec_type,
            "pin": misc_info.pin,
            "town": misc_info.town,
            "volume": misc_info.volume,
            "loc": misc_info.loc,
            "tax_code": misc_info.tax_code,
            "neighborhood": misc_info.neighborhood,
        })

    property_detail_response = PropertyDetailResponse(**response_data)
    return property_detail_response

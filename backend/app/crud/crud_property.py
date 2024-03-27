from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from typing import List, Tuple

from app.schemas.property import (
    PropertyQuerySchema, PropertyCreateRequest, PropertyClassificationCreate,
    AssessmentCreate, SalesAppealCreate, PropertyFeatureCreate, MiscInfoCreate,
    SliderRangeResponse, PropertyDetailResponse
)
from app.models.models import (
    SalesAppeal, MiscInfo, Property, PropertyClassification,
    Assessment, PropertyFeature
)


def filter_by_address_components(query, address: str):
    """Filters query based on address components."""
    if address:
        address_components = address.split()
        conditions = [
            or_(
                Property.house_no.ilike(f"%{component}%"),
                Property.dir.ilike(f"%{component}%"),
                Property.street.ilike(f"%{component}%"),
                Property.suffix.ilike(f"%{component}%"),
                Property.apt.ilike(f"%{component}%"),
                Property.city.ilike(f"%{component}%")
            ) for component in address_components
        ]
        query = query.filter(or_(*conditions))
    return query


def apply_other_filters(query, query_params: PropertyQuerySchema):
    """Applies non-address filters to query."""
    if query_params.class_description:
        query = query.filter(PropertyClassification.class_description.ilike(f"%{query_params.class_description}%"))
    if query_params.estimated_market_value_min is not None:
        query = query.filter(Assessment.estimated_market_value >= query_params.estimated_market_value_min)
    if query_params.estimated_market_value_max is not None:
        query = query.filter(Assessment.estimated_market_value <= query_params.estimated_market_value_max)
    if query_params.building_sq_ft_min is not None:
        query = query.filter(PropertyFeature.building_sq_ft >= query_params.building_sq_ft_min)
    if query_params.building_sq_ft_max is not None:
        query = query.filter(PropertyFeature.building_sq_ft <= query_params.building_sq_ft_max)
    if query_params.bldg_use:
        query = query.filter(PropertyClassification.bldg_use.ilike(f"%{query_params.bldg_use}%"))
    return query


def paginate_query(query, skip: int, limit: int) -> Tuple[List[Property], bool]:
    """Paginates query results."""
    results = query.offset(skip).limit(limit + 1).all()
    more_exists = len(results) > limit
    properties = results[:limit]
    return properties, more_exists


def get_filtered_properties(db: Session, query_params: PropertyQuerySchema) -> Tuple[List[Property], bool]:
    """Returns filtered properties based on query params."""
    query = db.query(
        Property.id,
        (
         Property.house_no + ' ' + Property.dir + ' ' + Property.street + ' ' + Property.suffix + ' ' + Property.apt + ' ' + Property.city).label(
            'full_address'),
        Property.longitude,
        Property.latitude,
        PropertyClassification.class_description,
        Assessment.estimated_market_value,
        PropertyFeature.building_sq_ft,
        PropertyClassification.bldg_use,
    ).join(PropertyClassification, Property.id == PropertyClassification.property_id
           ).join(Assessment, Property.id == Assessment.property_id
                  ).join(PropertyFeature, Property.id == PropertyFeature.property_id)

    query = filter_by_address_components(query, query_params.full_address)
    query = apply_other_filters(query, query_params)

    return paginate_query(query, query_params.skip, query_params.limit)


def create_property_db(db: Session, property_data: PropertyCreateRequest) -> Property:
    """Creates and returns a new property in the database."""
    new_property = Property(**property_data.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


def create_property_classification(db: Session, classification_data: PropertyClassificationCreate) -> PropertyClassification:
    """Creates and returns a new property classification."""
    new_classification = PropertyClassification(**classification_data.dict())
    db.add(new_classification)
    db.commit()
    db.refresh(new_classification)
    return new_classification


def create_assessment(db: Session, assessment_data: AssessmentCreate) -> Assessment:
    """Creates and returns a new property assessment."""
    new_assessment = Assessment(**assessment_data.dict())
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    return new_assessment


def create_sales_appeal(db: Session, sales_appeal_data: SalesAppealCreate) -> SalesAppeal:
    """Creates and returns a new sales appeal."""
    new_sales_appeal = SalesAppeal(**sales_appeal_data.dict())
    db.add(new_sales_appeal)
    db.commit()
    db.refresh(new_sales_appeal)
    return new_sales_appeal


def create_property_feature(db: Session, feature_data: PropertyFeatureCreate) -> PropertyFeature:
    """Creates and returns a new property feature."""
    new_feature = PropertyFeature(**feature_data.dict())
    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature


def create_misc_info(db: Session, misc_info_data: MiscInfoCreate) -> MiscInfo:
    """Creates and returns new miscellaneous property information."""
    new_misc_info = MiscInfo(**misc_info_data.dict())
    db.add(new_misc_info)
    db.commit()
    db.refresh(new_misc_info)
    return new_misc_info


def get_slider_ranges_crud(db: Session) -> SliderRangeResponse:
    """Returns minimum and maximum values for slider filters."""
    emv_min, emv_max = db.query(
        func.min(Assessment.estimated_market_value),
        func.max(Assessment.estimated_market_value)
    ).first()

    sq_ft_min, sq_ft_max = db.query(
        func.min(PropertyFeature.building_sq_ft),
        func.max(PropertyFeature.building_sq_ft)
    ).first()

    return SliderRangeResponse(
        estimated_market_value={"min": emv_min or 0, "max": emv_max or 10000000},
        building_sq_ft={"min": sq_ft_min or 0, "max": sq_ft_max or 20000},
    )


def fetch_property_classification(db: Session, property_id: int):
    """Fetches and returns the property classification for a given property."""
    return db.query(PropertyClassification).filter(
        PropertyClassification.property_id == property_id).first()


def fetch_assessment(db: Session, property_id: int):
    """Fetches and returns the assessment for a given property."""
    return db.query(Assessment).filter(Assessment.property_id == property_id).first()


def fetch_sales_appeal(db: Session, property_id: int):
    """Fetches and returns the sales appeal for a given property."""
    return db.query(SalesAppeal).filter(SalesAppeal.property_id == property_id).first()


def fetch_property_feature(db: Session, property_id: int):
    """Fetches and returns the property feature for a given property."""
    return db.query(PropertyFeature).filter(PropertyFeature.property_id == property_id).first()


def fetch_misc_info(db: Session, property_id: int):
    """Fetches and returns miscellaneous information for a given property."""
    return db.query(MiscInfo).filter(MiscInfo.property_id == property_id).first()


def get_property_details(property_id: int, db: Session) -> PropertyDetailResponse:
    """Fetches and returns detailed information for a given property."""
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    property_classification = fetch_property_classification(db, property_id)
    assessment = fetch_assessment(db, property_id)
    sales_appeal = fetch_sales_appeal(db, property_id)
    property_feature = fetch_property_feature(db, property_id)
    misc_info = fetch_misc_info(db, property_id)

    # Combine data from different sources into a single response dictionary
    response_data = {**property_obj.__dict__}
    for detail in [property_classification, assessment, sales_appeal, property_feature, misc_info]:
        if detail:
            response_data.update(detail.__dict__)

    # Exclude internal SQLAlchemy attributes
    filtered_response_data = {k: v for k, v in response_data.items() if not k.startswith('_')}

    return PropertyDetailResponse(**filtered_response_data)



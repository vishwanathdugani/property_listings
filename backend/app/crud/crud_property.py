from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from typing import List, Tuple

from app.schemas.property import PropertyQuerySchema, PropertyCreateRequest, PropertyClassificationCreate, \
    AssessmentCreate, SalesAppealCreate, PropertyFeatureCreate, MiscInfoCreate
from app.models.models import SalesAppeal, MiscInfo, Property, PropertyClassification, \
    Assessment, PropertyFeature


def filter_by_address_components(query, address: str):
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
        # Apply all conditions using or_
        query = query.filter(or_(*conditions))
    return query



def apply_other_filters(query, query_params: PropertyQuerySchema):
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
    results = query.offset(skip).limit(limit + 1).all()
    more_exists = len(results) > limit
    properties = results[:limit]
    return properties, more_exists



def get_filtered_properties(db: Session, query_params: PropertyQuerySchema) -> Tuple[List[Property], bool]:
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

    # Apply filters
    query = filter_by_address_components(query, query_params.full_address)
    query = apply_other_filters(query, query_params)

    # Apply pagination and return results
    return paginate_query(query, query_params.skip, query_params.limit)


def create_property_db(db: Session, property_data: PropertyCreateRequest) -> Property:
    """
    Create a new property in the database.

    Parameters:
        db (Session): SQLAlchemy session object.
        property_data (PropertyCreateRequest): Data for the new property.

    Returns:
        Property: The newly created Property instance.
    """
    new_property = Property(**property_data.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


def create_property_classification(db: Session, classification_data: PropertyClassificationCreate) -> PropertyClassification:
    new_classification = PropertyClassification(**classification_data.dict())
    db.add(new_classification)
    db.commit()
    db.refresh(new_classification)
    return new_classification


def create_assessment(db: Session, assessment_data: AssessmentCreate) -> Assessment:
    new_assessment = Assessment(**assessment_data.dict())
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    return new_assessment

def create_sales_appeal(db: Session, sales_appeal_data: SalesAppealCreate) -> SalesAppeal:
    new_sales_appeal = SalesAppeal(**sales_appeal_data.dict())
    db.add(new_sales_appeal)
    db.commit()
    db.refresh(new_sales_appeal)
    return new_sales_appeal

def create_property_feature(db: Session, feature_data: PropertyFeatureCreate) -> PropertyFeature:
    new_feature = PropertyFeature(**feature_data.dict())
    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature

def create_misc_info(db: Session, misc_info_data: MiscInfoCreate) -> MiscInfo:
    new_misc_info = MiscInfo(**misc_info_data.dict())
    db.add(new_misc_info)
    db.commit()
    db.refresh(new_misc_info)
    return new_misc_info


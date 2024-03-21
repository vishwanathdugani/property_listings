from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.models import Property


def get_property_db(db: Session, property_id: int) -> Property:
    """
    Retrieve a single property by its ID.

    Parameters:
        db (Session): SQLAlchemy database session.
        property_id (int): Unique identifier of the property.

    Returns:
        Property: An instance of the Property model.
    """
    return db.query(Property).filter(Property.id == property_id).first()


def get_properties_db(db: Session, skip: int = 0, limit: int = 100) -> list:
    """
    Retrieve a list of properties, with optional skipping and limiting for pagination.

    Parameters:
        db (Session): SQLAlchemy database session.
        skip (int): Number of records to skip (default is 0).
        limit (int): Maximum number of records to return (default is 100).

    Returns:
        list: A list of Property instances.
    """
    return db.query(Property).offset(skip).limit(limit).all()


def create_property_db(db: Session, property: Property) -> Property:
    """
    Create a new property in the database.

    Parameters:
        db (Session): SQLAlchemy database session.
        property (Property): Property data to create.

    Returns:
        Property: The newly created Property instance.
    """
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def update_property_db(db: Session, property_id: int, property: Property) -> Property:
    """
    Update an existing property by its ID.

    Parameters:
        db (Session): SQLAlchemy database session.
        property_id (int): Unique identifier of the property to update.
        property (Property): New data for the property.

    Returns:
        Property: The updated Property instance, or None if not found.
    """
    db_property = get_property_db(db, property_id=property_id)
    if not db_property:
        return None

    update_data = property.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_property, key, value)

    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def delete_property_db(db: Session, property_id: int) -> bool:
    """
    Delete a property by its ID.

    Parameters:
        db (Session): SQLAlchemy database session.
        property_id (int): Unique identifier of the property to delete.

    Returns:
        bool: True if the property was deleted, False otherwise.
    """
    db_property = get_property_db(db, property_id=property_id)
    if db_property is not None:
        db.delete(db_property)
        db.commit()
        return True
    return False


def get_filtered_properties_db(
        db: Session,
        full_address: str = None,
        class_description: str = None,
        estimated_market_value_min: int = None,
        estimated_market_value_max: int = None,
        bldg_use: str = None,
        building_sq_ft_min: int = None,
        building_sq_ft_max: int = None,
        skip: int = 0,
        limit: int = 100
) -> list:
    """
    Retrieve a filtered list of properties based on various criteria.

    Parameters:
        db (Session): SQLAlchemy database session.
        full_address (str): Full address to filter by (optional).
        class_description (str): Class description to filter by (optional).
        estimated_market_value_min (int): Minimum estimated market value to filter by (optional).
        estimated_market_value_max (int): Maximum estimated market value to filter by (optional).
        bldg_use (str): Building use to filter by (optional).
        building_sq_ft_min (int): Minimum building square footage to filter by (optional).
        building_sq_ft_max (int): Maximum building square footage to filter by (optional).
        skip (int): Number of records to skip (default is 0).
        limit (int): Maximum number of records to return (default is 100).

    Returns:
        list: A list of filtered Property instances.
    """
    query = db.query(Property)

    if full_address:
        query = query.filter(Property.full_address.ilike(f"%{full_address}%"))
    if class_description:
        query = query.filter(Property.class_description.ilike(f"%{class_description}%"))
    if estimated_market_value_min is not None:
        query = query.filter(Property.estimated_market_value >= estimated_market_value_min)
    if estimated_market_value_max is not None:
        query = query.filter(Property.estimated_market_value <= estimated_market_value_max)
    if bldg_use:
        query = query.filter(Property.bldg_use.ilike(f"%{bldg_use}%"))
    if building_sq_ft_min is not None:
        query = query.filter(Property.building_sq_ft >= building_sq_ft_min)
    if building_sq_ft_max is not None:
        query = query.filter(Property.building_sq_ft <= building_sq_ft_max)

    return query.offset(skip).limit(limit).all()


def get_property_value_range(db: Session) -> dict:
    """Retrieve the minimum and maximum values for estimated market value and building square footage."""
    max_min_values = db.query(
        func.min(Property.estimated_market_value).label("min_estimated_market_value"),
        func.max(Property.estimated_market_value).label("max_estimated_market_value"),
        func.min(Property.building_sq_ft).label("min_building_sq_ft"),
        func.max(Property.building_sq_ft).label("max_building_sq_ft")
    ).first()
    return {
        "estimated_market_value": {"min": max_min_values.min_estimated_market_value, "max": max_min_values.max_estimated_market_value},
        "building_sq_ft": {"min": max_min_values.min_building_sq_ft, "max": max_min_values.max_building_sq_ft}
    }
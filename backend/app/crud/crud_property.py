from sqlalchemy.orm import Session
from app.models.models import Property


def get_property_db(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()


def get_properties_db(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Property).offset(skip).limit(limit).all()


def create_property_db(db: Session, property: Property):
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def update_property_db(db: Session, property_id: int, property: Property):
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


def delete_property_db(db: Session, property_id: int):
    db_property = get_property_db(db, property_id=property_id)
    if db_property is not None:
        db.delete(db_property)
        db.commit()
        return True
    return False


def get_filtered_properties_db(
    db: Session,
    full_address: str,
    class_description: str,
    estimated_market_value_min: int,
    estimated_market_value_max: int,
    bldg_use: str,
    building_sq_ft_min: int,
    building_sq_ft_max: int,
    skip: int,
    limit: int
):
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
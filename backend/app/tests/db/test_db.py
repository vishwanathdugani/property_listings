from sqlalchemy.orm import Session
from crud.crud_property import create_property_db, get_filtered_properties
from schemas.property import PropertyCreateRequest


def test_create_property(db_session: Session):
    property_data = PropertyCreateRequest(
        longitude=123.456,
        latitude=78.910,
        zip="12345",
        house_no="123",
        dir="N",
        street="Main",
        suffix="St",
        apt="1A",
        city="Anytown"
    )
    property = create_property_db(db_session, property_data)
    assert property.id is not None
    assert property.zip == "12345"


def test_get_filtered_properties(db_session: Session):
    properties, more_exists = get_filtered_properties(db_session, {})
    assert isinstance(properties, list)
    assert isinstance(more_exists, bool)

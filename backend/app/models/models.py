from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Index, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base



class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    zip = Column(String, index=True)
    house_no = Column(String, nullable=False)
    dir = Column(String)
    street = Column(String, nullable=False)
    suffix = Column(String)
    apt = Column(String)
    city = Column(String, nullable=False)

    assessments = relationship("Assessment", back_populates="property")
    sales_appeals = relationship("SalesAppeal", back_populates="property")
    property_features = relationship("PropertyFeature", back_populates="property")
    misc_info = relationship("MiscInfo", back_populates="property")
    property_classifications = relationship("PropertyClassification", back_populates="property")
    __table_args__ = (Index('zip', 'house_no', 'street', 'suffix', 'apt', 'city', unique=True),)


class PropertyClassification(Base):
    __tablename__ = 'property_classifications'
    property_id = Column(Integer, ForeignKey('properties.id'))
    id = Column(Integer, primary_key=True)
    ovac_ls = Column(Integer)
    class_description = Column(Text, index=True)
    res_type = Column(String)
    bldg_use = Column(String, index=True)
    apt_desc = Column(String)
    property = relationship("Property", back_populates="property_classifications")



class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    current_land = Column(Integer)
    current_building = Column(Integer)
    current_total = Column(Integer)
    estimated_market_value = Column(Integer, index=True)
    prior_land = Column(Integer)
    prior_building = Column(Integer)
    prior_total = Column(Integer)
    property = relationship("Property", back_populates="assessments")


class SalesAppeal(Base):
    __tablename__ = 'sales_appeals'
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    multi_sale = Column(Boolean)
    deed_type = Column(Integer)
    sale_date = Column(DateTime, nullable=True)
    sale_amount = Column(Integer)
    property = relationship("Property", back_populates="sales_appeals")


class PropertyFeature(Base):
    __tablename__ = 'property_features'
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    comm_units = Column(Integer)
    ext_desc = Column(String)
    full_bath = Column(Integer)
    half_bath = Column(Integer)
    bsmnt_desc = Column(String)
    attic_desc = Column(String)
    ac = Column(Integer)
    fireplace = Column(Integer)
    gar_desc = Column(String)
    age = Column(Integer)
    building_sq_ft = Column(Integer, index=True)
    land_sq_ft = Column(Integer)
    property = relationship("Property", back_populates="property_features")


class MiscInfo(Base):
    __tablename__ = 'misc_info'
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    rec_type = Column(String)
    pin = Column(Integer)
    town = Column(Integer)
    volume = Column(Integer)
    loc = Column(String)
    tax_code = Column(Integer)
    neighborhood = Column(Integer)
    property = relationship("Property", back_populates="misc_info")

from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base import Base

from datetime import datetime


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    full_address = Column(String, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    zip = Column(Integer)
    rec_type = Column(String)
    pin = Column(Integer)
    ovacls = Column(Integer)
    class_description = Column(String)
    current_land = Column(Integer)
    current_building = Column(Integer)
    current_total = Column(Integer)
    estimated_market_value = Column(Integer)
    prior_land = Column(Integer)
    prior_building = Column(Integer)
    prior_total = Column(Integer)
    pprior_land = Column(Integer)
    pprior_building = Column(Integer)
    pprior_total = Column(Integer)
    pprior_year = Column(Integer)
    town = Column(Integer)
    volume = Column(Integer)
    loc = Column(String)
    tax_code = Column(Integer)
    neighborhood = Column(Integer)
    houseno = Column(Integer)
    dir = Column(String)
    street = Column(String)
    suffix = Column(String)
    apt = Column(String)
    city = Column(String)
    res_type = Column(String)
    bldg_use = Column(String)
    apt_desc = Column(Integer)
    comm_units = Column(Integer)
    ext_desc = Column(String)
    full_bath = Column(Integer)
    half_bath = Column(Integer)
    bsmt_desc = Column(String)
    attic_desc = Column(String)
    ac = Column(Integer)
    fireplace = Column(Integer)
    gar_desc = Column(String)
    age = Column(Integer)
    building_sq_ft = Column(Integer)
    land_sq_ft = Column(Integer)
    bldg_sf = Column(Integer)
    units_tot = Column(Integer)
    multi_sale = Column(Integer)
    deed_type = Column(Integer)
    sale_date = Column(Date)
    sale_amount = Column(Integer)
    appcnt = Column(Integer)
    appeal_a = Column(Integer)
    appeal_a_status = Column(String)
    appeal_a_result = Column(String)
    appeal_a_reason = Column(Integer)
    appeal_a_pin_result = Column(String)
    appeal_a_propav = Column(Integer)
    appeal_a_currav = Column(Integer)
    appeal_a_resltdate = Column(Date)

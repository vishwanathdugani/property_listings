from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from pydantic import create_model


class PropertyBase(BaseModel):
    full_address: str = Field(..., example="123 Main St, Anytown, USA")
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    zip: Optional[int] = None
    rec_type: Optional[str] = None
    pin: Optional[int] = None
    ovacls: Optional[int] = None
    class_description: str = Field(..., example="Residential")
    current_land: Optional[int] = None
    current_building: Optional[int] = None
    current_total: Optional[int] = None
    estimated_market_value: int = Field(..., example=100000)
    prior_land: Optional[int] = None
    prior_building: Optional[int] = None
    prior_total: Optional[int] = None
    pprior_land: Optional[int] = None
    pprior_building: Optional[int] = None
    pprior_total: Optional[int] = None
    pprior_year: Optional[int] = None
    town: Optional[int] = None
    volume: Optional[int] = None
    loc: Optional[str] = None
    tax_code: Optional[int] = None
    neighborhood: Optional[int] = None
    houseno: Optional[int] = None
    dir: Optional[str] = None
    street: Optional[str] = None
    suffix: Optional[str] = None
    apt: Optional[str] = None
    city: Optional[str] = None
    res_type: Optional[str] = None
    bldg_use: str = Field(..., example="Single Family")
    apt_desc: Optional[int] = None
    comm_units: Optional[int] = None
    ext_desc: Optional[str] = None
    full_bath: Optional[int] = None
    half_bath: Optional[int] = None
    bsmt_desc: Optional[str] = None
    attic_desc: Optional[str] = None
    ac: Optional[int] = None
    fireplace: Optional[int] = None
    gar_desc: Optional[str] = None
    age: Optional[int] = None
    building_sq_ft: int = Field(..., example=1200)
    land_sq_ft: Optional[int] = None
    bldg_sf: Optional[int] = None
    units_tot: Optional[int] = None
    multi_sale: Optional[int] = None
    deed_type: Optional[int] = None
    sale_date: Optional[datetime] = None
    sale_amount: Optional[int] = None
    appcnt: Optional[int] = None
    appeal_a: Optional[int] = None
    appeal_a_status: Optional[str] = None
    appeal_a_result: Optional[str] = None
    appeal_a_reason: Optional[int] = None
    appeal_a_pin_result: Optional[str] = None
    appeal_a_propav: Optional[int] = None
    appeal_a_currav: Optional[int] = None
    appeal_a_resltdate: Optional[datetime] = None

    @validator('full_address', 'class_description', 'loc', 'dir', 'street',
               'suffix', 'apt', 'city', 'res_type', 'bldg_use', 'ext_desc',
               'bsmt_desc', 'attic_desc', 'gar_desc', 'appeal_a_status',
               'appeal_a_result', 'appeal_a_pin_result', 'rec_type',
               pre=True, always=True)
    def strip_string(cls, v):
        if not isinstance(v, str):
            raise ValueError(f" must be a string")
        return str(v).strip()

    @validator('current_land', 'current_building', 'current_total',
               'estimated_market_value', 'prior_land', 'prior_building',
               'prior_total', 'pprior_land', 'pprior_building',
               'pprior_total', 'town', 'volume', 'tax_code', 'neighborhood',
               'houseno', 'apt_desc', 'comm_units', 'full_bath', 'half_bath',
               'ac', 'fireplace', 'age', 'building_sq_ft', 'land_sq_ft',
               'bldg_sf', 'units_tot', 'multi_sale', 'deed_type', 'pin',
               'sale_amount', 'appcnt', 'appeal_a', 'appeal_a_reason',
               'appeal_a_propav', 'appeal_a_currav', pre=True, always=True)
    def remove_periods_from_ints(cls, v):
        if v in [None, '', 'null']:
            return None
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            if v.strip().lower() in ['null', '']:
                return None
            return int(v)

    @validator('sale_date', 'appeal_a_resltdate', pre=True, always=True)
    def parse_dates(cls, v):
        if isinstance(v, str) and v.strip():
            return v
        return None

    @validator('longitude', 'latitude', pre=True)
    def replace_comma_with_dot(cls, v):
        if isinstance(v, str):
            return float(v.replace(',', '.'))
        return v


    @validator('pprior_year', pre=True, always=True)
    def parse_year(cls, v):
        if isinstance(v, int):
            # Check if it's a 4-digit year
            if 1000 <= v <= 9999:
                return str(v)
            else:
                # print(v)
                raise ValueError(f"Not a valid year: {v}")
        elif isinstance(v, str) and v.strip():
            try:
                return v
            except ValueError:
                # print(v)
                return None
        return v

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class PropertyCreate(PropertyBase):
    id: int


class PropertyUpdate(BaseModel):
    id: int


class PropertyListings(BaseModel):
    id : int
    full_address: str = Field(..., example="123 Main St, Anytown, USA")
    class_description: str = Field(..., example="Residential")
    estimated_market_value: int = Field(..., example=100000)
    bldg_use: str = Field(..., example="Single Family")
    building_sq_ft: int = Field(..., example=1200)
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    class Config:
        from_attributes = True


class PropertyResponse(BaseModel):
    id: int
    longitude: Optional[float]
    latitude: Optional[float]


class PropertyListing(BaseModel):
    id: int
    full_address: str = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    zip: Optional[int] = None
    rec_type: Optional[str] = None
    pin: Optional[int] = None
    ovacls: Optional[int] = None
    class_description: str = None
    current_land: Optional[int] = None
    current_building: Optional[int] = None
    current_total: Optional[int] = None
    estimated_market_value: int = None
    prior_land: Optional[int] = None
    prior_building: Optional[int] = None
    prior_total: Optional[int] = None
    pprior_land: Optional[int] = None
    pprior_building: Optional[int] = None
    pprior_total: Optional[int] = None
    pprior_year: Optional[int] = None
    town: Optional[int] = None
    volume: Optional[int] = None
    loc: Optional[str] = None
    tax_code: Optional[int] = None
    neighborhood: Optional[int] = None
    houseno: Optional[int] = None
    dir: Optional[str] = None
    street: Optional[str] = None
    suffix: Optional[str] = None
    apt: Optional[str] = None
    city: Optional[str] = None
    res_type: Optional[str] = None
    bldg_use: str = None
    apt_desc: Optional[int] = None
    comm_units: Optional[int] = None
    ext_desc: Optional[str] = None
    full_bath: Optional[int] = None
    half_bath: Optional[int] = None
    bsmt_desc: Optional[str] = None
    attic_desc: Optional[str] = None
    ac: Optional[int] = None
    fireplace: Optional[int] = None
    gar_desc: Optional[str] = None
    age: Optional[int] = None
    building_sq_ft: int = None
    land_sq_ft: Optional[int] = None
    bldg_sf: Optional[int] = None
    units_tot: Optional[int] = None
    multi_sale: Optional[int] = None
    deed_type: Optional[int] = None
    sale_date: Optional[datetime] = None
    sale_amount: Optional[int] = None
    appcnt: Optional[int] = None
    appeal_a: Optional[int] = None
    appeal_a_status: Optional[str] = None
    appeal_a_result: Optional[str] = None
    appeal_a_reason: Optional[int] = None
    appeal_a_pin_result: Optional[str] = None
    appeal_a_propav: Optional[int] = None
    appeal_a_currav: Optional[int] = None
    appeal_a_resltdate: Optional[datetime] = None


class PaginatedPropertyListingsResponse(BaseModel):
    properties: List[PropertyListings]
    moreExists: bool
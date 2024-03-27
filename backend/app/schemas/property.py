from pydantic import BaseModel
from typing import Optional, List


class PropertyQuerySchema(BaseModel):
    full_address: Optional[str] = None
    class_description: Optional[str] = None
    estimated_market_value_min: Optional[int] = None
    estimated_market_value_max: Optional[int] = None
    building_sq_ft_min: Optional[int] = None
    building_sq_ft_max: Optional[int] = None
    bldg_use: Optional[str] = None
    skip: int = 0
    limit: int = 5


class PropertyData(BaseModel):
    id: int
    full_address: str
    longitude: float
    latitude: float
    class_description: Optional[str]
    estimated_market_value: Optional[int]
    building_sq_ft: Optional[int]
    bldg_use: Optional[str]


class PaginatedPropertyResponse(BaseModel):
    data: List[PropertyData]
    more_exists: bool

class Range(BaseModel):
    min: int
    max: int

class SliderRangeResponse(BaseModel):
    estimated_market_value: Range
    building_sq_ft: Range


class PropertyCreateRequest(BaseModel):
    longitude: float
    latitude: float
    zip: str
    house_no: str
    dir: str
    street: str
    suffix: str
    apt: str
    city: str


class PropertyCreateResponse(BaseModel):
    id: int
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    zip: Optional[str] = None
    house_no: Optional[str] = None
    dir: Optional[str] = None
    street: Optional[str] = None
    suffix: Optional[str] = None
    apt: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True


class PropertyClassificationCreate(BaseModel):
    property_id: int = None
    ovac_ls: int
    class_description: str
    res_type: Optional[str] = None
    bldg_use: Optional[str] = None
    apt_desc: Optional[str] = None


class AssessmentCreate(BaseModel):
    property_id: int = None
    current_land: int = None
    current_building: int = None
    current_total: int = None
    estimated_market_value: int = None
    prior_land: Optional[int] = None
    prior_building: Optional[int] = None
    prior_total: Optional[int] = None


class SalesAppealCreate(BaseModel):
    property_id: Optional[int] = None
    multi_sale: Optional[bool] = None
    deed_type: Optional[int] = None
    sale_date: Optional[str] = None
    sale_amount: Optional[int] = None


class PropertyFeatureCreate(BaseModel):
    property_id: int
    comm_units: Optional[int] = None
    ext_desc: Optional[str] = None
    full_bath: Optional[int] = None
    half_bath: Optional[int] = None
    bsmnt_desc: Optional[str] = None
    attic_desc: Optional[str] = None
    ac: Optional[int] = None
    fireplace: Optional[int] = None
    gar_desc: Optional[str] = None
    age: Optional[int] = None
    building_sq_ft: Optional[int] = None
    land_sq_ft: Optional[int] = None


class MiscInfoCreate(BaseModel):
    property_id: int
    rec_type: Optional[str] = None
    pin: Optional[int] = None
    town: Optional[int] = None
    volume: Optional[int] = None
    loc: Optional[str] = None
    tax_code: Optional[int] = None
    neighborhood: Optional[int] = None


class PropertyDetailResponse(BaseModel):
    id: int
    longitude: Optional[float]
    latitude: Optional[float]
    zip: Optional[str]
    house_no: str
    dir: Optional[str]
    street: str
    suffix: Optional[str]
    apt: Optional[str]
    city: str
    class_description: Optional[str]
    ovac_ls: Optional[int]
    res_type: Optional[str]
    bldg_use: Optional[str]
    apt_desc: Optional[str]
    current_land: Optional[int]
    current_building: Optional[int]
    current_total: Optional[int]
    estimated_market_value: Optional[int]
    prior_land: Optional[int]
    prior_building: Optional[int]
    prior_total: Optional[int]
    multi_sale: Optional[bool]
    deed_type: Optional[int]
    sale_date: Optional[str]  # ISO format
    sale_amount: Optional[int]
    comm_units: Optional[int]
    ext_desc: Optional[str]
    full_bath: Optional[int]
    half_bath: Optional[int]
    bsmnt_desc: Optional[str]
    attic_desc: Optional[str]
    ac: Optional[int]
    fireplace: Optional[int]
    gar_desc: Optional[str]
    age: Optional[int]
    building_sq_ft: Optional[int]
    land_sq_ft: Optional[int]
    rec_type: Optional[str]
    pin: Optional[int]
    town: Optional[int]
    volume: Optional[int]
    loc: Optional[str]
    tax_code: Optional[int]
    neighborhood: Optional[int]

    class Config:
        from_attributes = True
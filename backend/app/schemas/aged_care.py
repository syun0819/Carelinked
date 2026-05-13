from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class FacilityCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    service_name: Optional[str] = None
    physical_address: Optional[str] = None
    physical_suburb: Optional[str] = None
    physical_state: Optional[str] = None
    physical_post_code: Optional[str] = None
    aged_care_planning_region: Optional[str] = None
    care_type: Optional[str] = None
    residential_places: Optional[int] = None
    provider_name: Optional[str] = None
    abs_remoteness: Optional[str] = None
    availability_group: Optional[str] = None
    data_source: Optional[str] = None
    distance_km: Optional[float] = None
    match_score: Optional[float] = None
    match_category: Optional[str] = None


class FacilityDetail(FacilityCard):
    home_care_places: Optional[int] = None
    restorative_care_places: Optional[int] = None
    organisation_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    australian_government_funding: Optional[float] = None
    overall_star_rating: Optional[int] = None
    residents_experience_rating: Optional[int] = None
    compliance_rating: Optional[int] = None
    staffing_rating: Optional[int] = None
    quality_measures_rating: Optional[int] = None
    re_food_score: Optional[float] = None
    re_safety_score: Optional[float] = None
    re_respect_score: Optional[float] = None
    re_caring_score: Optional[float] = None
    re_home_score: Optional[float] = None
    re_voice_score: Optional[float] = None
    re_explain_score: Optional[float] = None
    re_follow_up_score: Optional[float] = None
    re_independent_score: Optional[float] = None
    re_competent_score: Optional[float] = None
    re_care_need_score: Optional[float] = None
    re_operation_score: Optional[float] = None
    s_rn_care_minutes_target: Optional[float] = None
    s_rn_care_minutes_actual: Optional[float] = None
    s_total_care_minutes_target: Optional[float] = None
    s_total_care_minutes_actual: Optional[float] = None
    rn_minutes_met: Optional[bool] = None
    total_minutes_met: Optional[bool] = None


class FacilitySearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    results: List[FacilityCard]
    message: Optional[str] = None


class FacilityMapMarker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    service_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    care_type: Optional[str] = None
    residential_places: Optional[int] = None
    availability_group: str
    data_source: str
    provider_name: Optional[str] = None
    physical_suburb: Optional[str] = None
    physical_post_code: Optional[str] = None


class FacilityMapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    results: List[FacilityMapMarker]
    message: Optional[str] = None


class FacilityAutoComplete(BaseModel):
    id: str
    name: str
    type: str = "facility"
    suburb: Optional[str] = None
    state: Optional[str] = None


class SuburbAutoComplete(BaseModel):
    name: str
    postcode: str
    type: str = "suburb"


class PostcodeAutoComplete(BaseModel):
    postcode: str
    suburb: str
    type: str = "postcode"


class AutoCompleteResponse(BaseModel):
    facilities: List[FacilityAutoComplete] = []
    suburbs: List[SuburbAutoComplete] = []
    postcodes: List[PostcodeAutoComplete] = []

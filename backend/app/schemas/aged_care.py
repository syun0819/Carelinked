from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class FacilityCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    service_name: Optional[str] = None
    physical_address: Optional[str] = None
    physical_suburb: Optional[str] = None
    physical_post_code: Optional[str] = None
    aged_care_planning_region: Optional[str] = None
    care_type: Optional[str] = None
    residential_places: Optional[int] = None
    provider_name: Optional[str] = None
    abs_remoteness: Optional[str] = None


class FacilityDetail(FacilityCard):
    home_care_places: Optional[int] = None
    restorative_care_places: Optional[int] = None
    organisation_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    australian_government_funding: Optional[float] = None


class FacilitySearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    results: List[FacilityCard]


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

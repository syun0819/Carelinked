from typing import Optional
from pydantic import BaseModel


class WaitTimeEstimateRequest(BaseModel):
    priority_level: str
    age: str
    assessment_location: str
    dementia_status: str
    living_arrangement: str
    sex: Optional[str] = None
    first_nations_status: Optional[str] = None
    cald_status: Optional[str] = None
    country_of_birth: Optional[str] = None
    aged_care_service_use: Optional[str] = None
    caring_arrangement: Optional[str] = None
    mental_health_status: Optional[str] = None
    morbidity: Optional[str] = None
    remoteness: Optional[str] = None


class WaitTimeEstimateResponse(BaseModel):
    combined_ratio: float
    outcome: str
    outcome_label: str
    inputs_used: dict

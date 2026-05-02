from typing import Optional, Literal
from pydantic import BaseModel


class WaitTimeEstimateRequest(BaseModel):
    priority_level: Optional[Literal["Low", "Medium", "High"]] = None
    age: Optional[Literal["50–69", "70–79", "80–89", "90+"]] = None
    assessment_location: Optional[Literal[
        "Assessed outside hospital",
        "Assessed in hospital"
    ]] = None
    dementia_status: Optional[Literal["No dementia", "Dementia"]] = None
    living_arrangement: Optional[Literal[
        "Does not live alone",
        "Lives alone"
    ]] = None
    sex: Optional[Literal["Men", "Women"]] = None
    first_nations_status: Optional[Literal[
        "Non-Indigenous",
        "First Nations"
    ]] = None
    cald_status: Optional[Literal["Non-CALD", "CALD"]] = None
    country_of_birth: Optional[Literal[
        "Born in Australia",
        "Born overseas"
    ]] = None
    aged_care_service_use: Optional[Literal[
        "Has not previously used aged care services",
        "Has previously used aged care services"
    ]] = None
    caring_arrangement: Optional[Literal[
        "Does not have an informal carer",
        "Has an informal carer"
    ]] = None
    mental_health_status: Optional[Literal[
        "Does not have a mental health condition",
        "Has a mental health condition"
    ]] = None
    morbidity: Optional[Literal[
        "Having no or 1 health conditions",
        "Having 2–3 health conditions",
        "Having 4–5 health conditions",
        "Having 6 health conditions or more"
    ]] = None
    remoteness: Optional[Literal[
        "Metropolitan (MM 1)",
        "Regional centres (MM 2)",
        "Rural and remote (MM 3–7)"
    ]] = None


class WaitTimeEstimateResponse(BaseModel):
    combined_ratio: float
    outcome: str
    outcome_label: str
    inputs_used: dict

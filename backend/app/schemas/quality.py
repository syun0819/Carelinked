from typing import Optional
from pydantic import BaseModel


class QualityRating(BaseModel):
    facility_id: str
    service_name: str
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

    model_config = {"from_attributes": True}


class QualityCompareResponse(BaseModel):
    results: list[QualityRating]

from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class StarRating(Base):
    __tablename__ = "star_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    reporting_period = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)
    service_suburb = Column(String)
    state_territory = Column(String)
    overall_star_rating = Column(Integer)
    residents_experience_rating = Column(Integer)
    compliance_rating = Column(Integer)
    staffing_rating = Column(Integer)
    quality_measures_rating = Column(Integer)
    re_food_score = Column(Numeric(3, 2))
    re_safety_score = Column(Numeric(3, 2))
    re_operation_score = Column(Numeric(3, 2))
    re_care_need_score = Column(Numeric(3, 2))
    re_competent_score = Column(Numeric(3, 2))
    re_independent_score = Column(Numeric(3, 2))
    re_explain_score = Column(Numeric(3, 2))
    re_respect_score = Column(Numeric(3, 2))
    re_follow_up_score = Column(Numeric(3, 2))
    re_caring_score = Column(Numeric(3, 2))
    re_voice_score = Column(Numeric(3, 2))
    re_home_score = Column(Numeric(3, 2))
    s_rn_care_minutes_target = Column(Numeric(6, 2))
    s_rn_care_minutes_actual = Column(Numeric(6, 2))
    s_total_care_minutes_target = Column(Numeric(6, 2))
    s_total_care_minutes_actual = Column(Numeric(6, 2))

import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class WaitTimeRatio(Base):
    __tablename__ = "aged_care_timeliness_prac"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)
    value = Column(String, nullable=False)
    event_rate_ratio = Column(Float, nullable=True)
    lower_ci = Column(Float, nullable=True)
    upper_ci = Column(Float, nullable=True)
    is_reference = Column(Boolean, nullable=False)

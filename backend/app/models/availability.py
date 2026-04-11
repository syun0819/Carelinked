from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class FacilityAvailabilityML(Base):
    __tablename__ = "aged_care_facility_availability"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    facility_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), nullable=False)
    residential_label_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    residential_label_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    home_care_label_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    home_care_label_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    restorative_care_label_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    restorative_care_label_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

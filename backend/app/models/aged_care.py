from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Float, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AgedCareService(Base):
    __tablename__ = "aged_care_services"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    service_name: Mapped[str] = mapped_column(String)
    physical_address: Mapped[str] = mapped_column(String)
    physical_suburb: Mapped[str] = mapped_column(String)
    physical_state: Mapped[str] = mapped_column(String)
    physical_post_code: Mapped[str] = mapped_column(String)
    aged_care_planning_region: Mapped[Optional[str]] = mapped_column(
        "aged_care_planning_region_acpr_2018", String, nullable=True
    )
    care_type: Mapped[str] = mapped_column(String)
    residential_places: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    home_care_places: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    restorative_care_places: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    provider_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    organisation_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    abs_remoteness: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    australian_government_funding: Mapped[Optional[float]] = mapped_column(
        "australian_government_funding_2024_25", Float, nullable=True
    )
    lga_name: Mapped[Optional[str]] = mapped_column("lga_name_2023", String, nullable=True)
    lga_code: Mapped[Optional[str]] = mapped_column("lga_code_2023", String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
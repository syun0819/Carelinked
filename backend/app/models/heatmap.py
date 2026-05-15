from typing import Optional

from sqlalchemy import String, Integer, Float, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base



class ResidentialCareDemandByLga(Base):
    __tablename__ = "residential_care_demand_by_service_lga"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    lga_code: Mapped[str] = mapped_column(String)
    lga_name: Mapped[str] = mapped_column(String)
    admission_type: Mapped[str] = mapped_column(String)
    people_count: Mapped[int] = mapped_column(Integer)


class BushfireExtent(Base):
    __tablename__ = "bushfire_extents"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    fire_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fire_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ignition_date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    area_ha: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    perim_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    agency: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    centroid_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    centroid_lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class BushfireLgaSummary(Base):
    __tablename__ = "bushfire_lga_summary"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    lga_code: Mapped[str] = mapped_column(String)
    lga_name: Mapped[str] = mapped_column(String)
    state_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bushfire_count: Mapped[int] = mapped_column(Integer)


class LgaBoundary(Base):
    __tablename__ = "lga_boundaries"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    lga_code: Mapped[str] = mapped_column(String)
    lga_name: Mapped[str] = mapped_column(String)
    state_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    geom_wkt: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class CrimeRateLga(Base):
    __tablename__ = "crime_rate_lga"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True)
    lga_name: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    offence: Mapped[str] = mapped_column(String)
    adjusted_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    frequency: Mapped[str] = mapped_column(String)
    measure: Mapped[str] = mapped_column(String)
    region_type: Mapped[str] = mapped_column(String)
    offence_type: Mapped[str] = mapped_column(String)

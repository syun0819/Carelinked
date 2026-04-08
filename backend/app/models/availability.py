from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AvailabilityGroup(Base):
    __tablename__ = "availability_groups"

    availability_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    availability_group_display_name: Mapped[str] = mapped_column(String)


class FacilityAvailability(Base):
    __tablename__ = "facility_availability"

    facility_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("availability_groups.availability_group_id"),
        primary_key=True,
    )
    availability_group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("availability_groups.availability_group_id"),
    )

from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LocationGeo(Base):
    __tablename__ = "location_geo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    postcode: Mapped[str] = mapped_column(String)
    suburb: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.location import LocationGeo


async def fetch_facilities_by_name(db: AsyncSession, q: str, limit: int) -> List:
    result = await db.execute(
        select(AgedCareService.id, AgedCareService.service_name,
               AgedCareService.physical_suburb, AgedCareService.physical_state)
        .where(AgedCareService.service_name.ilike(f"%{q}%"))
        .order_by(AgedCareService.service_name)
        .limit(limit)
    )
    return list(result.all())


async def fetch_suburbs_by_name(db: AsyncSession, q: str, limit: int) -> List:
    result = await db.execute(
        select(LocationGeo.suburb, LocationGeo.postcode)
        .where(LocationGeo.suburb.ilike(f"%{q}%"))
        .distinct(LocationGeo.suburb)
        .order_by(LocationGeo.suburb)
        .limit(limit)
    )
    return list(result.all())


async def fetch_suburbs_by_postcode(db: AsyncSession, q: str, limit: int) -> List:
    result = await db.execute(
        select(LocationGeo.postcode, LocationGeo.suburb)
        .where(LocationGeo.postcode.like(f"{q}%"))
        .distinct(LocationGeo.postcode)
        .order_by(LocationGeo.postcode)
        .limit(limit)
    )
    return list(result.all())

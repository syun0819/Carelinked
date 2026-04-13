from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aged_care import AgedCareService
from app.models.location import LocationGeo
from app.schemas.aged_care import (
    AutoCompleteResponse,
    FacilityAutoComplete,
    PostcodeAutoComplete,
    SuburbAutoComplete,
)


async def get_autocomplete(db: AsyncSession, q: str) -> AutoCompleteResponse:
    if len(q.strip()) < 2:
        return AutoCompleteResponse()

    is_numeric = q.strip().isdigit()

    facilities: list[FacilityAutoComplete] = []
    suburbs: list[SuburbAutoComplete] = []
    postcodes: list[PostcodeAutoComplete] = []

    if not is_numeric:
        # Facility search
        fac_result = await db.execute(
            select(AgedCareService.id, AgedCareService.service_name)
            .where(AgedCareService.physical_state == "VIC")
            .where(AgedCareService.service_name.ilike(f"%{q}%"))
            .order_by(AgedCareService.service_name)
            .limit(3)
        )
        facilities = [
            FacilityAutoComplete(id=str(row.id), name=row.service_name)
            for row in fac_result
        ]

        # Suburb search
        sub_result = await db.execute(
            select(LocationGeo.suburb, LocationGeo.postcode)
            .where(LocationGeo.state == "VIC")
            .where(LocationGeo.suburb.ilike(f"%{q}%"))
            .distinct(LocationGeo.suburb)
            .order_by(LocationGeo.suburb)
            .limit(3)
        )
        suburbs = [
            SuburbAutoComplete(name=row.suburb, postcode=row.postcode)
            for row in sub_result
        ]
    else:
        # Postcode search
        pc_result = await db.execute(
            select(LocationGeo.postcode, LocationGeo.suburb)
            .where(LocationGeo.state == "VIC")
            .where(LocationGeo.postcode.like(f"{q}%"))
            .distinct(LocationGeo.postcode)
            .order_by(LocationGeo.postcode)
            .limit(3)
        )
        postcodes = [
            PostcodeAutoComplete(postcode=row.postcode, suburb=row.suburb)
            for row in pc_result
        ]

    return AutoCompleteResponse(facilities=facilities, suburbs=suburbs, postcodes=postcodes)

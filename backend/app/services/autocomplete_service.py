from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import autocomplete_repository as autocomplete_repo
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
        fac_rows = await autocomplete_repo.fetch_facilities_by_name(db, q, limit=3)
        facilities = [
            FacilityAutoComplete(
                id=str(row.id),
                name=row.service_name,
                suburb=row.physical_suburb,
                state=row.physical_state,
            )
            for row in fac_rows
        ]

        sub_rows = await autocomplete_repo.fetch_suburbs_by_name(db, q, limit=3)
        suburbs = [
            SuburbAutoComplete(name=row.suburb, postcode=row.postcode)
            for row in sub_rows
        ]
    else:
        pc_rows = await autocomplete_repo.fetch_suburbs_by_postcode(db, q, limit=3)
        postcodes = [
            PostcodeAutoComplete(postcode=row.postcode, suburb=row.suburb)
            for row in pc_rows
        ]

    return AutoCompleteResponse(facilities=facilities, suburbs=suburbs, postcodes=postcodes)

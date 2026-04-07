from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.aged_care import FacilityCard, FacilityDetail, FacilitySearchResponse
from app.services.facility_service import search_facilities, get_facility_by_id

router = APIRouter(prefix="/api/v1/facilities", tags=["facilities"])


@router.get("/search", response_model=FacilitySearchResponse)
async def search(
    suburb: Optional[str] = Query(None),
    postcode: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    care_type: Optional[str] = Query(None),
    abs_remoteness: Optional[str] = Query(None),
    min_beds: Optional[int] = Query(None),
    max_beds: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    if not suburb and not postcode and not region:
        raise HTTPException(
            status_code=400,
            detail="At least one of suburb, postcode, or region is required.",
        )

    results, total = await search_facilities(
        db=db,
        suburb=suburb,
        postcode=postcode,
        region=region,
        care_type=care_type,
        abs_remoteness=abs_remoteness,
        min_beds=min_beds,
        max_beds=max_beds,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
    )

    return FacilitySearchResponse(
        total=total,
        results=[FacilityCard.model_validate(r) for r in results],
    )


@router.get("/{facility_id}", response_model=FacilityDetail)
async def get_facility(
    facility_id: str,
    db: AsyncSession = Depends(get_db),
):
    facility = await get_facility_by_id(db, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return FacilityDetail.model_validate(facility)

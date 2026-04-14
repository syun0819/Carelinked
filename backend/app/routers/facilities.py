from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.aged_care import FacilityCard, FacilityDetail, FacilityMapResponse, FacilitySearchResponse
from app.services.facility_service import (
    get_facilities_for_map,
    get_facility_by_id,
    get_nearest_facilities,
    get_recommended_facilities,
    get_similar_facilities,
    search_facilities,
)
from app.services import location_service

router = APIRouter(prefix="/api/v1/facilities", tags=["facilities"])


@router.get("/search", response_model=FacilitySearchResponse)
async def search(
    suburb: Optional[str] = Query(None),
    postcode: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    care_type: Optional[List[str]] = Query(default=None),
    abs_remoteness: Optional[str] = Query(None),
    min_beds: Optional[int] = Query(None),
    max_beds: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    max_distance_km: Optional[float] = Query(None),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    results, total = await search_facilities(
        db=db,
        suburb=suburb,
        postcode=postcode,
        region=region,
        keyword=keyword,
        care_type=care_type,
        abs_remoteness=abs_remoteness,
        min_beds=min_beds,
        max_beds=max_beds,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
        max_distance_km=max_distance_km,
        user_lat=user_lat,
        user_lng=user_lng,
    )

    cards = []
    for r in results:
        card = FacilityCard.model_validate(r)
        card.availability_group = getattr(r, "_availability_group", None)
        card.data_source = getattr(r, "_data_source", None)
        cards.append(card)
    return FacilitySearchResponse(total=total, results=cards)


@router.get("/recommended", response_model=FacilitySearchResponse)
async def recommended(
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None),
    limit: int = Query(6, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if user_lat is not None and user_lng is not None:
        results = await get_nearest_facilities(db, user_lat, user_lng, limit=limit)
    else:
        results = await get_recommended_facilities(db)
    return FacilitySearchResponse(total=len(results), results=results)


@router.get("/map", response_model=FacilityMapResponse)
async def get_map(
    suburb: Optional[str] = Query(None),
    postcode: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    care_type: Optional[List[str]] = Query(default=None),
    max_distance_km: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    if not suburb and not postcode and not region:
        raise HTTPException(
            status_code=400,
            detail="At least one of suburb, postcode, or region is required.",
        )

    center_lat, center_lng = None, None
    if max_distance_km is not None:
        center_lat, center_lng = await location_service.get_location_center(
            db=db, suburb=suburb, postcode=postcode
        )
        if center_lat is None or center_lng is None:
            raise HTTPException(
                status_code=400,
                detail="Could not find location coordinates for the given suburb/postcode",
            )

    results, total = await get_facilities_for_map(
        db=db,
        suburb=suburb,
        postcode=postcode,
        region=region,
        care_type=care_type,
        max_distance_km=max_distance_km,
        center_lat=center_lat,
        center_lng=center_lng,
    )

    message = None
    if total == 0:
        message = (
            "No facilities found for your selected filters. "
            "Try broadening your search area or changing the care type."
        )

    return FacilityMapResponse(total=total, results=results, message=message)


@router.get("/{facility_id}/similar", response_model=FacilitySearchResponse)
async def similar(
    facility_id: str,
    limit: int = Query(4, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    target = await get_facility_by_id(db, facility_id)
    if not target:
        raise HTTPException(status_code=404, detail="Facility not found.")
    results = await get_similar_facilities(db, facility_id, limit=limit)
    return FacilitySearchResponse(total=len(results), results=results)


@router.get("/{facility_id}", response_model=FacilityDetail)
async def get_facility(
    facility_id: str,
    db: AsyncSession = Depends(get_db),
):
    facility = await get_facility_by_id(db, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return FacilityDetail.model_validate(facility)

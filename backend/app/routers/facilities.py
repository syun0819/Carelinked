import re
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.aged_care import FacilityCard, FacilityDetail, FacilityMapResponse, FacilitySearchResponse
from app.services.facility_service import (
    get_facilities_for_map,
    get_facility_by_id,
    get_recommended_facilities,
    get_similar_facilities,
    search_facilities,
)
from app.services import location_service

router = APIRouter(prefix="/api/v1/facilities", tags=["facilities"])

VALID_SORT_OPTIONS = {"name", "beds_desc", "beds_asc", "distance"}
VALID_REMOTENESS = {"Major Cities", "Inner Regional", "Outer Regional", "Remote", "Very Remote"}
VALID_CARE_TYPES = {
    "Residential",
    "Transition Care",
    "Short-Term Restorative Care (STRC)",
    "Multi-Purpose Service",
    "National Aboriginal and Torres Strait Islander Aged Care Program",
}

def validate_text_input(value: Optional[str], field_name: str, max_length: int = 100) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    if len(value) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"{field_name} must not exceed {max_length} characters."
        )
    if re.search(r"['\";\\<>]", value):
        raise HTTPException(
            status_code=400,
            detail=f"{field_name} contains invalid characters."
        )
    return value

def validate_postcode(postcode: Optional[str]) -> Optional[str]:
    if postcode is None:
        return None
    postcode = postcode.strip()
    if not re.fullmatch(r"\d{4}", postcode):
        raise HTTPException(
            status_code=400,
            detail="Postcode must be exactly 4 digits."
        )
    return postcode


@router.get("/search", response_model=FacilitySearchResponse)
@limiter.limit("30/minute")
async def search(
    request: Request,
    suburb: Optional[str] = Query(None),
    postcode: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    care_type: Optional[List[str]] = Query(default=None),
    abs_remoteness: Optional[str] = Query(None),
    min_beds: Optional[int] = Query(None, ge=0, le=999),
    max_beds: Optional[int] = Query(None, ge=0, le=999),
    sort_by: Optional[str] = Query("name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    max_distance_km: Optional[float] = Query(None, ge=0, le=500),
    user_lat: Optional[float] = Query(None, ge=-90, le=90),
    user_lng: Optional[float] = Query(None, ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
):
    suburb = validate_text_input(suburb, "Suburb")
    region = validate_text_input(region, "Region")
    keyword = validate_text_input(keyword, "Keyword")
    postcode = validate_postcode(postcode)

    if sort_by == "closest":
        sort_by = "distance"

    if sort_by and sort_by not in VALID_SORT_OPTIONS:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of: {', '.join(VALID_SORT_OPTIONS)}")

    if abs_remoteness and abs_remoteness not in VALID_REMOTENESS:
        raise HTTPException(status_code=400, detail=f"Invalid remoteness value.")

    if care_type:
        for ct in care_type:
            if ct not in VALID_CARE_TYPES:
                raise HTTPException(status_code=400, detail=f"Invalid care type: {ct}")

    if min_beds is not None and max_beds is not None and min_beds > max_beds:
        raise HTTPException(status_code=400, detail="min_beds cannot be greater than max_beds.")

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

    message = None
    if total == 0:
        if care_type and (suburb or postcode or keyword):
            message = "No facilities found in this area for the selected care type. Try changing the care type or broadening your search."
        elif suburb or postcode:
            message = "No facilities found in this area. Try a different suburb or postcode."
        elif keyword:
            message = f"No facilities found matching '{keyword}'. Try a different name or search by suburb."
        else:
            message = "No facilities found. Try adjusting your search criteria."

    return FacilitySearchResponse(total=total, results=cards, message=message)


@router.get("/recommended", response_model=FacilitySearchResponse)
@limiter.limit("30/minute")
@cache(expire=600)
async def recommended(
    request: Request,
    user_lat: Optional[float] = Query(None, ge=-90, le=90),
    user_lng: Optional[float] = Query(None, ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
):
    results = await get_recommended_facilities(db, user_lat=user_lat, user_lng=user_lng)
    return FacilitySearchResponse(total=len(results), results=results)


@router.get("/map", response_model=FacilityMapResponse)
@limiter.limit("30/minute")
@cache(expire=300)
async def get_map(
    request: Request,
    suburb: Optional[str] = Query(None),
    postcode: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    care_type: Optional[List[str]] = Query(default=None),
    max_distance_km: Optional[float] = Query(None, ge=0, le=500),
    db: AsyncSession = Depends(get_db),
):
    suburb = validate_text_input(suburb, "Suburb")
    region = validate_text_input(region, "Region")
    postcode = validate_postcode(postcode)

    if care_type:
        for ct in care_type:
            if ct not in VALID_CARE_TYPES:
                raise HTTPException(status_code=400, detail=f"Invalid care type: {ct}")

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
@limiter.limit("30/minute")
@cache(expire=600)
async def similar(
    request: Request,
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
@limiter.limit("60/minute")
@cache(expire=600)
async def get_facility(
    request: Request,
    facility_id: str,
    db: AsyncSession = Depends(get_db),
):
    facility = await get_facility_by_id(db, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return FacilityDetail.model_validate(facility)

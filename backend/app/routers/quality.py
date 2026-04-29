import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.quality import QualityRating, QualityCompareResponse
from app.services.quality_service import get_quality_by_facility_ids

def validate_facility_id(facility_id: str) -> str:
    if not re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        facility_id.lower()
    ):
        raise HTTPException(status_code=400, detail="Invalid facility ID format.")
    return facility_id

router = APIRouter(prefix="/api/v1/quality", tags=["quality"])


def build_quality_rating(row, facility_id: str) -> QualityRating:
    rn_met = None
    total_met = None
    if row.s_rn_care_minutes_actual is not None and row.s_rn_care_minutes_target is not None:
        rn_met = float(row.s_rn_care_minutes_actual) >= float(row.s_rn_care_minutes_target)
    if row.s_total_care_minutes_actual is not None and row.s_total_care_minutes_target is not None:
        total_met = float(row.s_total_care_minutes_actual) >= float(row.s_total_care_minutes_target)

    return QualityRating(
        facility_id=facility_id,
        service_name=row.service_name or "",
        overall_star_rating=row.overall_star_rating,
        residents_experience_rating=row.residents_experience_rating,
        compliance_rating=row.compliance_rating,
        staffing_rating=row.staffing_rating,
        quality_measures_rating=row.quality_measures_rating,
        re_food_score=float(row.re_food_score) if row.re_food_score else None,
        re_safety_score=float(row.re_safety_score) if row.re_safety_score else None,
        re_respect_score=float(row.re_respect_score) if row.re_respect_score else None,
        re_caring_score=float(row.re_caring_score) if row.re_caring_score else None,
        re_home_score=float(row.re_home_score) if row.re_home_score else None,
        re_voice_score=float(row.re_voice_score) if row.re_voice_score else None,
        re_explain_score=float(row.re_explain_score) if row.re_explain_score else None,
        re_follow_up_score=float(row.re_follow_up_score) if row.re_follow_up_score else None,
        re_independent_score=float(row.re_independent_score) if row.re_independent_score else None,
        re_competent_score=float(row.re_competent_score) if row.re_competent_score else None,
        re_care_need_score=float(row.re_care_need_score) if row.re_care_need_score else None,
        re_operation_score=float(row.re_operation_score) if row.re_operation_score else None,
        s_rn_care_minutes_target=float(row.s_rn_care_minutes_target) if row.s_rn_care_minutes_target else None,
        s_rn_care_minutes_actual=float(row.s_rn_care_minutes_actual) if row.s_rn_care_minutes_actual else None,
        s_total_care_minutes_target=float(row.s_total_care_minutes_target) if row.s_total_care_minutes_target else None,
        s_total_care_minutes_actual=float(row.s_total_care_minutes_actual) if row.s_total_care_minutes_actual else None,
        rn_minutes_met=rn_met,
        total_minutes_met=total_met,
    )


@router.get("/compare", response_model=QualityCompareResponse)
@limiter.limit("30/minute")
async def compare_quality(
    request: Request,
    facility_ids: List[str] = Query(...),
    db: AsyncSession = Depends(get_db),
):
    for fid in facility_ids:
        if not re.fullmatch(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            fid.lower()
        ):
            raise HTTPException(status_code=400, detail="Invalid facility ID format.")
    if len(facility_ids) < 2 or len(facility_ids) > 3:
        raise HTTPException(status_code=400, detail="Please provide 2 or 3 facility_ids.")
    rows = await get_quality_by_facility_ids(db, facility_ids)
    row_map = {str(row.service_id): row for row in rows}
    results = []
    for fid in facility_ids:
        if fid in row_map:
            results.append(build_quality_rating(row_map[fid], fid))
    return QualityCompareResponse(results=results)

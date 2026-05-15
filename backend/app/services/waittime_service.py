from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import waittime_repository as waittime_repo
from app.schemas.waittime import WaitTimeEstimateRequest, WaitTimeEstimateResponse

CATEGORY_FIELD_MAP = {
    "Priority level": "priority_level",
    "Age": "age",
    "Assessment location": "assessment_location",
    "Dementia status": "dementia_status",
    "Living arrangement": "living_arrangement",
    "Sex": "sex",
    "First Nations status": "first_nations_status",
    "Culturally and linguistically diverse (CALD)": "cald_status",
    "Country of birth": "country_of_birth",
    "Aged care service use": "aged_care_service_use",
    "Caring arrangement": "caring_arrangement",
    "Mental health status": "mental_health_status",
    "Morbidity": "morbidity",
    "Remoteness (MMM)": "remoteness",
}


def _normalize_value(value: str) -> str:
    """Replace ASCII hyphen-minus with en-dash to match DB values (e.g. '80-89' → '80–89')."""
    return value.replace("-", "–")


async def estimate_wait_time(
    db: AsyncSession,
    request: WaitTimeEstimateRequest,
) -> WaitTimeEstimateResponse:
    field_to_value = {
        "priority_level": request.priority_level,
        "age": request.age,
        "assessment_location": request.assessment_location,
        "dementia_status": request.dementia_status,
        "living_arrangement": request.living_arrangement,
        "sex": request.sex,
        "first_nations_status": request.first_nations_status,
        "cald_status": request.cald_status,
        "country_of_birth": request.country_of_birth,
        "aged_care_service_use": request.aged_care_service_use,
        "caring_arrangement": request.caring_arrangement,
        "mental_health_status": request.mental_health_status,
        "morbidity": request.morbidity,
        "remoteness": request.remoteness,
    }

    all_rows = await waittime_repo.fetch_all_ratios(db)

    lookup: Dict[str, Dict[str, float]] = {}
    for row in all_rows:
        if row.category not in lookup:
            lookup[row.category] = {}
        ratio = row.event_rate_ratio if row.event_rate_ratio is not None else 1.0
        lookup[row.category][row.value] = ratio

    combined_ratio = 1.0
    inputs_used = {}

    for category, field_name in CATEGORY_FIELD_MAP.items():
        user_value = field_to_value.get(field_name)
        if user_value is None:
            inputs_used[field_name] = {"value": "not provided", "ratio": 1.0}
            continue

        normalized = _normalize_value(user_value)
        cat_lookup = lookup.get(category, {})
        matched_value = user_value if user_value in cat_lookup else normalized if normalized in cat_lookup else None

        if matched_value is not None:
            ratio = cat_lookup[matched_value]
            combined_ratio *= ratio
            inputs_used[field_name] = {"value": user_value, "ratio": ratio}
        else:
            inputs_used[field_name] = {"value": user_value, "ratio": 1.0}

    if combined_ratio >= 1.2:
        outcome = "less_than_median"
        outcome_label = "Your estimated wait time is likely less than the median (6 months)."
    elif combined_ratio <= 0.8:
        outcome = "more_than_median"
        outcome_label = "Your estimated wait time is likely more than the median (6 months)."
    else:
        outcome = "around_median"
        outcome_label = "Your estimated wait time is likely around the median (6 months)."

    return WaitTimeEstimateResponse(
        combined_ratio=round(combined_ratio, 3),
        outcome=outcome,
        outcome_label=outcome_label,
        inputs_used=inputs_used,
    )

from decimal import Decimal, ROUND_FLOOR
from typing import Mapping, Optional


MATCH_FIELD_MAP = {
    "food_points": "re_food_score",
    "safety_points": "re_safety_score",
    "respect_points": "re_respect_score",
    "caring_points": "re_caring_score",
    "home_points": "re_home_score",
    "staffing_points": "staffing_rating",
    "compliance_points": "compliance_rating",
    "clinical_quality_points": "quality_measures_rating",
}

NOT_ENOUGH_DATA = "Not enough data"
STRONG_MATCH = "Strong Match"
MODERATE_MATCH = "Moderate Match"
LOWER_MATCH = "Lower Match"


def normalize_match_weights(weights: Optional[Mapping[str, Optional[int]]]) -> dict[str, int]:
    if not weights:
        return {}
    return {
        key: int(value or 0)
        for key, value in weights.items()
        if key in MATCH_FIELD_MAP and int(value or 0) > 0
    }


def is_matching_active(weights: Optional[Mapping[str, Optional[int]]]) -> bool:
    return sum(normalize_match_weights(weights).values()) == 100


def get_match_category(score: Optional[float]) -> str:
    if score is None:
        return NOT_ENOUGH_DATA
    if score >= 75:
        return STRONG_MATCH
    if score >= 50:
        return MODERATE_MATCH
    return LOWER_MATCH


def calculate_match_score(star_rating_row, weights: Mapping[str, int]) -> Optional[float]:
    normalized_weights = normalize_match_weights(weights)
    weighted_score = Decimal("0")
    denominator = Decimal("0")

    for weight_key, rating_field in MATCH_FIELD_MAP.items():
        points = normalized_weights.get(weight_key, 0)
        if points <= 0:
            continue

        rating = getattr(star_rating_row, rating_field, None) if star_rating_row is not None else None
        if rating is None:
            return None

        rating_value = Decimal(str(rating))
        rating_value = max(Decimal("0"), min(Decimal("5"), rating_value))
        point_value = Decimal(points)

        weighted_score += point_value * rating_value
        denominator += point_value * Decimal("5")

    if denominator == 0:
        return None

    score = (weighted_score / denominator) * Decimal("100")
    return float(score.quantize(Decimal("0.1"), rounding=ROUND_FLOOR))

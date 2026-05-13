from uuid import uuid4

from app.services.facility_service import _apply_match_scores, calculate_availability, haversine_distance, resolve_availability
from app.services.matching_service import (
    MODERATE_MATCH,
    NOT_ENOUGH_DATA,
    STRONG_MATCH,
    calculate_match_score,
    get_match_category,
)
from app.models.availability import FacilityAvailabilityML


# ── calculate_availability ─────────────────────────────────────────────────

def test_calculate_availability_likely():
    assert calculate_availability(100) == "Likely Available"
    assert calculate_availability(150) == "Likely Available"
    assert calculate_availability(999) == "Likely Available"


def test_calculate_availability_possibly():
    assert calculate_availability(30) == "Possibly Available"
    assert calculate_availability(50) == "Possibly Available"
    assert calculate_availability(99) == "Possibly Available"


def test_calculate_availability_unlikely():
    assert calculate_availability(0) == "Likely Unavailable"
    assert calculate_availability(1) == "Likely Unavailable"
    assert calculate_availability(29) == "Likely Unavailable"


def test_calculate_availability_none():
    assert calculate_availability(None) == "Possibly Available"


# ── haversine_distance ─────────────────────────────────────────────────────

def test_haversine_same_point():
    result = haversine_distance(-37.8136, 144.9631, -37.8136, 144.9631)
    assert result == 0.0


def test_haversine_known_distance():
    # Melbourne CBD to Sydney CBD ~713 km
    result = haversine_distance(-37.8136, 144.9631, -33.8688, 151.2093)
    assert 700 < result < 730


def test_haversine_short_distance():
    # Very close points — distance should be < 0.1 km
    result = haversine_distance(-37.8136, 144.9631, -37.8140, 144.9635)
    assert result < 0.1


# ── resolve_availability ───────────────────────────────────────────────────

def test_resolve_availability_with_ml():
    ml_record = FacilityAvailabilityML()
    ml_record.residential_label_name = "Likely Available"
    ml_record.home_care_label_name = "Does Not Provide This Service"
    ml_record.restorative_care_label_name = "Potentially Available"

    class FakeRow:
        id = "test-id"
        care_type = "Residential"
        residential_places = 50

    ml_map = {"test-id": ml_record}
    availability, source = resolve_availability(ml_map, FakeRow())

    assert availability == "Likely Available"
    assert "ML" in source


def test_resolve_availability_fallback():
    class FakeRow:
        id = "test-id"
        care_type = "Residential"
        residential_places = 150

    ml_map = {}
    availability, source = resolve_availability(ml_map, FakeRow())

    assert availability == "Likely Available"
    assert "bed capacity" in source


def test_resolve_availability_none_ml():
    class FakeRow:
        id = "test-id"
        care_type = "Residential"
        residential_places = 25

    ml_map = {"test-id": None}
    availability, source = resolve_availability(ml_map, FakeRow())

    assert availability == "Likely Unavailable"
    assert "bed capacity" in source


# ── matching ───────────────────────────────────────────────────────────────

class FakeStarRating:
    re_food_score = 4.0
    re_safety_score = 5.0
    re_respect_score = 3.0
    re_caring_score = None
    re_home_score = None
    staffing_rating = 2
    compliance_rating = 5
    quality_measures_rating = 4


class NearPerfectStarRating:
    re_food_score = 5.0
    re_safety_score = 4.99


class OutOfRangeStarRating:
    re_food_score = 5.5


def test_calculate_match_score_with_all_selected_fields_available():
    weights = {
        "food_points": 50,
        "safety_points": 50,
    }

    assert calculate_match_score(FakeStarRating(), weights) == 90.0


def test_calculate_match_score_does_not_round_near_perfect_up_to_100():
    weights = {
        "food_points": 50,
        "safety_points": 50,
    }

    assert calculate_match_score(NearPerfectStarRating(), weights) == 99.9


def test_calculate_match_score_clamps_ratings_to_five():
    weights = {
        "food_points": 100,
    }

    assert calculate_match_score(OutOfRangeStarRating(), weights) == 100.0


def test_calculate_match_score_returns_none_when_any_selected_score_is_missing():
    weights = {
        "food_points": 50,
        "caring_points": 50,
    }

    assert calculate_match_score(FakeStarRating(), weights) is None


def test_calculate_match_score_returns_none_when_all_selected_scores_missing():
    weights = {
        "caring_points": 60,
        "home_points": 40,
    }

    assert calculate_match_score(FakeStarRating(), weights) is None


def test_get_match_category_thresholds():
    assert get_match_category(75) == STRONG_MATCH
    assert get_match_category(50) == MODERATE_MATCH
    assert get_match_category(None) == NOT_ENOUGH_DATA


def test_apply_match_scores_matches_string_row_id_to_uuid_star_key():
    facility_id = uuid4()

    class FakeFacility:
        id = str(facility_id)
        service_name = "Example Care"

    weights = {"food_points": 100}
    star_map = {str(facility_id): FakeStarRating()}
    rows = _apply_match_scores([FakeFacility()], star_map, weights)

    assert rows[0].match_score == 80.0
    assert rows[0].match_category == STRONG_MATCH

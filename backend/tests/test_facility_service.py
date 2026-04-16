from app.services.facility_service import calculate_availability, haversine_distance, resolve_availability
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

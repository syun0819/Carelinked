from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def load_service_rows() -> list[dict[str, str]]:
    path = RAW_DIR / "aged_care_services.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def aggregate_demand_by_lga(
    file_name: str,
    lga_code_field: str,
    filters: dict[str, str] | None = None,
) -> dict[str, float]:
    path = RAW_DIR / file_name
    totals: dict[str, float] = defaultdict(float)

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if filters and any(row[key] != value for key, value in filters.items()):
                continue
            totals[row[lga_code_field]] += float(row["people_count"] or 0)

    return dict(totals)


def build_feature_rows(
    service_rows: list[dict[str, str]],
    supply_column: str,
    demand_by_lga: dict[str, float],
) -> list[dict[str, float | str | None]]:
    regional_supply_places: dict[str, float] = defaultdict(float)

    for row in service_rows:
        supply_places = float(row[supply_column] or 0)
        if supply_places <= 0:
            continue
        regional_supply_places[row["lga_code_2023"]] += supply_places

    feature_rows: list[dict[str, float | str | None]] = []
    for row in service_rows:
        facility_supply_places = float(row[supply_column] or 0)
        if facility_supply_places <= 0:
            continue

        lga_code = row["lga_code_2023"]
        total_supply = regional_supply_places.get(lga_code, 0)
        total_demand = demand_by_lga.get(lga_code, 0)

        feature_rows.append(
            {
                "facility_id": row["id"],
                "facility_supply_places": int(facility_supply_places)
                if facility_supply_places.is_integer()
                else facility_supply_places,
                "regional_demand_people": int(total_demand)
                if float(total_demand).is_integer()
                else total_demand,
                "regional_supply_places": int(total_supply)
                if float(total_supply).is_integer()
                else total_supply,
                "regional_demand_pressure": safe_divide(total_demand, total_supply),
                "facility_supply_share_lga": safe_divide(
                    facility_supply_places, total_supply
                ),
            }
        )

    return feature_rows


def write_csv(path: Path, rows: list[dict[str, float | str | None]]) -> None:
    fieldnames = [
        "facility_id",
        "facility_supply_places",
        "regional_demand_people",
        "regional_supply_places",
        "regional_demand_pressure",
        "facility_supply_share_lga",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    service_rows = load_service_rows()

    residential_demand_by_lga = aggregate_demand_by_lga(
        "residential_care_demand_by_service_lga.csv",
        lga_code_field="lga_code",
    )
    home_care_demand_by_lga = aggregate_demand_by_lga(
        "home_care_demand_by_service_lga.csv",
        lga_code_field="lga_code",
    )
    restorative_demand_by_lga = aggregate_demand_by_lga(
        "flex_care_demand_by_service_lga.csv",
        lga_code_field="lga_code",
        filters={"care_type": "STRC"},
    )

    residential_rows = build_feature_rows(
        service_rows=service_rows,
        supply_column="residential_places",
        demand_by_lga=residential_demand_by_lga,
    )
    home_care_rows = build_feature_rows(
        service_rows=service_rows,
        supply_column="home_care_places",
        demand_by_lga=home_care_demand_by_lga,
    )
    restorative_rows = build_feature_rows(
        service_rows=service_rows,
        supply_column="restorative_care_places",
        demand_by_lga=restorative_demand_by_lga,
    )

    write_csv(PROCESSED_DIR / "cluster_features_residential.csv", residential_rows)
    write_csv(PROCESSED_DIR / "cluster_features_home_care.csv", home_care_rows)
    write_csv(
        PROCESSED_DIR / "cluster_features_restorative_care.csv", restorative_rows
    )


if __name__ == "__main__":
    main()

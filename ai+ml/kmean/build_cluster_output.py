from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
MODEL_SELECTION_DIR = BASE_DIR / "kmean" / "model_output" / "model_selection"
INSPECT_DIR = BASE_DIR / "kmean" / "model_output" / "inspect"
MANUAL_LABEL_DIR = BASE_DIR / "kmean" / "cluster_output" / "manual_labels"
FINAL_OUTPUT_DIR = BASE_DIR / "kmean" / "cluster_output" / "final"


def load_labeled_stream(stream_name: str, selected_k: int) -> pd.DataFrame:
    inspect_path = INSPECT_DIR / f"{stream_name}_k{selected_k}_clusters.csv"
    manual_label_path = MANUAL_LABEL_DIR / f"{stream_name}_cluster_labels.csv"

    inspect_df = pd.read_csv(inspect_path, usecols=["facility_id", "cluster_id"])
    label_df = pd.read_csv(manual_label_path)

    missing_columns = {"stream_name", "selected_k", "cluster_id", "label_id", "label_name"} - set(label_df.columns)
    if missing_columns:
        raise ValueError(
            f"{manual_label_path} is missing required columns: {sorted(missing_columns)}"
        )

    label_df = label_df[
        (label_df["stream_name"] == stream_name)
        & (label_df["selected_k"] == selected_k)
    ].copy()

    if label_df.empty:
        raise ValueError(
            f"{manual_label_path} does not contain labels for stream_name={stream_name!r} and selected_k={selected_k}."
        )

    if label_df["label_id"].isna().any() or label_df["label_name"].isna().any():
        raise ValueError(
            f"{manual_label_path} still has blank labels. Fill in label_id and label_name first."
        )

    merged_df = inspect_df.merge(
        label_df[["cluster_id", "label_id", "label_name"]],
        on="cluster_id",
        how="left",
    )

    if merged_df["label_id"].isna().any() or merged_df["label_name"].isna().any():
        raise ValueError(
            f"{manual_label_path} does not cover every cluster_id used in {inspect_path.name}."
        )

    merged_df["label_id"] = merged_df["label_id"].astype("Int64")

    return merged_df.rename(
        columns={
            "label_id": f"{stream_name}_label_id",
            "label_name": f"{stream_name}_label_name",
        }
    ).drop(columns=["cluster_id"])


def main() -> None:
    FINAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    best_k_df = pd.read_csv(MODEL_SELECTION_DIR / "kmeans_best_k_by_stream.csv")

    final_df = pd.read_csv(RAW_DIR / "aged_care_services.csv", usecols=["id"]).rename(
        columns={"id": "facility_id"}
    )
    for row in best_k_df.itertuples(index=False):
        stream_df = load_labeled_stream(row.stream_name, int(row.k))
        final_df = final_df.merge(stream_df, on="facility_id", how="left")

    final_df = final_df.sort_values("facility_id")
    ordered_columns = [
        "facility_id",
        "residential_label_id",
        "residential_label_name",
        "home_care_label_id",
        "home_care_label_name",
        "restorative_care_label_id",
        "restorative_care_label_name",
    ]
    final_df = final_df.reindex(columns=ordered_columns)

    for column in [
        "residential_label_id",
        "home_care_label_id",
        "restorative_care_label_id",
    ]:
        final_df[column] = final_df[column].fillna(0).astype("Int64")

    for column in [
        "residential_label_name",
        "home_care_label_name",
        "restorative_care_label_name",
    ]:
        final_df[column] = final_df[column].fillna("Does Not Provide This Service")

    final_df.to_csv(
        FINAL_OUTPUT_DIR / "facility_cluster_labels.csv",
        index=False,
    )


if __name__ == "__main__":
    main()

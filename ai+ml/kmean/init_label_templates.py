from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_SELECTION_DIR = BASE_DIR / "kmean" / "model_output" / "model_selection"
INSPECT_DIR = BASE_DIR / "kmean" / "model_output" / "inspect"
MANUAL_LABEL_DIR = BASE_DIR / "kmean" / "cluster_output" / "manual_labels"


def build_template(stream_name: str, selected_k: int) -> pd.DataFrame:
    inspect_path = INSPECT_DIR / f"{stream_name}_k{selected_k}_clusters.csv"
    inspect_df = pd.read_csv(inspect_path)

    cluster_ids = sorted(inspect_df["cluster_id"].dropna().unique().tolist())
    template_df = pd.DataFrame({"cluster_id": cluster_ids})
    template_df["stream_name"] = stream_name
    template_df["selected_k"] = selected_k
    template_df["label_id"] = pd.Series([pd.NA] * len(template_df), dtype="Int64")
    template_df["label_name"] = pd.Series([pd.NA] * len(template_df), dtype="string")
    template_df = template_df[
        ["stream_name", "selected_k", "cluster_id", "label_id", "label_name"]
    ]

    manual_path = MANUAL_LABEL_DIR / f"{stream_name}_cluster_labels.csv"
    if manual_path.exists():
        existing_df = pd.read_csv(manual_path)
        keep_columns = ["cluster_id", "label_id", "label_name"]
        existing_df = existing_df[keep_columns]
        template_df = template_df.drop(columns=["label_id", "label_name"]).merge(
            existing_df,
            on="cluster_id",
            how="left",
        )

    return template_df


def main() -> None:
    MANUAL_LABEL_DIR.mkdir(parents=True, exist_ok=True)

    best_k_df = pd.read_csv(MODEL_SELECTION_DIR / "kmeans_best_k_by_stream.csv")
    for row in best_k_df.itertuples(index=False):
        template_df = build_template(row.stream_name, int(row.k))
        template_df.to_csv(
            MANUAL_LABEL_DIR / f"{row.stream_name}_cluster_labels.csv",
            index=False,
        )


if __name__ == "__main__":
    main()

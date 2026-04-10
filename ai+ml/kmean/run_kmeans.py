from __future__ import annotations

from pathlib import Path

import pandas as pd

from kmeans_utils import fit_kmeans, load_feature_table, prepare_features, summarize_clusters


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_OUTPUT_DIR = BASE_DIR / "kmean" / "model_output"
INSPECT_DIR = MODEL_OUTPUT_DIR / "inspect"
EVALUATION_DIR = MODEL_OUTPUT_DIR / "evaluation"
MODEL_SELECTION_DIR = MODEL_OUTPUT_DIR / "model_selection"
CLUSTER_OUTPUT_DIR = BASE_DIR / "kmean" / "cluster_output"

STREAM_FILES = {
    "residential": "cluster_features_residential.csv",
    "home_care": "cluster_features_home_care.csv",
    "restorative_care": "cluster_features_restorative_care.csv",
}

CANDIDATE_KS = [3, 4, 5, 6]


def ensure_directories() -> None:
    INSPECT_DIR.mkdir(parents=True, exist_ok=True)
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    CLUSTER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_stream(stream_name: str, input_file_name: str) -> list[dict[str, float | int | str | None]]:
    input_path = PROCESSED_DIR / input_file_name
    original_df = load_feature_table(str(input_path))
    model_df, _ = prepare_features(original_df)

    selection_rows: list[dict[str, float | int | str | None]] = []

    for k in CANDIDATE_KS:
        if len(model_df) <= k:
            continue

        labeled_model_df, _, silhouette, inertia = fit_kmeans(model_df, k)

        inspect_df = original_df.copy()
        inspect_df["cluster_id"] = labeled_model_df["cluster_id"].values
        inspect_df.to_csv(
            INSPECT_DIR / f"{stream_name}_k{k}_clusters.csv",
            index=False,
        )

        summary_df = summarize_clusters(original_df, labeled_model_df)
        summary_df.to_csv(
            EVALUATION_DIR / f"{stream_name}_k{k}_summary.csv",
            index=False,
        )

        selection_rows.append(
            {
                "stream_name": stream_name,
                "k": k,
                "silhouette_score": silhouette,
                "inertia": inertia,
                "row_count": len(original_df),
            }
        )

    return selection_rows


def main() -> None:
    ensure_directories()

    all_selection_rows: list[dict[str, float | int | str | None]] = []
    for stream_name, input_file_name in STREAM_FILES.items():
        all_selection_rows.extend(run_stream(stream_name, input_file_name))

    selection_df = pd.DataFrame(all_selection_rows)
    selection_df = selection_df.sort_values(
        ["stream_name", "silhouette_score", "inertia"],
        ascending=[True, False, True],
    )
    selection_df["rank_within_stream"] = selection_df.groupby("stream_name").cumcount() + 1

    best_k_df = selection_df[selection_df["rank_within_stream"] == 1].copy()

    selection_df.to_csv(
        MODEL_SELECTION_DIR / "kmeans_model_selection.csv",
        index=False,
    )
    best_k_df.to_csv(
        MODEL_SELECTION_DIR / "kmeans_best_k_by_stream.csv",
        index=False,
    )


if __name__ == "__main__":
    main()

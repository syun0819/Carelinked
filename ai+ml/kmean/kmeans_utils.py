from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "facility_supply_places",
    "regional_demand_pressure",
    "facility_supply_share_lga",
]

LOG_COLUMNS = [
    "facility_supply_places",
    "regional_demand_pressure",
]


def load_feature_table(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required_columns = [
        "facility_id",
        "facility_supply_places",
        "regional_demand_people",
        "regional_supply_places",
        "regional_demand_pressure",
        "facility_supply_share_lga",
    ]
    return df[required_columns].dropna().copy()


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, StandardScaler]:
    model_df = df.copy()

    for column in LOG_COLUMNS:
        model_df[column] = model_df[column].clip(lower=0)
        model_df[column] = model_df[column].map(np.log1p)

    scaler = StandardScaler()
    model_df[FEATURE_COLUMNS] = scaler.fit_transform(model_df[FEATURE_COLUMNS])
    return model_df, scaler


def fit_kmeans(model_df: pd.DataFrame, k: int) -> tuple[pd.DataFrame, KMeans, float | None, float]:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    labeled_df = model_df.copy()
    labeled_df["cluster_id"] = kmeans.fit_predict(model_df[FEATURE_COLUMNS])

    silhouette = None
    if labeled_df["cluster_id"].nunique() > 1:
        silhouette = silhouette_score(model_df[FEATURE_COLUMNS], labeled_df["cluster_id"])

    return labeled_df, kmeans, silhouette, float(kmeans.inertia_)


def summarize_clusters(original_df: pd.DataFrame, labeled_df: pd.DataFrame) -> pd.DataFrame:
    summary_df = original_df.copy()
    summary_df["cluster_id"] = labeled_df["cluster_id"].values

    return (
        summary_df.groupby("cluster_id", as_index=False)
        .agg(
            cluster_size=("facility_id", "count"),
            facility_supply_places_mean=("facility_supply_places", "mean"),
            regional_demand_people_mean=("regional_demand_people", "mean"),
            regional_supply_places_mean=("regional_supply_places", "mean"),
            regional_demand_pressure_mean=("regional_demand_pressure", "mean"),
            facility_supply_share_lga_mean=("facility_supply_share_lga", "mean"),
        )
        .sort_values("cluster_id")
    )

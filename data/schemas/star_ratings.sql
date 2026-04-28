CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS star_ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Soft link to aged_care_services (nullable, no FK constraint).
    -- See star_ratings_raw.sql for rationale.
    service_id UUID,

    reporting_period TEXT NOT NULL,
    service_name TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    service_suburb TEXT,
    state_territory TEXT,

    -- Five published star ratings (1-5, NULL = no rating available)
    overall_star_rating         SMALLINT,
    residents_experience_rating SMALLINT,
    compliance_rating           SMALLINT,
    staffing_rating             SMALLINT,
    quality_measures_rating     SMALLINT,

    -- Residents' Experience topic scores on a 1.0-5.0 scale.
    -- Computed as a weighted average of the four answer levels:
    --   Always           = 5
    --   Most of the time = 11/3 (~3.67)
    --   Some of the time = 7/3  (~2.33)
    --   Never            = 1
    -- NULL when no survey data is available for that service.
    re_food_score        NUMERIC(3,2),
    re_safety_score      NUMERIC(3,2),
    re_operation_score   NUMERIC(3,2),
    re_care_need_score   NUMERIC(3,2),
    re_competent_score   NUMERIC(3,2),
    re_independent_score NUMERIC(3,2),
    re_explain_score     NUMERIC(3,2),
    re_respect_score     NUMERIC(3,2),
    re_follow_up_score   NUMERIC(3,2),
    re_caring_score      NUMERIC(3,2),
    re_voice_score       NUMERIC(3,2),
    re_home_score        NUMERIC(3,2),

    -- Staffing care minutes (kept from raw because the frontend may show them)
    s_rn_care_minutes_target    NUMERIC(6,2),
    s_rn_care_minutes_actual    NUMERIC(6,2),
    s_total_care_minutes_target NUMERIC(6,2),
    s_total_care_minutes_actual NUMERIC(6,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_star_ratings_service_id
    ON star_ratings(service_id) WHERE service_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_star_ratings_natural
    ON star_ratings(service_name, service_suburb);

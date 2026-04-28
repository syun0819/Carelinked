CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS star_ratings_raw (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Soft link to aged_care_services. Nullable, no FK constraint
    -- because the two source files have independent extract dates and
    -- some services in the ratings file may not yet exist in the
    -- service list. Resolved during the load via (service_name, suburb).
    service_id UUID,

    reporting_period TEXT NOT NULL,
    service_name TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    service_suburb TEXT,
    purpose TEXT,
    aged_care_planning_region TEXT,
    state_territory TEXT,
    mmm_region TEXT,
    mmm_code TEXT,
    size TEXT,

    overall_star_rating         SMALLINT,
    residents_experience_rating SMALLINT,
    compliance_rating           SMALLINT,
    staffing_rating             SMALLINT,
    quality_measures_rating     SMALLINT,

    re_interview_year TEXT,

    -- Residents' Experience: 12 topics x 4 answer levels = 48 columns
    re_food_always               NUMERIC(5,2),
    re_food_most_of_the_time     NUMERIC(5,2),
    re_food_some_of_the_time     NUMERIC(5,2),
    re_food_never                NUMERIC(5,2),

    re_safety_always             NUMERIC(5,2),
    re_safety_most_of_the_time   NUMERIC(5,2),
    re_safety_some_of_the_time   NUMERIC(5,2),
    re_safety_never              NUMERIC(5,2),

    re_operation_always             NUMERIC(5,2),
    re_operation_most_of_the_time   NUMERIC(5,2),
    re_operation_some_of_the_time   NUMERIC(5,2),
    re_operation_never              NUMERIC(5,2),

    re_care_need_always             NUMERIC(5,2),
    re_care_need_most_of_the_time   NUMERIC(5,2),
    re_care_need_some_of_the_time   NUMERIC(5,2),
    re_care_need_never              NUMERIC(5,2),

    re_competent_always             NUMERIC(5,2),
    re_competent_most_of_the_time   NUMERIC(5,2),
    re_competent_some_of_the_time   NUMERIC(5,2),
    re_competent_never              NUMERIC(5,2),

    re_independent_always             NUMERIC(5,2),
    re_independent_most_of_the_time   NUMERIC(5,2),
    re_independent_some_of_the_time   NUMERIC(5,2),
    re_independent_never              NUMERIC(5,2),

    re_explain_always             NUMERIC(5,2),
    re_explain_most_of_the_time   NUMERIC(5,2),
    re_explain_some_of_the_time   NUMERIC(5,2),
    re_explain_never              NUMERIC(5,2),

    re_respect_always             NUMERIC(5,2),
    re_respect_most_of_the_time   NUMERIC(5,2),
    re_respect_some_of_the_time   NUMERIC(5,2),
    re_respect_never              NUMERIC(5,2),

    re_follow_up_always             NUMERIC(5,2),
    re_follow_up_most_of_the_time   NUMERIC(5,2),
    re_follow_up_some_of_the_time   NUMERIC(5,2),
    re_follow_up_never              NUMERIC(5,2),

    re_caring_always             NUMERIC(5,2),
    re_caring_most_of_the_time   NUMERIC(5,2),
    re_caring_some_of_the_time   NUMERIC(5,2),
    re_caring_never              NUMERIC(5,2),

    re_voice_always             NUMERIC(5,2),
    re_voice_most_of_the_time   NUMERIC(5,2),
    re_voice_some_of_the_time   NUMERIC(5,2),
    re_voice_never              NUMERIC(5,2),

    re_home_always             NUMERIC(5,2),
    re_home_most_of_the_time   NUMERIC(5,2),
    re_home_some_of_the_time   NUMERIC(5,2),
    re_home_never              NUMERIC(5,2),

    -- Compliance detail
    c_decision_type         TEXT,
    c_date_decision_applied DATE,
    c_date_decision_ends    DATE,

    -- Staffing detail (care minutes per resident per day)
    s_rn_care_minutes_target    NUMERIC(6,2),
    s_rn_care_minutes_actual    NUMERIC(6,2),
    s_total_care_minutes_target NUMERIC(6,2),
    s_total_care_minutes_actual NUMERIC(6,2),

    -- Quality Measures detail (rates per source units; see Notes sheet)
    qm_pressure_injuries        NUMERIC(6,2),
    qm_restrictive_practices    NUMERIC(6,2),
    qm_unplanned_weight_loss    NUMERIC(6,2),
    qm_falls                    NUMERIC(6,2),
    qm_falls_major_injury       NUMERIC(6,2),
    qm_medication_polypharmacy  NUMERIC(6,2),
    qm_medication_antipsychotic NUMERIC(6,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

CREATE INDEX IF NOT EXISTS idx_star_ratings_raw_service_id
    ON star_ratings_raw(service_id) WHERE service_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_star_ratings_raw_natural
    ON star_ratings_raw(service_name, service_suburb);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS aged_care_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    service_name TEXT NOT NULL,
    physical_address TEXT,
    physical_suburb TEXT,
    physical_state TEXT,
    physical_post_code VARCHAR(10),

    aged_care_planning_region_acpr_2018 TEXT,
    care_type TEXT,

    residential_places INTEGER,
    home_care_places INTEGER,
    restorative_care_places INTEGER,

    provider_name TEXT,
    organisation_type TEXT,
    abs_remoteness TEXT,

    mmm_code_2019 INTEGER,

    sa2_code_2016 TEXT,
    sa2_name_2016 TEXT,

    sa3_code_2016 TEXT,
    sa3_name_2016 TEXT,

    lga_name_2023 TEXT,
    lga_code_2023 TEXT,

    phn_code_2017 TEXT,
    phn_name_2017 TEXT,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    australian_government_funding_2024_25 NUMERIC(14,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
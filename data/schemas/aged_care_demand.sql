CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS aged_care_demand (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lga_code_2017 TEXT NOT NULL,
    lga_name_2017 TEXT NOT NULL,
    lga_type_2017 TEXT,

    total_people_using_home_support INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
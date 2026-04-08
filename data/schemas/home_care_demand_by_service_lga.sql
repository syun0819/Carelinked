CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS home_care_demand_by_service_lga (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lga_code TEXT NOT NULL,
    lga_name TEXT NOT NULL,
    care_level SMALLINT NOT NULL CHECK (care_level BETWEEN 1 AND 4),
    people_count INTEGER NOT NULL CHECK (people_count >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

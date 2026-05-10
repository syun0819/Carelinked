CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP TABLE IF EXISTS crime_rate_lga;
CREATE TABLE IF NOT EXISTS crime_rate_lga (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lga_name TEXT NOT NULL,
    year INTEGER NOT NULL,

    offence TEXT NOT NULL,               -- 'dwelling', 'motor_vehicle', 'violent'

    adjusted_rate NUMERIC(12, 2),        -- normalised offence rate per 100,000 population
                                         -- NULL where data is suppressed or unavailable

    -- Source metadata
    frequency TEXT NOT NULL,             -- always 'ANNUAL' in this dataset
    measure TEXT NOT NULL,               -- always 'OFFENCE_RATE_POOLED_NORMALISED'
    region_type TEXT NOT NULL,           -- always 'LGA_2024'
    offence_type TEXT NOT NULL,          -- always 'OFF'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (lga_name, year, offence)
);

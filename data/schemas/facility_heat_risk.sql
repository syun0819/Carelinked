CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP TABLE IF EXISTS facility_heat_risk;
CREATE TABLE IF NOT EXISTS facility_heat_risk (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    service_id UUID NOT NULL REFERENCES aged_care_services(id) ON DELETE CASCADE,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    grid_lat DOUBLE PRECISION,
    grid_lon DOUBLE PRECISION,

    avg_hot_days_per_year NUMERIC(6,2),
    avg_extreme_days_per_year NUMERIC(6,2),
    avg_heatwaves_per_year NUMERIC(6,2),
    avg_hot_nights_per_year NUMERIC(6,2),

    risk_score NUMERIC(5,3),
    heat_risk TEXT CHECK (heat_risk IN ('low', 'medium', 'high', 'error')),

    error_message TEXT,

    data_start_date DATE,
    data_end_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (service_id, data_start_date, data_end_date)
);

CREATE INDEX IF NOT EXISTS idx_facility_heat_risk_service_id
    ON facility_heat_risk (service_id);

CREATE INDEX IF NOT EXISTS idx_facility_heat_risk_heat_risk
    ON facility_heat_risk (heat_risk);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS lga_boundaries;
CREATE TABLE IF NOT EXISTS lga_boundaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lga_code TEXT UNIQUE NOT NULL,
    lga_name TEXT NOT NULL,

    state_code TEXT,
    state_name TEXT,

    area_sqkm DOUBLE PRECISION,

    -- WKT representation of MultiPolygon in EPSG:7844 (GDA2020 lat/lon).
    -- Pre-simplified to ~100m tolerance for frontend rendering.
    -- CRS is not stored here — readers must apply EPSG:7844 themselves.
    geom_wkt TEXT NOT NULL,

    loci_uri TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS lga_boundaries_state_idx
    ON lga_boundaries (state_name);
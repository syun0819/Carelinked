CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP TABLE IF EXISTS bushfire_extents;
CREATE TABLE IF NOT EXISTS bushfire_extents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    fire_id TEXT,
    fire_name TEXT,

    ignition_date TIMESTAMPTZ,    

    area_ha DOUBLE PRECISION,
    perim_km DOUBLE PRECISION,

    state TEXT,
    agency TEXT,

    centroid_lat DOUBLE PRECISION,
    centroid_lon DOUBLE PRECISION,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

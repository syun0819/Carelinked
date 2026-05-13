CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS bushfire_lga_summary;
CREATE TABLE IF NOT EXISTS bushfire_lga_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lga_code TEXT UNIQUE NOT NULL,
    lga_name TEXT NOT NULL,
    state_name TEXT,

    bushfire_count INTEGER NOT NULL DEFAULT 0,
    earliest_date TIMESTAMPTZ,
    latest_date TIMESTAMPTZ,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS bushfire_lga_summary_state_idx
    ON bushfire_lga_summary (state_name);

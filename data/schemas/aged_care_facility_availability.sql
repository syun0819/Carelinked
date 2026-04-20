CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP TABLE IF EXISTS aged_care_facility_availability;
CREATE TABLE IF NOT EXISTS aged_care_facility_availability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    facility_id UUID NOT NULL,

    residential_label_id INTEGER,
    residential_label_name TEXT,

    home_care_label_id INTEGER,
    home_care_label_name TEXT,

    restorative_care_label_id INTEGER,
    restorative_care_label_name TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (facility_id)
        REFERENCES aged_care_services(id)
        ON DELETE CASCADE,

    UNIQUE (facility_id)
);
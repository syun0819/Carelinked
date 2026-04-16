-- Run this script from ai+ml/data_processing using:
-- psql "host=$DB_HOST port=$DB_PORT dbname=$DB_NAME user=$DB_USER sslmode=$DB_SSLMODE" -f export_tables.sql
--
-- Export every ML input table into ../data/raw so the downstream Python jobs
-- read a complete, consistent dataset from a single directory.

\set ON_ERROR_STOP on

\copy aged_care_services TO '../data/raw/aged_care_services.csv' CSV HEADER
\copy flex_care_demand_by_service_lga TO '../data/raw/flex_care_demand_by_service_lga.csv' CSV HEADER
\copy home_care_demand_by_recipient_lga TO '../data/raw/home_care_demand_by_recipient_lga.csv' CSV HEADER
\copy home_care_demand_by_service_lga TO '../data/raw/home_care_demand_by_service_lga.csv' CSV HEADER
\copy home_support_demand_by_recipient_lga TO '../data/raw/home_support_demand_by_recipient_lga.csv' CSV HEADER
\copy location_geo TO '../data/raw/location_geo.csv' CSV HEADER
\copy residential_care_demand_by_service_lga TO '../data/raw/residential_care_demand_by_service_lga.csv' CSV HEADER
\copy aged_care_facility_availability TO '../data/raw/aged_care_facility_availability.csv' CSV HEADER

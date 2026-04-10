-- connect to the database using the credentials from the .env file
-- the run the script to export the tables to CSV files:
-- psql "host=$DB_HOST port=$DB_PORT dbname=$DB_NAME user=$DB_USER sslmode=$DB_SSLMODE" -f export_tables.sql

\copy aged_care_services TO 'ai+ml/data/raw/aged_care_services.csv' CSV HEADER
\copy flex_care_demand_by_service_lga TO 'ai+ml/data/raw/flex_care_demand_by_service_lga.csv' CSV HEADER
\copy home_care_demand_by_recipient_lga TO 'ai+ml/data/raw/home_care_demand_by_recipient_lga.csv' CSV HEADER
\copy home_care_demand_by_service_lga TO 'ai+ml/data/raw/home_care_demand_by_service_lga.csv' CSV HEADER
\copy home_support_demand_by_recipient_lga TO 'ai+ml/data/raw/home_support_demand_by_recipient_lga.csv' CSV HEADER
\copy location_geo TO 'ai+ml/data/raw/location_geo.csv' CSV HEADER
\copy residential_care_demand_by_service_lga TO 'ai+ml/data/raw/residential_care_demand_by_service_lga.csv' CSV HEADER





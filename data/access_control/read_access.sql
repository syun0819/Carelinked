-- create read-only role
CREATE ROLE readonly_group;

-- allow connection and schema access
GRANT CONNECT ON DATABASE "carelink" TO readonly_group;
GRANT USAGE ON SCHEMA public TO readonly_group;

-- read only on existing and future tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_group;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_group;
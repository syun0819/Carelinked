-- create role
CREATE ROLE write_sandbox_group;

-- allow connection
GRANT CONNECT ON DATABASE "carelink" TO write_sandbox_group;

-- schema access (USAGE = see inside, CREATE = make tables)
GRANT USAGE, CREATE ON SCHEMA public TO write_sandbox_group;

-- read only on existing tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO write_sandbox_group;

-- read only on future tables too
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO write_sandbox_group;
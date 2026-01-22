CREATE SCHEMA IF NOT EXISTS iceberg.gold
WITH (location = 's3a://lakehouse/gold/warehouse/gold');

CREATE TABLE IF NOT EXISTS iceberg.gold.user_sessions (
  user_id VARCHAR,
  session_id VARCHAR,
  start_ts TIMESTAMP,
  end_ts TIMESTAMP,
  pages BIGINT,
  errors BIGINT,
  label VARCHAR
)
WITH (
  format = 'PARQUET'
);

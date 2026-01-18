-- This creates a calendar from 2023 to 2026
WITH date_series AS (
    SELECT 
        generate_series('2023-01-01'::date, '2026-12-31'::date, '1 day'::interval)::date AS full_date
)

SELECT
    -- A unique ID for each date (e.g., 20240101)
    CAST(to_char(full_date, 'YYYYMMDD') AS INTEGER) AS date_key,
    full_date,
    extract(year FROM full_date) AS year,
    extract(month FROM full_date) AS month,
    to_char(full_date, 'Month') AS month_name,
    extract(day FROM full_date) AS day,
    to_char(full_date, 'Day') AS day_name,
    -- Is it a weekend? (0 = Sunday, 6 = Saturday)
    CASE WHEN extract(dow FROM full_date) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_series
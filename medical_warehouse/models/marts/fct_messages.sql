WITH stg_messages AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
),
dim_dates AS (
    SELECT * FROM {{ ref('dim_dates') }}
),
dim_channels AS (
    SELECT * FROM {{ ref('dim_channels') }}
)

SELECT
    m.message_id,
    -- Connect to Dimension Tables using Foreign Keys
    c.channel_key,
    d.date_key,
    m.message_text,
    m.message_length,
    m.view_count,
    m.forward_count,
    m.has_image
FROM stg_messages m
-- Join with Dimensions to get the Keys
LEFT JOIN dim_dates d 
    ON CAST(to_char(m.message_timestamp, 'YYYYMMDD') AS INTEGER) = d.date_key
LEFT JOIN dim_channels c 
    ON m.channel_name = c.channel_name
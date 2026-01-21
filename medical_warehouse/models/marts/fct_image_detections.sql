-- This model joins our AI image results with our main message data
WITH detections AS (
    SELECT * FROM {{ source('raw', 'image_detections') }}
),
messages AS (
    SELECT * FROM {{ ref('fct_messages') }}
)

SELECT
    m.message_id,
    m.channel_key,
    m.date_key,
    d.detected_class,
    d.confidence_score,
    d.image_category,
    m.view_count
FROM messages m
-- We use a JOIN to connect the message to its specific AI detection result
INNER JOIN detections d ON CAST(m.message_id AS TEXT) = CAST(d.message_id AS TEXT)
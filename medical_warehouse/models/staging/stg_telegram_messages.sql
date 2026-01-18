-- This model cleans the raw telegram data
WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'telegram_messages') }}
)

SELECT
    message_id,
    channel_name,
    -- Convert the text date into a real timestamp
    CAST(message_date AS TIMESTAMP) AS message_timestamp,
    message_text,
    -- Standardize names and handle empty values
    COALESCE(views, 0) AS view_count,
    COALESCE(forwards, 0) AS forward_count,
    image_path,
    -- Add a calculated field: Does it have an image?
    CASE WHEN image_path IS NOT NULL THEN TRUE ELSE FALSE END AS has_image,
    -- Add a calculated field: Length of the message
    LENGTH(message_text) AS message_length
FROM raw_data
WHERE message_text IS NOT NULL -- Remove empty messages
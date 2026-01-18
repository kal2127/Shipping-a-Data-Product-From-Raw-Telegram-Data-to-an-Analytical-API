WITH channel_data AS (
    SELECT 
        channel_name,
        MIN(message_timestamp) AS first_post_date,
        MAX(message_timestamp) AS last_post_date,
        COUNT(message_id) AS total_posts,
        AVG(view_count) AS avg_views
    FROM {{ ref('stg_telegram_messages') }}
    GROUP BY 1
)

SELECT
    -- Create a simple unique key for each channel
    MD5(channel_name) AS channel_key,
    channel_name,
    first_post_date,
    last_post_date,
    total_posts,
    ROUND(avg_views, 2) AS avg_views
FROM channel_data
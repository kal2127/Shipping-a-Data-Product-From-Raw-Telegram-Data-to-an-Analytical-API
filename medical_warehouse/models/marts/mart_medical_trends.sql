SELECT
    d.full_date,
    d.day_name,
    d.is_weekend,
    COUNT(f.message_id) AS total_messages,
    SUM(f.view_count) AS total_views,
    ROUND(AVG(f.message_length), 2) AS avg_message_length
FROM {{ ref('fct_messages') }} f
LEFT JOIN {{ ref('dim_dates') }} d ON f.date_key = d.date_key
GROUP BY 1, 2, 3
ORDER BY d.full_date DESC
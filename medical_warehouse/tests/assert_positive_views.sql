-- This test fails if it finds any message with views less than 0
SELECT *
FROM {{ ref('fct_messages') }}
WHERE view_count < 0
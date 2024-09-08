SELECT 
    CAST(event_name AS STRING) AS event_name,
    PARSE_DATE('%m/%d/%y', start_date) AS start_date,
    PARSE_DATE('%m/%d/%y', end_date) AS end_date
FROM 
    {{ ref('shopping_events') }}
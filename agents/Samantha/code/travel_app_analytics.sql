-- Travel App: Example analytics SQL queries
-- Path: output/code/data/travel_app_analytics.sql
-- Purpose: Provide sample queries to validate instrumentation and produce basic metrics.

-- 1) DAU (Daily Active Users) by platform
SELECT
  DATE(event_timestamp) as event_date,
  platform,
  COUNT(DISTINCT COALESCE(user_id, anon_id)) AS dau
FROM analytics.events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND event_name IN ('session_start','discovery_view','search_initiated','search_result_clicked','itinerary_created','booking_payment_success')
GROUP BY event_date, platform
ORDER BY event_date DESC;

-- 2) Funnel: Search -> Itinerary Created -> Booking Initiated -> Booking Success
WITH funnel AS (
  SELECT
    COALESCE(user_id, anon_id) AS uid,
    MIN(CASE WHEN event_name = 'search_initiated' THEN event_timestamp END) AS t_search,
    MIN(CASE WHEN event_name = 'itinerary_created' THEN event_timestamp END) AS t_itin,
    MIN(CASE WHEN event_name = 'booking_initiated' THEN event_timestamp END) AS t_booking_init,
    MIN(CASE WHEN event_name = 'booking_payment_success' THEN event_timestamp END) AS t_booking_success
  FROM analytics.events
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    AND event_name IN ('search_initiated','itinerary_created','booking_initiated','booking_payment_success')
  GROUP BY uid
)
SELECT
  COUNT(1) FILTER (WHERE t_search IS NOT NULL) AS search_count,
  COUNT(1) FILTER (WHERE t_itin IS NOT NULL) AS itin_count,
  COUNT(1) FILTER (WHERE t_booking_init IS NOT NULL) AS booking_init_count,
  COUNT(1) FILTER (WHERE t_booking_success IS NOT NULL) AS booking_success_count
FROM funnel;

-- 3) Top search queries and average result click-through rate
WITH searches AS (
  SELECT
    query_text,
    COUNT(1) AS searches,
    SUM(CASE WHEN event_name = 'search_result_clicked' THEN 1 ELSE 0 END) AS clicks
  FROM analytics.events
  WHERE event_name IN ('search_initiated','search_result_clicked')
    AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
  GROUP BY query_text
)
SELECT
  query_text,
  searches,
  clicks,
  SAFE_DIVIDE(clicks, searches) AS ctr
FROM searches
ORDER BY searches DESC
LIMIT 50;

-- 4) Revenue by day and payment method
SELECT
  DATE(event_timestamp) AS event_date,
  payment_method,
  SUM(revenue_local * exchange_rate_to_usd) AS revenue_usd,
  SUM(revenue_local) AS revenue_local_sum
FROM analytics.events
WHERE event_name = 'booking_payment_success'
  AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY event_date, payment_method
ORDER BY event_date DESC;

-- 5) Validate schema conformance: count of events missing required base properties
SELECT
  event_name,
  COUNT(1) AS total_events,
  SUM(CASE WHEN event_timestamp IS NULL THEN 1 ELSE 0 END) AS missing_event_timestamp,
  SUM(CASE WHEN COALESCE(user_id, anon_id) IS NULL THEN 1 ELSE 0 END) AS missing_user_identifiers,
  SUM(CASE WHEN platform IS NULL THEN 1 ELSE 0 END) AS missing_platform
FROM raw.events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
GROUP BY event_name
ORDER BY total_events DESC;

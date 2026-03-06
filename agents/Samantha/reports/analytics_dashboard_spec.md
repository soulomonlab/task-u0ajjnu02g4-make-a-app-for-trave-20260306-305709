# Analytics Dashboard Spec — Travel App (MVP)

Purpose: Define the dashboards needed for MVP analytics and acceptance criteria for data team and Design/Product to validate UX choices.

Dashboards
1. Funnel Conversion (search -> select -> checkout -> booking)
   - Granularity: daily, by platform, by guest_vs_signed (derived)
   - Widgets: funnel visualization, conversion rates, time-to-conversion median

2. Guest vs Signed Conversion
   - Metric: booking_conversion_rate for sessions starting with guest_checkout_start vs signup_start
   - Table: cohort analysis by day of week, platform

3. Map Engagement
   - Metrics: map_interactions per session, avg zoom_level, conversion rate from map searches
   - Heatmap: interactions by geographic bbox (top cities)

4. Revenue & ARPU
   - Daily bookings, booking_value sum, bookings_by_source

5. Errors & Stability
   - Payment_failure rate, events with error, pipeline ingestion lag

Acceptance criteria
- Each dashboard loads in <5s with sample MVP data (100k events/day simulated)
- Metrics match SQL queries (included in data repo)
- Data freshness <15 minutes for near-real-time widgets

Owners
- Data: Samantha (implement queries and dbt models)
- Product: Alex (validate metrics)
- Design: Maya (confirm UX-metric alignment)


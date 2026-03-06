# Travel App — Data & Analytics Spec (MVP)

## Situation
PRD for Travel App MVP completed (output/specs/travel_app_prd.md). Designs are next — product needs a clear data contract and analytics plan to guide UX decisions (guest checkout, booking flows, map interactions).

## Purpose
Provide the event taxonomy, payload schema, data pipeline design, metrics & acceptance criteria required by Design, Frontend, Backend, and Analytics teams so UX trade-offs can be evaluated and implemented without repeated back-and-forth.

## High-level decisions (made now)
- Use event-driven instrumentation: frontend posts JSON events to a single ingest endpoint (POST /api/v1/events).
- user_id is nullable: allow anonymous (guest) flows; require anonymous_id + session_id for attribution.
- Do NOT include raw PII (email, phone) in event payloads. Booking events reference booking_id which the backend maps to PII in a secure service.
- Raw events retained 90 days; aggregated/warehouse models retained 2+ years.
- Warehouse: BigQuery (preferred) or Snowflake. Transform layer: dbt.

## Event taxonomy (core events)
- page_view
- search_submit
- search_results_view
- product_select (flight_select / hotel_select)
- add_to_cart
- checkout_start
- guest_checkout_start
- signup_start
- signup_complete
- login
- payment_attempt
- booking_complete
- booking_cancel
- payment_failure
- map_interaction (subtypes: pan, zoom, select, cluster_expand)
- promotion_view
- promotion_click
- error

## Event payload (required fields)
All events must include the following base fields:
- event_name (string)
- timestamp (ISO 8601 UTC)
- anonymous_id (string) — client-generated UUID for anonymous users
- session_id (string)
- user_id (string|null) — internal user id once authenticated
- platform (web|ios|android)
- app_version
- locale
- currency

Common optional fields (depending on event):
- search: origin, destination, depart_date, return_date, pax_adults, pax_children, cabin_class
- product_select: product_type (flight|hotel), product_id, price, currency, fare_class
- checkout_start / guest_checkout_start: cart_id, cart_value, guest_email_collected (bool)
- booking_complete: booking_id (opaque), booking_value, payment_method, booking_source (web|app)
- map_interaction: map_event (pan|zoom|select), bbox (lat/lon box), center, zoom_level, result_count
- error: error_code, error_message, stacktrace (truncated)

PII handling
- Do NOT send emails, phone numbers, or payment details in events.
- If guest email is absolutely required for UX (e.g., to send e-ticket), send it to backend via a separate secure API that returns booking_id; only booking_id is included in analytics events.
- Backend must store PII in a secure vault; analytics maps booking_id → non-PII attributes only.

## Metrics & Reports (MVP)
- Funnel: search_submit → product_select → checkout_start → booking_complete (overall & by platform)
- Guest vs Signed-up conversion: compare booking conversion rates for guest_checkout_start vs signup_complete flows
- Map engagement: map_interaction events / session, avg zoom_level, conversions coming from map searches
- Revenue: bookings per day, ARPU
- Error rate: payment_failure rate, % of sessions with an error

## Acceptance criteria (for instrumentation & pipeline)
1. End-to-end event ingestion working for all core events in staging: frontend → ingest endpoint → raw events storage → transformed table in warehouse.
2. Example dashboards available: funnel conversion + guest-vs-signed conversion + map engagement.
3. Missing required fields alert: if >1% of events are missing required base fields for 24h, a pager alert triggers.
4. No raw PII present in analytics tables.

## Data pipeline (overview)
- Source: Frontend apps (web, iOS, Android) post to ingest endpoint or use Segment.
- Ingest: API writes raw JSON to object store (GCS/S3) partitioned by date and platform.
- Load: Streaming or batched load into raw_events table in BigQuery.
- Transform: dbt models to produce analytics.tables: events_staged, events_canonical, bookings_summary, funnel_aggregates.
- Consumption: Looker/Metabase dashboards and export for ML team.

Operational requirements
- Schema registry for events (versioned). Any new required field must be announced.
- Validation: lightweight schema validation at ingest (reject/flag malformed). Store raw rejected events for inspection.
- Monitoring: count per event, missing_fields_pct, pipeline latency, failed loads.

Estimated volume & cost
- MVP estimate: 100k events/day (~3M/month). Typical event size 1KB → 3GB/month raw. Scales linearly with users.

Open UX questions for Design (please answer)
1. Guest checkout: Do we require email at time of booking or allow a pure guest flow where we ask email after booking (e.g., on confirmation page)?
   - If email required at booking, analytics needs to capture guest_email_collected flag and an explicit mapping flow to booking_id.
2. Signup friction: Should we offer social login or passwordless email link? Each has different analytics needs (oauth provider, token flow success).
3. Map behavior: Should map selections open a detail modal (counts as product_select) or navigate to search results? Define expected user path so instrumentation can track conversion attribution.

Next steps / responsibilities
- Backend (Marcus): implement ingest endpoint + persistent storage for raw events; ensure no PII in events and booking_id mapping.
- Frontend (Kevin): implement event emission per taxonomy and include anonymous_id/session_id generation.
- Design (Maya): confirm UX answers above and indicate where email is collected or signup gate exists.
- Data (Samantha): implement ingestion pipeline and dbt models; produce dashboards.

Contacts
- Data: Samantha (this doc owner)
- Backend: Marcus
- Frontend: Kevin
- Product: Alex


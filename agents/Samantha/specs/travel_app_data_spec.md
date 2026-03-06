# Travel App — Data & Tracking Specification

## Situation
The Travel App PRD and epic for the MVP are ready. Design will produce wireframes for Home/Discovery, Search, Itinerary Builder, and Booking Checkout. We must ensure the product is instrumented and the data platform can support analytics, ML, and monitoring prior to frontend/backend builds.

## Complication
Design-first approach means frontend will be implemented against prototypes; without a clear data contract and event schema we risk rework, missing metrics, and inconsistent instrumentation across mobile/web.

## Resolution (deliverable)
I created a data & tracking specification and sample analytics SQL to unblock backend and analytics work:
- Data model: event-driven analytics (central `events` table), partitioned and clustered for performance.
- Tracking plan: canonical event names + required properties for Home/Discovery, Search, Itinerary Builder, Booking Checkout.
- Data governance: PII handling, retention, schema versioning, QA checks, monitoring.

Files created:
- output/specs/travel_app_data_spec.md
- output/code/data/travel_app_analytics.sql

---

## Core ask (restated)
Provide a clear, implementable data contract and analytics queries so backend (Marcus) can instrument events and data engineering (Samantha) can ingest, transform, and expose datasets to frontend, ML, and growth.

## MECE breakdown (assigned owners)
1) Event definitions & tracking plan — Samantha (Data Engineer) [this file]
2) Backend event emission & API hooks — Marcus (Backend) — NEXT HANDOFF
3) Frontend event mapping & sample SDK calls — Kevin (Frontend)
4) Data ingestion, ETL/ELT, and monitoring — Samantha (Data Engineer)
5) ML dataset exports & labeling pipeline — Lisa (ML) (not started until events available)

## Decisions made (so they are explicit)
- Warehouse: BigQuery chosen (reason: streaming ingestion, partitioned tables, low ops). This is reversible; Snowflake is an alternative if infra prefers it. (Trade-off: Snowflake has different streaming semantics.)
- Event model vs. many normalized tables: pick event model for mobile-first, flexible product metrics and ML features.
- PII: do not store raw emails/phone numbers in events. Send hashed/pseudonymized values only when necessary.

## Event taxonomy (canonical names + required properties)
Each event includes these base properties (required):
- event_name (STRING)
- event_timestamp (TIMESTAMP)
- user_id (STRING, nullable) — internal user id when logged in
- anon_id (STRING) — UUID for anonymous sessions
- platform (STRING) — 'ios' | 'android' | 'web'
- app_version (STRING)
- session_id (STRING)
- locale (STRING)
- device_info (RECORD) — os, model
- experiment_id (STRING, nullable)
- metadata (RECORD, nullable) — free-form JSON

Domain events (examples + required properties):
1) discovery_view
   - context: home | category | curated
   - items_shown: ARRAY<STRING> (ids)

2) discovery_card_impression
   - card_id
   - rank
   - section

3) search_initiated
   - query_text
   - origin (home | search_page)
   - filters (RECORD)

4) search_result_clicked
   - query_text
   - result_id
   - position

5) itinerary_created
   - itinerary_id
   - source (search | suggestion | import)

6) itinerary_item_added
   - itinerary_id
   - item_type (flight | hotel | activity)
   - item_id
   - price_local
   - currency

7) booking_initiated
   - itinerary_id
   - total_price_local
   - currency

8) booking_payment_success
   - booking_id
   - itinerary_id
   - payment_method (card | apple_pay | google_pay)
   - revenue_local
   - currency

9) booking_payment_failed
   - booking_id (nullable)
   - error_code
   - error_message (truncate)

Instrument additional technical events: session_start, session_end, app_crash, network_error.

## Data model (high level)
- Raw events ingestion: all events streamed into `raw.events_{YYYYMMDD}` or `events_raw` (partitioned) with append-only write.
- Core analytics view: `analytics.events` (cleaned, typed, enriched: geo, currency normalization, attach user_profile_id)
- Aggregates & marts: `analytics.metrics_*` (DAU, funnels, booking_revenue)
- ML dataset exports: `ml.user_behavior_features` (pre-aggregated windows)

Table design notes (BigQuery):
- Use ingestion-time partitioning: PARTITION BY DATE(event_timestamp)
- Cluster by user_id, event_name for faster filtering
- Use schema versioning: event_schema_version in root record

## ETL & quality checks
- Required checks on each batch/stream: schema conformance, null rates for required fields, event volume delta (alerts if >50% drop), late arrival rate.
- Implement Great Expectations or custom SQL-based checks; alert to Slack + PagerDuty on P0 failures.

## Privacy & retention
- PII: do not transmit raw PII fields. If necessary, send sha256(email) and mark as pseudonymized.
- Retention: 365 days default; aggregated metrics older than 3 years can be archived.

## Acceptance criteria (how we'll know it's done)
1) Backend emits the canonical events for the four flows (Home, Search, Itinerary, Booking) with required properties.
2) A streaming ingestion pipeline is writing to BigQuery (or equivalent) into partitioned `events` dataset.
3) Basic QA checks pass on first week's data (schema conformance, row counts >0, user_id mapping present when logged in).
4) Example analytics queries (DAU, funnels) run within SLAs (expected <5s on sample data)

## Next steps & owners
- Marcus (#ai-backend) — implement server-side event emission and streaming to the warehouse. See handoff.
- Kevin (#ai-frontend) — implement frontend SDK calls for events using the canonical event names and properties in this doc.
- Noah (#ai-devops) — provide credentials + secure ingestion path to BigQuery and verify network configuration.
- Samantha (Data) — build ingestion jobs, transform to `analytics.events`, and create dashboards.

## Notes & gotchas
- Ensure both user_id and anon_id are always emitted for sessions started anonymously then converted to logged-in state.
- Timezones: store event_timestamp in UTC; provide event_date derived field for partitioning.
- Currency normalization: store local currency and a normalized USD amount in analytics layer.


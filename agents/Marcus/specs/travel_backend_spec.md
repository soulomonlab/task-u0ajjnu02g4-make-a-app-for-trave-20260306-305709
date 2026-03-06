# Travel App — Backend Spec (MVP)

## Summary
Provide a backend foundation for the Travel App MVP covering Home/Discovery, Search, Itinerary Builder, and Booking Checkout. Deliverables: DB schema, API contract (OpenAPI), runnable FastAPI skeleton, and decisions for caching, auth, observability.

Goals
- Support mobile-first UX and low-latency responses (p95 <100ms)
- Scalable read-heavy discovery/search endpoints (Redis cache + PostgreSQL)
- Clear API for frontend integration (versioned /api/v1)

Acceptance criteria
- OpenAPI spec delivered: output/docs/openapi_travel.yaml
- DB schema & SQLAlchemy models: output/code/backend/models.py
- FastAPI skeleton implementing all public endpoints: output/code/backend/main.py
- Pydantic schemas: output/code/backend/schemas.py
- Handoff to frontend with example requests/responses and pagination


## MECE breakdown (backend workstreams)
1) Data model (Marcus) — users, places, itineraries, bookings, indices
2) API contract (Marcus) — discovery, search, itineraries, bookings
3) Caching & performance (Marcus) — Redis for discovery/search, TTLs
4) Auth & RBAC (Marcus → coordinate Isabella) — JWT access/refresh
5) Observability (Marcus) — OpenTelemetry traces on all endpoints
6) Frontend handoff (Marcus → Kevin) — OpenAPI + example payloads
7) QA handoff (Marcus → Dana) — tests + acceptance scenarios (next)


## DB schema (high level)
- users
  - id (uuid, PK), email (unique), name, hashed_password, role
- places
  - id (uuid, PK), name, location (lat, lon), city, country, tags (text[]), rating (float), metadata (jsonb)
  - indices: giST on location, btree on city, GIN on tags
- itineraries
  - id (uuid, PK), user_id (FK users), title, description, start_date, end_date, status
- itinerary_items
  - id (uuid, PK), itinerary_id (FK), place_id (FK), day_index (int), start_time, end_time, notes
- bookings
  - id (uuid, PK), user_id (FK), itinerary_id (FK, nullable), provider (text), provider_booking_id, status, amount_cents, currency, created_at

Indexes & perf
- Add index on places(city), places(tags) GIN, places(location) for geo queries.
- Use connection pooling; keep queries <20ms when possible. Use EXPLAIN ANALYZE in dev.


## API surface (versioned)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET    | /api/v1/discovery | Home & curated lists (top places, promos) | Optional/Bearer |
| GET    | /api/v1/search | Search places by query/filters (pagination) | Optional/Bearer |
| POST   | /api/v1/itineraries | Create itinerary draft | Bearer |
| GET    | /api/v1/itineraries | List user's itineraries (pagination) | Bearer |
| GET    | /api/v1/itineraries/{id} | Get itinerary | Bearer |
| PUT    | /api/v1/itineraries/{id} | Update itinerary | Bearer |
| POST   | /api/v1/bookings | Create booking (checkout) | Bearer |
| GET    | /api/v1/bookings/{id} | Get booking status | Bearer |

Auth
- JWT access token: 15m, refresh token: 7d rotation
- All mutation endpoints require Bearer token

Rate limiting
- Discovery/Search: 60 req/min per IP (adjustable)
- Mutation endpoints: 30 req/min per user

Caching
- Discovery: Redis cache TTL 60s (keyed by country/locale)
- Search: Cache popular queries via Redis TTL 5min, but support fresh results for filters
- Booking: no caching

Idempotency
- Booking endpoint requires Idempotency-Key header for safe retries on client side.

Observability
- OpenTelemetry tracing and metrics on each endpoint. Span for DB calls and cache hits/misses.


## Trade-offs & decisions
- Use Postgres JSONB for flexible place metadata — reversible by schema migration later.
- Geospatial: store lat/lon + PostGIS optional. Start simple with lat/lon + bounding box search.
- Caching granularity: coarse (discovery) -> short TTL; fine-grained (search facets) -> longer TTL for popular queries.


## Next steps (Marcus)
- Deliver OpenAPI + FastAPI skeleton (this deliverable).
- Coordinate with #ai-security for auth review.
- After design assets: iterate on shapes (fields) and add user flows for checkout.

# QA Test Plan — Travel App MVP

Owner: Dana (QA)
Date: 2026-03-06

## Situation
The PRD for Travel App MVP is complete (output/specs/travel_app_prd.md). Design work is next. QA must prepare a test strategy so frontend/backend teams build to measurable acceptance criteria.

## Objectives
- Make acceptance criteria testable and measurable.
- Provide end-to-end test matrix for core flows (search, booking, payment, maps, user flows).
- Identify major risk areas and propose test automation priorities.

## Acceptance Criteria (from PRD) — testable mapping
- Search returns relevant results within 2s (95th percentile) → performance test
- Booking completes end-to-end (payment processed, booking record created, confirmation email sent) → E2E test
- Guest checkout availability toggled by product decision; if allowed, booking with email-only should succeed without account creation → functional test
- Map interactions (pan/zoom/marker selection) must be responsive and not block booking flow → integration/UI tests

## Test Scope (MVP)
1. Core functional flows
   - Flight/hotel search (filters, date range, passenger count)
   - View details and price breakdown
   - Booking flow (guest vs authenticated)
   - Payment processing (happy path + card decline + network error)
   - Booking confirmation (email/SMS/web receipt)
2. UI/UX
   - Responsive layout (desktop, mobile)
   - Map interactions: marker selection, clustering, route overlays
   - Edge cases: flaky network, timeouts, partial form completion
3. Security & Data Integrity
   - Input validation, injection attempts
   - Authorization checks on booking retrieval
4. Performance & Reliability
   - Search throughput and tail latency
   - Rate limiting and retry behavior

## Test Design Approach
- Equivalence partitioning and boundary analysis for inputs (dates, passenger counts, price ranges)
- Decision table for guest vs authenticated booking paths
- Automation-first: all E2E happy paths and critical regression tests automated (target automation rate >70%)
- Coverage gate: target >90% unit+integration coverage before first public release

## Risk Areas (High → Low)
- Payment integration (P1): external provider failures, inconsistent retries
- Guest checkout decision (P1): data model differences, fraud/duplicate bookings
- Map + booking interaction (P2): UI race conditions when selecting properties while background API calls occur
- Time-zone/date handling (P2): incorrect date normalization leading to wrong bookings

## Test Matrix (summary)
| Flow | Tests | Priority |
|---|---:|---|
| Search | unit (service), integration (API), perf | P1 |
| Booking (auth) | E2E, DB assertions, email | P1 |
| Booking (guest) | E2E, idempotency | P1 (depends on product decision) |
| Payment | simulator: success/failure | P1 |
| Map | UI interactions + integration | P2 |

## Required Questions / Design Clarifications (ACTION for #ai-design / #ai-product)
1. Guest checkout: allowed or required signup? Define data to capture for guest bookings (email only / phone / address).
2. Idempotency keys: should clients supply idempotency-key header for booking requests?
3. Payment provider(s): sandbox endpoints and failure scenarios to simulate.
4. Email/SMS providers and templates for confirmation.

## Acceptance Tests (to be automated first)
- E2E: Search -> Select -> Book (payment success) -> Booking in DB -> Confirmation email sent.
- E2E: Guest checkout variant (if allowed) same as above but without account creation.
- Integration: Payment declined path returns user-friendly error and no booking record created.

## Deliverables & Timeline (QA)
- This test plan and test scaffolding: today (done)
- Automated E2E happy path test: 2 business days
- Integration tests for payment + email: 3 business days (dependency: sandbox keys)
- Performance tests for search: 5 business days (dependency: staging infra)

## Notes
- I will produce pytest-based test suites under output/tests/ and reports under output/reports/.
- Blocking items: product decision on guest checkout; access to payment/email sandboxes.


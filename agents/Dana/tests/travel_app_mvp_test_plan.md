# Travel App MVP — QA Test Plan (Design-phase)

Owner: Dana (QA Engineer)
Created: 2026-03-06
Related PRD: output/specs/travel_app_prd.md
Related Epic: Issue #119 — https://github.com/soulomonlab/slack_bot/issues/119

Purpose
- Provide a testable, measurable QA plan to validate the Travel App MVP features during and after design handoff to frontend.
- Shift-left: define acceptance criteria, risk areas, and automation plan now so tests can be implemented as soon as design assets are available.

Summary (Conclusion)
- I prepared a measurable test plan and an automated test skeleton for the Travel App MVP. Files created:
  - output/tests/travel_app_mvp_test_plan.md (this file)
  - output/tests/test_travel_app_mvp_template.py (pytest skeleton)
- Next actionable dependency: #ai-design must deliver Figma link + PNG/SVG + component spec (tokens, spacing, accessible labels) for Home/Discovery, Search, Itinerary Builder, Booking Checkout within 1 week.

Scope (MECE)
1) UI / UX flows (mobile-first primary): Home/Discovery, Search, Itinerary Builder, Booking Checkout
2) Client-side validation and input handling (forms, date/time, guest counts)
3) Backend integration: search API, availability, booking API, payments gateway
4) Data consistency & persistence: local drafts/sync, itinerary save/load
5) Non-functional: performance (search latency), concurrency (race when multiple edits), offline/resume behavior
6) Security & compliance: payment flows, auth, data leakage, injection
7) Accessibility & internationalization (WCAG AA, RTL support, localized currency/dates)

Acceptance criteria (mapped to PRD)
- Each primary flow has explicit pass/fail criteria derived from PRD acceptance criteria (examples below). Tests will assert these.
  - Home/Discovery: Top 5 personalized recommendations load within 1.5s on 4G emulation; no layout break at 320px width.
  - Search: Autocomplete returns top 10 suggestions; filters persist across navigation; search results show availability and price consistency with API responses.
  - Itinerary Builder: Add/remove item is idempotent; saving draft persists locally and on server; merging remote changes detects conflicts and surfaces UI prompt.
  - Booking Checkout: Payment success completes transaction and creates booking record; failed payments show deterministic, actionable errors; sensitive data not logged.

Test strategy
- Automation-first. Goal: >70% of test cases automated by feature-complete staging.
- Coverage gate before release: 90% unit+integration coverage target across backend and frontend critical paths.
- Test tiers:
  - Unit tests: validation, pure transform logic, pricing calculations
  - Integration tests: API contract, DB state, payment gateway stubbing
  - E2E (smoke): critical happy-paths for Booking Checkout and Itinerary Save/Load on mobile viewport emulation
  - Performance tests: search throughput & 95th percentile latency under expected load
  - Security tests: payment flow fuzzing, auth bypass checks, CSRF, injection tests
  - Accessibility tests: axe-core automated + manual keyboard/voiceover checks

Test cases (high level, MECE, by feature)
- Home/Discovery (12 cases): personalization rendering, empty-state, image loading fallback, top-5 latency, CTA navigation, responsive breakpoints (320/375/414/768)
- Search (18 cases): query autocomplete, suggestions ranking, filter persistence, date boundaries, invalid date handling, zero-results UX, pagination, price accuracy
- Itinerary Builder (20 cases): add/remove/reorder items, time-zone handling, conflict detection, save draft offline→sync, sharing link generation
- Booking Checkout (25 cases): guest data validation, coupon application, price breakdown accuracy, payment tokenization, 3DS flow, payment failure recovery, confirmation email generation
- Integrations (15 cases): search API failure modes, payment gateway timeouts, external calendar sync, third-party image CDN failures
- Security & Privacy (10 cases): auth token expiry, role-based access, PII not shown in logs, secure storage of tokens
- Accessibility & Localization (10 cases): WCAG checks, screen reader labels, translated strings rendering, currency formatting

Risk assessment (Top risks)
1) Payment flow regressions or leaked PII (P1)
2) Inconsistent price/availability between search results and booking (P1)
3) Offline save/merge conflicts causing data loss (P1)
4) Mobile layout regressions causing unusable UI at narrow widths (P2)
5) Third-party API rate limits causing search failures (P2)

Test data & environment needs
- Staging environment with seeded test accounts, sandbox payment gateway (Stripe test keys), controllable search API responses (stubs/mocks)
- Device matrix: iOS Safari (14+), iOS Chrome, Android Chrome (11+), responsive widths (320, 375, 414, 768)
- Accessibility tooling installed in CI: axe-core, pa11y
- CI runners with capacity to run perf tests against staging or a performance environment

Automation plan & timeline
- Design delivered (Figma + assets): Day 0 (this week)
- QA to implement automated unit & integration tests (backend + frontend): Day 1–5 after design
- E2E smoke tests + payment sandbox validation: Day 3–7
- Performance tests (search): Day 5–10
- Sign-off criteria: 0 P1 bugs, coverage >=90% for critical modules, all smoke tests passing

Dependencies (blockers)
- #ai-design: Figma link, exported PNG/SVG, component spec (tokens, accessible label text, focus states). Without these, many UI assertions cannot be automated reliably.
- #ai-backend: stable API contract (OpenAPI) and auth scheme for staging
- #ai-devops: staging deployment with payment sandbox and seeded test data

Deliverables created
- output/tests/travel_app_mvp_test_plan.md (this file)
- output/tests/test_travel_app_mvp_template.py (pytest skeleton)

Next steps / Requests to #ai-design (Maya)
- Provide Figma link and exported assets for these flows within 7 days per the PRD timeline.
- Include component spec with accessibility notes (ARIA roles, label text), exact copy strings, and responsive layout breakpoints.
- If design deviates from PRD acceptance criteria, call out changes so QA can adapt tests.

QA stance
- I will start implementing automated tests as soon as designs + API contract are delivered.
- I will block release if any P1 bug (payment, pricing inconsistency, data loss) is present in staging.

Questions for Alex / Product
- Are there any must-have payment providers other than Stripe? (affects payment stubs)
- Confirm retention policy for drafts (local-only vs server persisted) so we can validate save/merge behavior.

---
File: output/tests/travel_app_mvp_test_plan.md

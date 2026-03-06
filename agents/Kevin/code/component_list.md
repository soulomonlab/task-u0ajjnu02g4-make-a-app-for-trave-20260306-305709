Overview

This document lists frontend components required for the Travel App MVP (mobile-first). It maps screens → components → minimal props/data shape → backend endpoint(s) required. It also records key frontend decisions and a rough effort estimate.

Design reference: output/specs/travel_app_prd.md (PRD) and expected design assets from Maya (hi-fi screens + tokens).

Decisions (frontend)
- State: use Zustand for global client state (auth/session, shopping cart/itinerary draft). Use React Query for server state (lists, search results, detail fetches). Rationale: React Query handles caching, background refresh, and pagination cleanly; Zustand keeps small, synchronous client-only state.
- Styling: Tailwind CSS (project stack). Component tokens will be wired to design tokens when Maya delivers them.
- Accessibility: keyboard support for search/typeahead, screen-reader labels, ARIA live regions for toasts, focus trap for modals.

Screens & Components

1) Home / Discovery
- Components:
  - DiscoveryFeed
    - Props: { initialCursor?: string, pageSize?: number }
    - APIs: GET /items?cursor={cursor}&limit={pageSize} (cursor pagination)
    - Behavior: infinite scroll loadNext (React Query cursor-based); show skeleton items while loading.
  - FeaturedCarousel
    - Props: { items: Array<{id,title,image_url}> }
    - APIs: GET /featured
  - DestinationCard
    - Props: { id, title, short_description, thumbnail_url, price_from }
    - Click -> navigates to Destination Detail screen

2) Search (global header + dedicated page)
- Components:
  - GlobalSearchInput
    - Props: none
    - Behavior: debounce 300ms, keyboard nav (ArrowUp/Down/Enter/Escape), ARIA listbox semantics, show up to 10 typeahead results with 'See more' link
    - APIs: GET /api/v1/search?q={q}&limit=10
  - SearchResultsPage
    - Props: { query, filters }
    - APIs: GET /search?q=...&filters=...&cursor=... (cursor pagination). Optional include_total param only when explicit (expensive)
  - FilterPanel
    - Props: { appliedFilters, onChange }
    - Client-only filtering UI; server side filters passed to search endpoint

3) Itinerary Builder
- Components:
  - ItineraryEditor
    - Props: { draftId?: string }
    - APIs:
      - POST /itineraries (Create) — Idempotency-Key header for create
      - PATCH /itineraries/{id} (Update)
      - GET /itineraries/{id}
    - Behavior: local draft stored in Zustand; autosave debounce 2s -> PATCH; explicit Save triggers POST when new.
  - DayList / DayItem
    - Props: events array per day
  - AddBookingModal
    - Props: { onAdd }
    - Calls availability/pricing endpoints for selected booking

4) Booking Checkout
- Components:
  - CheckoutForm
    - Props: { itineraryId }
    - APIs:
      - POST /bookings  (Create booking) — requires Idempotency-Key; response includes booking_id, status, payment_instructions
      - GET /pricing?offer_id=... (pricing breakdown)
    - Responsibilities: Collect traveler info, payment method placeholder (external), show price breakdown and cancellaton policy
  - PaymentStatus / BookingConfirmation
    - Props: { bookingId }
    - APIs: GET /bookings/{id}

5) Auth & Onboarding (per core_flow_v1)
- Components:
  - SignupForm (data-testid: signup-form)
    - APIs: POST /auth/signup
  - LoginForm (data-testid: login-form)
    - APIs: POST /auth/token (returns access token + sets refresh cookie)
  - EmailConfirmation / Resend (data-testid: resend-email)

6) Common / Shared
- Components:
  - Toast / GlobalAlert (ARIA live region)
  - Modal (focus trap)
  - LoadingSkeleton
  - ErrorBoundary + ErrorScreen
  - Avatar / Image component with lazy loading and placeholder

API fields we need frontend confirmation on (blocking for accurate props)
- Search result item shape: fields required for UI (id, title, snippet/html_highlight, type, image_url, price_min, rating, location_name). Does backend return highlighted HTML or range offsets? (UI needs to know whether to render HTML or apply client highlight.)
- Cursor pagination shape: { items: [], next_cursor?: string }. Confirm exact key names and whether items length==0 indicates end.
- Pricing response for bookings: need itemized breakdown (base_price, taxes_fees[], discounts[], currency, refundable boolean). Confirm field names and currency format.
- Availability: what shape for availability windows or slot IDs used by booking endpoint.
- Booking create response: booking_id, status(enum: pending/confirmed/failed), next_action (e.g., payment_url), and when/how to poll for final status.
- Idempotency: confirm server accepts Idempotency-Key header for POST /bookings and returns 409 vs idempotent 200 for retries.

Acceptance & QA considerations
- Provide data-testid attributes as specified in design/core_flow_v1.md.
- Keyboard-first Nav for search (Arrow keys, Enter to open result; Escape to dismiss).
- Offline / Network error states: clear retry affordances.

Effort estimate (rough, person-days)
- Component library & tokens integration: 3 PD
- Home/Discovery screens: 3 PD
- Search (global + results page + keyboard nav): 4 PD
- Itinerary Builder (core flows + autosave): 5 PD
- Booking Checkout (forms, pricing, booking flow): 4 PD
- Auth + Onboarding screens: 2 PD
- QA fixes & accessibility: 2 PD
Total: ~23 person-days (MVP scope). Adjust after design tokens and API confirmation.

Next steps for frontend (Kevin)
1) Wait for Maya's hi-fi screens + tokens (Figma link) to implement exact spacing/colors.
2) Marcus: confirm the API field shapes listed above and cursor pagination keys.
3) Start branches: feat/component-library and feat/search-mvp once APIs confirmed.


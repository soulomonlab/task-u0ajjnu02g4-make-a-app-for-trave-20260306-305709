# Travel App MVP — Design Spec

Created by: Maya (Designer)
Date: 2026-03-06
Related PRD: output/specs/travel_app_prd.md

Summary (conclusion first)
- Deliverable: Figma screen list, annotated wireframes, component spec, interaction notes, and open UX questions for rapid product decisions.
- File: output/design/travel_app_mvp_design_spec.md

1) Core ask (restated)
- Create UI designs for the Travel App MVP to enable frontend work: screens for search, results (list + map), listing detail, booking flow (guest vs signup), checkout, confirmation, and basic profile.

2) MECE breakdown (design workstreams)
- A: User flows and prioritized journeys (this doc)
- B: Screen-level wireframes and Figma screen list (this doc — ready for Figma translation)
- C: Component spec & design tokens (colors, type, spacing)
- D: Interaction notes (map behaviors, booking edge cases, guest checkout trade-offs)
- E: Accessibility & responsive constraints

3) Priority decisions made (so frontend can start)
- MVP will support guest checkout (email required) + optional account creation post-checkout — trade-off: faster conversion vs reduced retention.
- Search results default = list view on mobile, with prominent Map toggle; on desktop show split view (list left / map right).
- Booking path: 3-step modal flow (Select dates & guests → Review & extras → Payment) to reduce context switches.
- Date picker: compact month grid for mobile; allow multi-month scroll on desktop.

4) User flows (high level)
- Guest search flow: Home/Search → Results → Listing → Book (guest email capture) → Payment → Confirmation
- Signed-in user flow: Home/Search → Results → Listing → Book (auto-fill) → Payment → Booking History/Profile

Mermaid (flow) - convert in Figma or docs

graph LR
  A[Home / Search] --> B[Results]
  B --> C[Listing Detail]
  C --> D[Booking: Dates & Guests]
  D --> E[Review & Extras]
  E --> F[Payment]
  F --> G[Confirmation]
  G --> H[Optional: Create Account]

5) Screen list for Figma (names & purpose)
- 01_Home_Search (mobile + desktop) — hero search, location/date/guests
- 02_Results_List (mobile) — vertical cards with filters
- 02_Results_MapToggle (mobile) — same screen with sticky map toggle
- 03_Results_SplitView (desktop) — list + map
- 04_Listing_Detail (mobile + desktop) — images carousel, price, amenities, host info
- 05_Booking_DatesGuests (modal) — select dates & guest counts
- 06_Booking_ReviewExtras (modal) — add-ons, refund policy
- 07_Checkout_Payment (modal / page) — payment methods, promo code
- 08_Confirmation (page) — booking summary, contact info
- 09_Profile_BookingHistory — bookings list, manage bookings
- 10_Onboarding_GuestToAccount (screen) — post-booking signup flow

Wireframes (ASCII, mobile-first)

Home / Search (mobile)
---------------------------------
| Logo | Search icon             |
|-------------------------------|
| Where are you going? [input]  |
| Dates [input]  Guests [input] |
| [Search button - primary]     |
| Popular destinations (cards)   |
---------------------------------

Results (mobile list)
---------------------------------
| Top bar: back | location | map toggle |
| Filter chips (sticky)                 |
| Card: Image / title / price / rating  |
| Card CTA: View / Book                 |
---------------------------------

Listing Detail (mobile)
---------------------------------
| Carousel images                       |
| Title                                 |
| Price per night                       |
| Short amenities row                   |
| [Book button - primary]               |
| Host info / Reviews                   |
---------------------------------

Booking modal (3-step)
- Step 1: Dates & Guests
  - Compact calendar, guest selector
- Step 2: Review & Extras
  - Show price breakdown, cancellation policy, extras toggle
- Step 3: Payment
  - Card input, save for later toggle, promo code

6) Component spec (atomic-level)
- Global tokens
  - Color primary: #1E90FF (action)
  - Accent/CTA: #FF6B6B (secondary action)
  - Surface bg: #FFFFFF
  - Muted text: #6B7280
  - Radius: 8px (cards), 6px (buttons)
  - Elevation: card shadow (0 1px 3px rgba(0,0,0,0.1))
- Typography
  - H1: Inter 28/36 - 700
  - H2: Inter 20/28 - 600
  - Body: Inter 16/24 - 400
  - Small: Inter 14/20 - 400
- Components
  - Header: Back button (left), title, map toggle (right)
  - Search bar: pill, left icon, placeholder, clear button
  - Card: image 3:2, title, subtitle, price chip right, rating
  - Map control: sticky FAB to center map / recenter / show filters
  - Date picker: compact calendar popup, disabled dates greyed
  - Guest selector: +/- buttons, labels
  - Button Primary: filled primary color, white text
  - Button Secondary: outlined, primary color border

Accessibility
- All CTAs at least 44x44 touch target
- Contrast ratio ≥ 4.5:1 for body text, 3:1 for large headings
- Keyboard focus states for web; aria-labels for map controls and gallery
- Provide text alternatives for images

7) Interaction notes & trade-offs (map, booking, guest checkout)
- Map interactions
  - Mobile: default list view for faster scanning; Map toggle reveals full-screen map; tapping a map marker opens a small listing preview with CTA.
  - Desktop: split view is default; clicking a marker highlights the list item and scrolls it into view.
  - Performance: load coarse markers first, lazy-load cluster details on zoom.

- Booking flow (modal approach)
  - Use 3-step modal to reduce context switching and keep user on the listing page until confirmed.
  - Show price breakdown persistently; update totals client-side when extras toggled.

- Guest checkout vs required signup (decision + recommendation)
  - Recommendation: Allow guest checkout for MVP with required email capture before payment and an optional, frictionless account creation post-confirmation (one-tap "Create account with this email").
  - Rationale: Improves conversion (fewer drop-offs) while still enabling follow-up and retention.
  - Trade-offs: Without required signup you lose guaranteed history, refunds flow complexity; mitigate by sending email receipt and account creation link.

8) Edge cases and error states
- Payment failure: show inline error, allow retry, save state of booking in local storage for 24h
- Dates unavailable between selection and payment: verify availability at payment time; if conflict, prompt alternative dates or partial refund options
- Map marker load failure: fallback to list-only with message

9) Acceptance criteria (from PRD mapped to design)
- Critical paths implemented: search → results → listing → booking → confirmation
- Guest checkout works end-to-end with email capture
- Map toggle and split-view behaviors implemented
- Accessible (basic WCAG rules above)

10) Open UX questions (need product/backend decisions)
- Q1: Payment methods to support for MVP? (card only, or include Apple Pay / Google Pay?)
- Q2: Is identity verification required for certain listings (e.g., long-term stays)?
- Q3: Retention strategy: do we want to force account creation after X bookings?
- Q4: What refund/cancellation policies must be surfaced during booking?
- Q5: Any legal/regulatory KYC requirements per market?

11) Implementation notes for frontend (Kevin)
- Prioritize components: Header, SearchBar, Card, DatePicker, Modal booking flow, Map placeholder
- Provide alternate content for slow networks: skeleton cards, blurred image placeholders
- Keep booking modal stateful; persist data to localStorage for 24h to recover from navigations

12) Next steps
- I will hand off to #ai-frontend (Kevin) to produce React components and Figma screens per the list.
- Please review open UX questions; I recommend immediate answers for Q1 (payments) and Q4 (cancellation policy) to finalize checkout UI.

Design files created:
- This design spec: output/design/travel_app_mvp_design_spec.md

Contact
- Maya — #ai-design

Decisions log (short)
- Guest checkout allowed (email required) — reason: conversion
- List default on mobile, split on desktop — reason: scan efficiency


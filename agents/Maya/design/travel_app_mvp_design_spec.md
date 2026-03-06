# Travel App MVP — Design Spec

## Summary
Deliver high-fidelity, mobile-first designs and interaction flows for the Travel App MVP screens: Home/Discovery, Search, Itinerary Builder, Booking Checkout. This document defines user flows, mobile-first wireframes, component specifications, visual tokens, accessibility notes, deliverables, and a 1-week work plan for handing off to frontend.

Reference: PRD created at output/specs/travel_app_prd.md (goals, acceptance criteria, success metrics).

---

## Scope (MVP screens)
- Home / Discovery (feed of curated destinations & deals)
- Search (destination + date + passenger filters + results list + map)
- Itinerary Builder (add/remove days, drag & drop activities, timeline)
- Booking Checkout (review trip summary, passenger info, payment, confirmation)

Excluded (out of scope for MVP): multi-currency, advanced loyalty integration, deep personalization.

---

## Constraints & Principles
- Mobile-first, then tablet/desktop responsive.
- Performance: low-CPU animations, lazy-loaded images.
- Accessibility: WCAG AA baseline, tappable targets >= 44px.
- Reusable component system (cards, list items, form elements).
- Keep flows < 5 primary taps/screens for key tasks (search → book).

Design decisions (quick rationale)
- Card-based feed for Discovery: fast scannability and easy progressive disclosure.
- Bottom navigation with primary actions: Home, Search, Trips, Profile — mobile ergonomic.
- Itinerary Builder uses drag-and-drop list + compact day chips to reduce cognitive load.
- Checkout is a single-column vertical flow to reduce errors on mobile.

---

## Personas & Key Jobs
- Leisure Planner (primary): ages 25–45, plans 1–2 trips/year, seeks inspiration + simple booking.
- Business Traveler (secondary): cares about speed and confirmations.

Primary user goals mapped to screens:
- Find inspiration → Home/Discovery
- Find and filter options quickly → Search
- Build and organize a day-by-day plan → Itinerary Builder
- Complete booking with minimal friction → Booking Checkout

---

## User Flows (high level)
1) Discovery → Search → Result → Itinerary Builder → Checkout
   - Home tap on destination card → Destination details modal → Start trip (calls Search)
   - Search results tap “Add to itinerary” → choose day → added to Itinerary
   - From Itinerary: reorder activities (drag), save, then Proceed to Book
   - Checkout: enter passenger details → payment → confirmation

2) Quick Book (fast path)
   - Search results > Quick Book button → pre-filled checkout (1-screen) → confirm

Each flow includes error states (no results, payment failure), and lightweight inline help.

---

## Wireframes (mobile-first) — ASCII sketches
Note: these are structural wireframes for alignment. High-fidelity PNG/SVG and Figma file will follow.

1) Home / Discovery (mobile)
[Top nav: logo | search icon]
[Hero carousel: curated destinations]
[Section: Trending deals horizontal scroll (cards)]
[Section: Categories: icon chips (Beaches, Cities, Adventure)]
[Bottom nav: Home | Search | Trips | Profile]

2) Search (mobile)
[Back | Search input (destination) | date chip | pax chip]
[Filters: price, duration, stops (collapsible)]
[Results: vertical list of ResultCard — image, title, price, time, action buttons (Add / Book)]
[Map toggle floating action button]

3) Itinerary Builder (mobile)
[Header: Trip Title | Edit]
[Day chips horizontally scrollable: Day 1 | Day 2 | + Add Day]
[Timeline list: Activity Row (time | title | location | drag handle | remove)]
[FAB: Save / Proceed to Checkout]

4) Booking Checkout (mobile)
[Progress indicator: Contact → Passengers → Payment → Review]
[Form: contact fields collapsed, passenger list, add passenger button]
[Payment: card entry or saved methods][Promo code input]
[Price summary card sticky at bottom with Confirm & Pay CTA]

Mermaid interaction map (basic)

flowchart LR
  Home --> Search
  Search --> Results
  Results --> Itinerary
  Itinerary --> Checkout
  Checkout --> Confirmation

---

## Component Specs (tokens + components)
Design tokens (mobile baseline):
- Colors:
  - Primary: #0B72FF (brand action)
  - Secondary: #00BFA6
  - Background: #FFFFFF
  - Surface: #F7F8FA
  - Text primary: #0F1724
  - Text secondary: #6B7280
  - Error: #E02424
- Typography:
  - H1 (mobile): 20px / 28px / 600
  - H2: 16px / 24px / 600
  - Body: 14px / 20px / 400
  - Caption: 12px / 16px / 400
- Spacing scale: 4, 8, 12, 16, 20, 24, 32
- Border radius: 12px for cards, 8px for buttons

Core components (props & behavior):
1) ResultCard
  - Image ratio 16:9, lazy-loaded
  - Title (H2, max 2 lines ellipsis)
  - Subtitle (location, small)
  - Price badge (right-aligned)
  - Actions: Primary (Add/Book) full-width small button, Secondary icon (save)
  - Tap area: whole card opens detail; primary action triggers booking flow

2) SearchBar
  - Placeholder: "Where to?" with microcopy for dates/pax
  - Autocomplete suggestions + recent searches
  - Accessible label announced

3) Day Chip
  - Text: Day #, selectable, focus ring
  - Overflow: + Add Day opens modal

4) Activity Row (Itinerary)
  - Drag handle on left; content: time, activity title, location; right: kebab menu
  - Swipe left to delete (confirm undo toast)

5) Bottom Price Summary
  - Sticky footer card with breakdown rows and CTA. CTA uses Primary color, min height 56px.

Animations & micro-interactions:
- Subtle elevation (shadow) for cards on press
- Dragging shows placeholder with slight scale and drop animation
- Error toasts at top (red background)

Accessibility notes:
- All images have alt text generated from title + location
- Buttons and actionable items meet contrast ratio 4.5:1
- Keyboard navigation & screen reader labels for complex components (itinerary drag handles, day chips)

---

## Edge Cases & Error States
- Search no results: show suggested destinations, expand radius, and contact support CTA
- Itinerary empty: CTA to "Add from Discovery" and template suggestions
- Payment declined: clear inline error, retry and contact options

---

## Assets & Deliverables (what I'll deliver in 1 week)
- High-fidelity PNG/SVG exports for each screen (mobile 375x812) — Home, Search, Itinerary, Checkout
- Component spec sheet (Figma components + tokens)
- Interactive prototype (Figma link) with key flows: Search → Add to Itinerary → Checkout
- Asset export package (icons SVG, images JPG/WEBP optimized)

Placeholder Figma file: https://www.figma.com/file/<<to-be-created>>/Travel-App-MVP (I will create and share link in 48 hours)

---

## Implementation Notes for Frontend
- Provide exact token names and CSS variables in the Figma tokens page
- Deliver components as React-ready atoms/molecules with states (default/hover/active/disabled)
- Use semantic HTML equivalents: lists, buttons, forms for better accessibility

---

## Timeline (1 week plan)
Day 0 (today): Confirm scope and constraints (this doc)
Day 1: Low-fidelity flows & wireframes (mobile)
Day 2-3: High-fidelity screens (Home, Search)
Day 4-5: High-fidelity screens (Itinerary, Checkout) + components
Day 6: Prototype, accessibility pass, export assets
Day 7: Final review, deliver PNG/SVG, Figma link, handoff to frontend

---

## Open questions / Need decisions from Product
1. Primary payment methods to support in MVP? (Card only vs. Apple Pay / Google Pay)
2. Required analytics events on booking flow (which steps, custom properties)
3. Any required legal copy (cancellations, T&Cs) to include in checkout?

---

## Acceptance Criteria (design-level)
- All four screens visually complete and exported (PNG/SVG)
- Figma file with components & tokens published and shared
- Prototype demonstrates the end-to-end flow
- Component spec includes spacing, colors, typography, interaction states

---

## Next steps (for frontend handoff)
- I will finalize Figma file and share link by Day 2.
- After exporting PNG/SVG and component specs, I'll hand off to #ai-frontend (Kevin) with implementation notes and token mapping.



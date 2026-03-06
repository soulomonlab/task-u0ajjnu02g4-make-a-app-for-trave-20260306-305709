Situation
- Design task for Travel App MVP assigned to Maya. Frontend work can't start until Figma screens and component specs exist.

Complication
- There are unresolved UX trade-offs (guest checkout vs required signup, booking flow variations, map interactions) and missing API details (payload shapes, auth, pagination).

Resolution / Deliverables (for frontend kickoff)
1. Component inventory & acceptance criteria (this file)
2. API questions list to unblock backend (output/specs/frontend_api_questions.md)
3. Initial reusable component scaffold to speed development (output/code/frontend/BookingForm.tsx)
4. Unit tests for the scaffold (output/tests/BookingForm.test.tsx)

Component inventory (MECE)
- Shell / Layout: AppShell, TopNav, BottomNav, Modals
- Discovery: SearchBar, Filters, ResultsList, MapView
- Product: ListingCard, ListingGallery, PriceBadge
- Booking flow: BookingForm, PassengerForm, PaymentSheet, Confirmation
- Account & Auth: SignupForm, LoginForm, Profile
- Shared primitives: Button, Input, Select, DatePicker, Spinner, ErrorBanner

Acceptance criteria (what I will deliver now)
- A clear list of components with responsibilities and data needs (above).
- API dependency list and explicit questions for Marcus to answer.
- One fully implemented, typed, accessible BookingForm component (local state) with unit tests.

Decisions & assumptions
- Start with local component state for forms; adopt Zustand later if cross-component state is required.
- Use Tailwind CSS for styling (matches stack). Component will be unstyled/minimally styled for now.
- Accessibility: form labels, aria-invalid, role="alert" for validation messages.

Blockers for frontend work
- Concrete API shapes for search/listings, booking creation, auth endpoints, and whether guest checkout is allowed.
- Design tokens & Figma screens from Maya for spacing, typography, and interactions.

Next steps for Marcus (frontend needs)
- Provide API response shapes for listing search, booking create, auth flows, and a flag to indicate guest checkout availability.
- Preferred error format (field-level vs single message) and validation error codes.

Reference files created in this step
- output/specs/frontend_readiness.md (this file)
- output/specs/frontend_api_questions.md
- output/code/frontend/BookingForm.tsx
- output/tests/BookingForm.test.tsx

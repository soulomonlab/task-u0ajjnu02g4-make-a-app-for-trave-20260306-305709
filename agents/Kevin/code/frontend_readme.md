Frontend Developer README — Kevin (Mobile-first, React + TypeScript + Tailwind)

Purpose
This README summarizes how to proceed with implementing the Travel App MVP frontend after receiving design assets from Maya and API confirmation from Marcus.

Tech decisions
- React 18 + TypeScript
- Vite for dev + build
- Tailwind CSS for styling
- Zustand for small client state (session, itinerary draft)
- React Query for server data (lists, pagination, mutations)
- Testing: React Testing Library + Vitest for unit tests

Folder structure (output/code/frontend)
- components/  -> shared UI components (Modal, Toast, Input, Button)
- hooks/       -> custom hooks (useAuth, useItineraryDraft, useDebouncedValue)
- pages/       -> page-level components (Home, SearchResults, Itinerary, Checkout, Signup, Login)
- lib/         -> api client (api.ts) + types (types.ts)
- styles/      -> tailwind config + design token mapping
- tests/       -> unit & integration tests

Stand-up checklist
1) Get Figma link and design tokens from Maya. If not received within 24h, start with Tailwind default tokens and flag missing tokens.
2) Confirm API shapes with Marcus for endpoints: /search, /items, /bookings, /itineraries, /auth.
3) Create branches and PRs per feature: feat/component-library, feat/search-mvp, feat/itinerary-mvp.

Developer scripts (to add in project)
- dev: vite
- build: vite build
- test: vitest
- lint: eslint

Contact points
- #ai-design — Maya (for tokens, Figma link)
- #ai-backend — Marcus (for API field confirmation and OpenAPI updates)
- #ai-qa — Dana (for acceptance tests once feature branch ready)


Kevin → Marcus: API shape clarifications (blocking frontend)

Context:
I’m preparing the frontend components for the Travel App MVP. Maya will deliver hi-fi screens and tokens, but to implement components correctly I need confirmation of several API response shapes and header behaviors. This will unblock accurate prop typing, UI fields, and pagination handling.

Questions (please answer or point to OpenAPI fields):
1) Search result item shape (GET /api/v1/search):
   - Exact fields returned per item (name, id, type, image_url, snippet or highlight_html, price_min, rating, location_name).
   - Does backend return highlighted HTML (highlight_html) or highlight ranges (start/end)? If HTML, what tags are allowed? (We prefer sanitized HTML or range offsets.)
2) Cursor pagination envelope:
   - Confirm response shape: { items: [], next_cursor?: string } or { data: [], meta: { next_cursor: "" } }
   - Is next_cursor null/absent when there are no more pages, or empty string?
3) Booking pricing response (GET /pricing?offer_id=):
   - Desired shape for frontend: { base_price: number, taxes: [{name, amount}], fees: [{name, amount}], discounts: [{name, amount}], currency: string }
   - Confirm field names and whether amounts are integers (cents) or floats.
4) Booking create response (POST /bookings):
   - Required fields we should expect: booking_id, status (pending|confirmed|failed), next_action (payment_url|null), expires_at?
   - On idempotent retries with same Idempotency-Key, do you return 200 with existing booking or 409? Please confirm behavior and status codes.
5) Itinerary draft autosave:
   - PATCH /itineraries/{id} expected request shape for partial updates? Are PATCH semantics JSON Merge Patch or JSON Patch?
6) Auth flows:
   - Login response: access token in JSON (access_token) and HttpOnly refresh cookie set by server? Confirm key names.
   - For protected endpoints, clearly require Authorization: Bearer <token>. Any additional headers needed (traceparent ok). Any custom claims we should parse in access token we should expect (e.g., roles)?
7) Idempotency header name and format:
   - Confirm header name: Idempotency-Key and expected GUID/UUID format or any unique string.
8) Currency formatting rules:
   - Should frontend display amounts using Intl.NumberFormat('en-US', { style: 'currency', currency: currencyCode })? Any exceptions for zero-decimals currencies?

Timeline: I can start implementing with best-effort mock shapes, but I prefer signed-off shapes within 48 hours to avoid rework. If there's an OpenAPI update that answers these, point me to the exact spec file / path.

Thanks — Kevin
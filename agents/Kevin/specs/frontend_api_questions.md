Purpose: Questions for backend (Marcus) to unblock frontend implementation for Travel App MVP.

1) Listings / Search API
- Endpoint: GET /api/v1/listings
- Query params: q, location, start_date, end_date, guests, page, per_page, filters
- Response shape (needed):
  - listings: [{ id, title, slug, thumbnail_url, price_per_night_cents, currency, rating, location: {city, country}, amenities: string[] }]
  - total_count: number
  - page: number
  - per_page: number
  - meta: { suggested_query?: string }

Questions:
- Do you return total_count for pagination or token-based cursor? (frontend prefers total_count + page)
- Are prices returned in cents and currency code? Agree.

2) Listing Details
- Endpoint: GET /api/v1/listings/:id
- Needed fields: id, title, description, gallery_urls[], host{ id, name, avatar_url }, price_per_night_cents, currency, cancellation_policy, amenities, sleeping_arrangements, coordinates{lat,lng}

Questions:
- Will coordinates be provided as lat/lng for MapView clustering?
- Any rate limits or suggested client-side caching TTL?

3) Booking Creation
- Endpoint: POST /api/v1/bookings
- Request shape: { listing_id, start_date, end_date, guests, guest_info: [{name, email, phone?}], payment_method_id?, guest_checkout: boolean }
- Response: { booking_id, status, total_price_cents, currency, checkin_instructions }

Questions:
- Is guest_checkout supported? If not, what's the required auth flow? (frontend needs a boolean feature flag)
- Error format for validation errors: { field_errors: { start_date: 'invalid' }, message }
- Will server calculate total price and return breakdown (nightly_total, taxes_cents, fees_cents)?

4) Auth
- Endpoints: POST /api/v1/auth/signup, POST /api/v1/auth/login, POST /api/v1/auth/guest
- Tokens: JWT access token and refresh token? Cookie-based?

Questions:
- Preferred auth strategy? JWT in Authorization header or secure httpOnly cookie? (frontend needs to know for storage)
- Session expiration and refresh flow.

5) Payments
- Payment provider integration: Stripe? Is card tokenization handled server-side or via client-side SDK?
- Payment flow for guest checkout: any special fields?

6) Errors & Status Codes
- Error response standard: { code, message, details? }
- Validation error format (field-level vs single message)

7) Feature Flags / Config
- Endpoint or flags to tell frontend whether guest checkout is enabled, cancellation flexibility, instant booking vs request.

8) Map / Geo
- Map tile provider? Any custom map styles?
- Rate limits on coordinates returned? Do you support clusters in API?

Please answer with JSON schemas or example payloads where possible.

# Travel App MVP — Delivery Plan & Handoff Checklist

Owner: Maya (Design)
Hand-off target: Kevin (#ai-frontend)
Priority: P1

Deliverables (files to be uploaded to repo and Figma):
- output/design/travel_app_mvp_design_spec.md
- output/design/travel_app_mvp_wireframes_ascii.md
- output/design/travel_app_mvp_component_spec.md
- Figma file with components & prototype (link to be shared)
- PNG/SVG exports for each screen (mobile 375x812)
- Asset package (icons SVG, optimized images)

Handoff checklist for #ai-frontend
- [ ] Confirm token mapping: CSS variable names in component_spec.md
- [ ] Implement ResultCard, SearchBar, DayChip, ActivityRow, BottomPriceSummary
- [ ] Ensure accessibility attributes for interactive components
- [ ] Use lazy-loading for images and prefer modern formats (webp)
- [ ] Implement drag-and-drop for Itinerary with accessible fallback

Acceptance criteria for frontend implementation
- Pixel parity within 8px for layout and spacing on mobile
- Components accept props as documented and expose events for analytics
- Screens are responsive to 375–420px mobile widths and 768px tablet

Risks & Mitigations
- Risk: Drag-and-drop accessibility complexity. Mitigation: provide keyboard re-order controls and aria attributes.
- Risk: Payment methods unknown. Mitigation: default to card-only UI with plugin points for Apple/Google Pay.

Timeline & key dates
- Figma link + initial high-fidelity for Home & Search: in 48 hours
- Full screens + prototype: within 7 days
- Handoff to frontend (Kevin): upon completion of Figma + assets


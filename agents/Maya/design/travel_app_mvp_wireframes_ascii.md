# Travel App MVP — Mobile Wireframes (ASCII)

This file contains mobile-first ASCII wireframes for rapid reference and development alignment. Use these to verify layout and spacing before Figma high-fidelity screens are published.

Canvas size: 375 x 812 (iPhone 11/12 baseline)

1) Home / Discovery

------------------------------------
| Top nav: [logo]       [search🔍] |
------------------------------------
| HERO Carousel (image 16:9)       |
|  "Discover Bali"  |  CTA: View  |
|----------------------------------|
| Trending Deals → (horizontal)    |
| [Card][Card][Card]               |
|----------------------------------|
| Categories: [Beaches][Cities][...]|
|----------------------------------|
| Recommended for you (list)       |
| [Small Card]                     |
| [Small Card]                     |
|----------------------------------|
| Bottom Nav: Home | Search | Trips |
------------------------------------

2) Search

------------------------------------
| Back | Where to? (input) [date]  |
|----------------------------------|
| Filters (collapsible): Price | Stops|
|----------------------------------|
| [ResultCard]
|  Img
|  Title
|  Location  •  Price  [Add] [Book]
|----------------------------------|
| Map toggle FAB (bottom-right)
|----------------------------------|
| Bottom Nav
------------------------------------

3) Itinerary Builder

------------------------------------
| Header: "My Bali Trip"    [Edit] |
| Day chips: [Day 1][Day 2][+ Add]  |
|----------------------------------|
| Timeline:                         |
|  ⠿ 08:00  -> Breakfast at Cafe    |
|  ⠿ 10:00  -> Beach time           |
|  ⠿ 14:00  -> Temple visit         |
|----------------------------------|
| FAB: Save / Proceed to Checkout   |
| Bottom Nav                         |
------------------------------------

4) Booking Checkout

------------------------------------
| Progress: Contact > Passengers > Payment > Review |
| Form: Contact info                                |
| Passenger list: (Name, DOB, Remove)               |
| Payment: Card input or saved                       |
| Promo code                                        |
|----------------------------------|
| Price Summary (sticky) | Confirm & Pay (CTA)      |
------------------------------------

Notes:
- All tap targets >= 44px
- Cards use 12px radius and 8px inner padding
- Visual hierarchy: image -> title -> location -> price


# Product Requirements Prompt — Jiangnan Trip Planner

Build a collaborative trip-planning web app for a small group travelling to China, 15–22 Nov 2026. Deliver it as a **single `index.html` file** (inline CSS and JS, no build step, no external dependencies except the Amap JS API loaded from `webapi.amap.com` via `<script>`). It must open directly in a browser and be hostable on GitHub Pages as-is.

## Pitch
A shared wishlist-to-itinerary planner: each traveller searches Amap for places, adds picks to a common wishlist, and the group assembles a day-by-day itinerary around fixed flights, trains and hotels.

## Users
Tze (organiser) plus two or three travel companions. Used on phone and laptop, before the trip (planning) and during it (reference). Non-technical users: setup must be one screen — enter your name and paste the Amap key.

## Trip facts to pre-seed
- Arrive: MH388 KUL → PVG, Sun 15 Nov 2026
- Hangzhou 15–18 Nov (3 nights) → Nanjing 18–20 Nov (2 nights) → Suzhou 20–21 Nov (1 night) → Shanghai 21–22 Nov (1 night, JW Marriott Pudong)
- Depart: MH389 PVG → KUL, Sun 22 Nov 2026
- Hotels under consideration: Conrad Hangzhou, Ritz-Carlton Nanjing, Suzhou hotel TBC. Seed these as editable hotel blocks marked "tentative".
- Inter-city legs (Shanghai→Hangzhou, Hangzhou→Nanjing, Nanjing→Suzhou, Suzhou→Shanghai) seeded as empty train blocks the user fills in.

## User journey
1. Open the URL → prompted for display name (stored locally) and Amap key + security JS code (stored locally, never in the repo). Show a one-line pointer: whitelist this site's domain in the Amap console.
2. Search tab: pick a city (Hangzhou / Nanjing / Suzhou / Shanghai), type a query, see results as a list plus pins on an Amap map. Tap "Add to wishlist" on any result.
3. Wishlist tab: everyone's picks in one list, each showing who added it, category, city, votes, notes. Filter by city and by person.
4. Itinerary tab: eight day columns/cards (15–22 Nov), each labelled with its city. Assign wishlist items to a day and reorder within the day. Fixed blocks (flight, train, hotel check-in/out) appear inline in time order.
5. Share: export the whole plan as one JSON file; send it to a companion; they import it and the app **merges** (union by item ID, keeps both sets of votes/notes) rather than overwrites. Repeat until finalised.

## Key features
- Amap place search using the Amap JS API 2.0 `PlaceSearch` plugin with city restriction; map with markers; clicking a marker highlights the list item. Handle a missing/invalid key with a clear message in the Settings tab, not a silent failure.
- Manual add: name, address, city, optional coordinates, note — for places found in emails, articles or recommendations that aren't on Amap.
- Wishlist items: id, name, address, city, lat/lng, category, addedBy, addedAt, notes (free text), votes (per person, toggle), status (wishlist / scheduled / dropped).
- Itinerary: per-day ordered list; move item between days; unassign back to wishlist; optional time and duration per item; transport and hotel blocks with editable number/time/from/to.
- Export / import JSON with merge; also "Copy summary as text" for pasting into WhatsApp.
- Persistence in `localStorage`; no backend.
- Mobile-first, responsive; four bottom tabs on mobile (Search, Wishlist, Itinerary, Settings), side nav on desktop. Keyboard focus visible; respect reduced motion.

## Constraints
- Do not commit any API key. Keys live only in the browser's localStorage.
- Amap script must load only after a key is present; app remains usable (wishlist, itinerary, import/export) without a key.
- All copy in plain English; place names shown as returned by Amap (Chinese) with the user's own note field for a nickname.
- Design: make one deliberate visual choice tied to the subject (Jiangnan water-town / canal palette), keep the rest quiet. No generic SaaS card grid.

## Deliverable
`index.html` at repo root plus a short `README.md` covering: how to get an Amap key, whitelisting the GitHub Pages domain, and the export → send → import loop.

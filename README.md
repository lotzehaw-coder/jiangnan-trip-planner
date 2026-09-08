# Jiangnan Trip Planner

A shared, interactive version of the *China Itinerary HZ · NJ · SZ 15–22 Nov* workbook — Hangzhou → Nanjing → Suzhou → Shanghai, 15–22 Nov 2026.

**Live:** https://lotzehaw-coder.github.io/jiangnan-trip-planner/

One file (`index.html`), no backend, no build, no API keys. Everything lives in your own browser; to plan together you swap export files (below).

## What's in it

- **Itinerary** — all eight days from the workbook, every stop with its time, duration, notes and address. Tap a stop to vote ♥, add your own note, change its start time, nudge it earlier/later, move it to another day, or take it off the plan (it goes to the wishlist, nothing is lost). Flights, trains and hotel check-ins sit inline as travel blocks — tap **Edit** to fill in a train number or booking ref.
- **Map ↗** on every stop, card and hotel — opens the place in **高德地图 (Amap)** on your phone, already searched, so you tap 路线 for directions. No account or key needed; it's a plain deep link. Falls back to the Amap web map if the app isn't installed.
- **Browse** — the workbook's other tabs: Dining & cafés, the ranked meal picks for every lunch and dinner, Shop · street food · explore, and Events & foliage. Filter by city, search by name or dish, then **Add to wishlist** or **Put on <day>** in one tap. "Add a place that isn't in the list" covers recommendations from elsewhere.
- **Wishlist** — the plan's optional and alternative picks plus anything anyone adds. Vote, then pick a day.
- **Copy as text for WhatsApp** — the whole plan, formatted, on the clipboard.

## Planning together — export → send → import

Import **merges**; it never overwrites.

1. **Share → Export plan** downloads `jiangnan-plan-<name>-<date>.json`.
2. Send it to a companion on WhatsApp.
3. They open the site, **Share → Import & merge**, pick the file.
4. Their copy now has both sets of votes, notes and additions. Each person's note stays under their own name; scheduling changes take whichever side edited most recently.
5. They export and send it back. Repeat until the plan is final.

## Sources and what's confirmed

- Flights are the confirmed Trip.com booking: **MH388** KUL T1 09:10 → PVG T2 14:30 on 15 Nov; **MH389** PVG T2 16:05 → KUL T1 21:50 on 22 Nov. (The workbook shows older times — the booking wins.)
- Hotels per the workbook: Conrad Hangzhou 15–18, Ritz-Carlton Nanjing 18–20, Ritz-Carlton Suzhou 20–22.
- Trains are **not booked** and are marked *tentative* with the workbook's suggested departures.

## Updating from the workbook

The app is generated from the spreadsheet; edit the workbook, re-run the generator, commit `index.html`. Stops nobody has touched follow the workbook; anything someone has voted on, noted or moved is left alone.

## Hosting

GitHub Pages serves `main` from the repo root. Push `index.html` and it's live within a minute or two.

# Jiangnan Trip Planner

A shared, interactive version of the *China Itinerary HZ · NJ · SZ 15–22 Nov* workbook — Hangzhou → Nanjing → Suzhou → Shanghai, 15–22 Nov 2026.

**Live:** https://lotzehaw-coder.github.io/jiangnan-trip-planner/

One file (`index.html`), no backend, no build step for the reader, no API keys. Everything lives in your own browser; to plan together you swap export files (below).

## What's in it

- **Itinerary** — all eight days from the workbook, colour-coded by type (the same code as the sheet: blue sights, orange food, cocoa cafés, ochre shops, magenta trendy, maple foliage, lilac optional, gold hotels, green travel). Each city has its own colour and landmark — West Lake pagoda, the Ming wall gate, Suzhou's stepped gables and moon gate, the Pudong skyline. Day headers stick while you scroll and collapse on tap; the `1 … 8` strip jumps between days; the chips filter to must-sees, food, optional or travel.
- **Tap a stop** to open it: ♥ vote, add your own note, change the start time, nudge it earlier/later, move it to another day, or take it off (it goes to the wishlist, nothing is lost). **Tap the dot** on the timeline to tick it done — during the trip the hero shows *up next* using China time.
- **Map** — opens 高德地图 directly (not the web page) into **public-transport directions to the stop**; every landmark, hotel and station carries GCJ-02 coordinates. On iPhone you get a choice of Amap or Apple Maps. Stops without a pin fall back to a name search.
- **Browse** — the workbook's other tabs: Dining & cafés, the ranked meal picks for every lunch and dinner, Shop · street food · explore, Events & foliage. Filter by city, search by name or dish, then *Add to wishlist* or *Put on <day>*.
- **Wishlist** — the plan's optional and alternative picks plus anything anyone adds.
- **Copy as text for WhatsApp** — the whole plan, formatted, on the clipboard.

## Planning together — export → send → import

Import **merges**; it never overwrites.

1. **Share → Export plan** downloads `jiangnan-plan-<name>-<date>.json`.
2. Send it to a companion on WhatsApp.
3. They open the site, **Share → Import & merge**, pick the file.
4. Their copy now has both sets of votes, notes, ticks and additions. Each person's note stays under their own name; scheduling changes take whichever side edited most recently.
5. They export and send it back. Repeat until the plan is final.

## The workbook is the source

`index.html` is generated from the shared iCloud workbook (`China_Itinerary_HZ_NJ_SZ_15-22Nov.xlsx`). To pick up edits made in the spreadsheet:

```bash
cd tools
python parse_seed.py        # pulls the latest workbook from the iCloud share link, writes seed.json
python build.py             # seed.json + template.html -> ../index.html
```

then commit and push `index.html`. Needs Python 3 and `openpyxl`. `python parse_seed.py --local` skips the download and uses `tools/itinerary.xlsx`. Stops nobody has touched follow the workbook; anything someone has voted on, noted, ticked or moved is left alone.

Coordinates come from a hand-kept table in `parse_seed.py` (WGS-84, converted to GCJ-02 for Chinese maps). A new place in the workbook without an entry there still gets a Map button — it searches by name instead of routing.

## Confirmed vs not

- Flights are the Trip.com booking: **MH388** KUL T1 09:10 → PVG T2 14:30 on 15 Nov; **MH389** PVG T2 16:05 → KUL T1 21:50 on 22 Nov. (The workbook shows older times — the booking wins.)
- Hotels per the workbook: Conrad Hangzhou 15–18, Ritz-Carlton Nanjing 18–20, Ritz-Carlton Suzhou 20–22.
- Trains are **not booked** and are marked *tentative* with the workbook's suggested departures.

## Hosting

GitHub Pages serves `main` from the repo root. Push `index.html` and it's live within a minute or two.

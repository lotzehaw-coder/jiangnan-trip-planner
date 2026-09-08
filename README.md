# Jiangnan Trip Planner

A shared wishlist-to-itinerary planner for a small group travelling Hangzhou → Nanjing → Suzhou → Shanghai, 15–22 Nov 2026.

**Live:** https://lotzehaw-coder.github.io/jiangnan-trip-planner/

One file (`index.html`), no backend, no build. Everything you add is kept in your own browser. To plan together, you swap export files — see below.

## First open

1. Enter your display name.
2. Paste your Amap key and security code — or skip and add them later in **Settings**. Without a key you can still add places by hand, vote, build the itinerary and share the plan; only search and the map are off.

## Getting an Amap key

1. Sign in at https://console.amap.com (a Chinese mobile number or email works for registration).
2. **应用管理 → 我的应用 → 创建新应用**, then **添加 Key**.
3. Service platform: **Web端 (JS API)**.
4. Copy both the **Key** and the **安全密钥 (security JS code)** the console shows.
5. In the key's settings, add the site to the **域名白名单** (domain whitelist):
   ```
   lotzehaw-coder.github.io
   ```
   Searches from a domain that isn't whitelisted are refused — the app will tell you in Settings, and **Test key** there runs a one-word search so you can confirm it works.

Keys are stored in your browser's local storage only. They are never written into the repo and never included in an export file.

## Planning together — the export → send → import loop

Import **merges**; it never overwrites.

1. **Settings → Export plan** downloads `jiangnan-plan-<name>-<date>.json`.
2. Send it to a companion on WhatsApp.
3. They open the site, **Settings → Import & merge**, pick the file.
4. Their copy now has both sets of places. Places you both added (same Amap result) are combined — votes from both, each person's note kept under their own name. Scheduling (which day, what time) takes whichever side changed it most recently.
5. They export and send it back. Repeat until the plan is final.

**Copy summary as text** on the Itinerary tab puts the whole plan on the clipboard, formatted for pasting straight into a WhatsApp group.

## What's pre-filled

- MH388 KUL → PVG on Sun 15 Nov, MH389 PVG → KUL on Sun 22 Nov
- Hotel check-in/out blocks: Conrad Hangzhou, Ritz-Carlton Nanjing, Suzhou (TBC) — all marked *tentative* — and JW Marriott Pudong
- Four empty train blocks for the inter-city legs

Tap **Edit** on any block in the Itinerary to fill in numbers, times and names.

## Hosting

GitHub Pages serves `main` from the repo root. Push `index.html` and it's live within a minute or two. Nothing else to configure.

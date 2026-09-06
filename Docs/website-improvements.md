# Project Car — Website Improvements (Living)

**Status:** Living document — update when items ship, get deferred, or new issues are found  
**Last audited:** 2026-09-06 (brochure hygiene P0-3…P0-7 in git **and already live** on Worker `projectcar-brochure`; re-uploaded 2026-09-06)  
**Owner:** Ben (decisions) · Garage (brochure HTML/CSS) · Zone (Cloudflare Worker upload) · Doc (Shop API host)  
**Canonical:** `Coombzy/Project-Car` → `Docs/website-improvements.md`  
**Local clone:** `~/src/Project-Car/Docs/website-improvements.md`  
**Desktop mirror:** `~/Desktop/Project Car/docs/website-improvements.md`  
**Site code:** `apps/website/` (git SSOT). **Live origin:** Cloudflare Worker `projectcar-brochure` Direct Upload of `apps/website/html` (not Doc `:8088` tunnel). Classic Pages git skipped for now. Apex is **deferred** (stripped from this tree).  
**Related:**
- `website-webapp-specification.md` — domain, tunnel, email, architecture (SSOT; do not dual-author a second plan under `apps/website/`)
- `api-stay-up.md` / `cors-origins.md` — public Shop API stay-up + waitlist CORS
- Skill `project-car-web-copy` — public copy rules (tighten, no fake prices/dates)
- Skill `project-car` — fleet / product context (public site ≠ Mission Control)

---

## How to maintain this doc

1. **Audit block** — when re-checking the live site, bump **Last audited** and add a short Changelog entry.
2. **Status values** (use exactly these in tables):
   - `open` — agreed worth doing, not started
   - `in_progress` — actively being worked
   - `done` — shipped and verified on https://projectcar.ca
   - `blocked` — waiting on Ben / dependency / secret / hardware
   - `wontfix` — explicit decision not to do (note why)
   - `deferred` — not now; revisit later
3. **When shipping** — mark `done`, add date, one-line verification (URL or command).
4. **Do not invent** prices, open dates, street addresses, or “live” features that are not live. Match public honesty on About / Membership.
5. **Copy changes** — follow `project-car-web-copy` page lanes (Home ≠ product dump; Chat must not overpromise).
6. **After edits** — commit + push `Coombzy/Project-Car`; rsync/copy to Desktop mirror without `--delete` unless intentionally pruning.

---

## Snapshot (2026-09-06)

| Check | Result |
|--------|--------|
| https://projectcar.ca / www | Worker `projectcar-brochure` Direct Upload of `apps/website/html` (PR #5 on `main`). HTML from this agent often hits CF challenge (403); SSL in front is Cloudflare. |
| robots.txt / sitemap / favicon / Home bar | Pre-upload snapshot from earlier 2026-09-06 is **stale**. Worker was re-uploaded later that day with P0-3…P0-7. Do not treat hygiene as pending. |
| Waitlist | **e2e PASS** — Membership/Contact `POST` to `https://api.projectcar.ca/waitlist` |
| Pages | Home, About, The Shop, Membership, Roadmap, Contact. Chat nav stripped (PR #5). |
| Discord invite | `https://discord.gg/projectcar` |
| Soft-404 | Live Worker 404s missing static files. Git has `404.html` + nginx `error_page 404`. Do not add SPA `/* /index.html 200`. |
| Mission Control | Separate; Owner + Member booking are live on Doc demo. Cockpit still needs **Ben GO** — do not start it from brochure work. |

**Overall:** Waitlist is live. Chat/Apex stay gone. Brochure hygiene P0-3…P0-7 is **already live** on the Worker. Owner + Member booking are live on Doc demo — not Mission Control, not Apex, not a redesign. `app.projectcar.ca` is still not claimed.

---

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Broken, misleading, or actively hurts trust/crawlers — fix first |
| **P1** | Conversion / visitor clarity before open doors |
| **P2** | SEO, share cards, headers, deploy hygiene |
| **P3** | Copy tighten per page-lane skill |
| **P4** | Growth / content once basics are solid |

---

## P0 — Fix now

Apex is **not** in this list. See Deferred — Apex.

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P0-3 | **Real `robots.txt`** | done | 2026-09-06 — `apps/website/html/robots.txt` is `User-agent: *` / `Allow: /` + `Sitemap:` (no extra Disallow). Local: `curl -sS http://127.0.0.1:8088/robots.txt` is `text/plain`, not Home HTML. Live after next Worker Direct Upload. |
| P0-4 | **Real `sitemap.xml`** | done | 2026-09-06 — `apps/website/html/sitemap.xml` lists canonical public HTML only: `/`, about, the-shop, membership, roadmap, contact. No Chat/Apex. Local: `curl -sSI http://127.0.0.1:8088/sitemap.xml`. |
| P0-5 | **Stop soft-404 SPA fallback for static site** | done | 2026-09-06 — `404.html` + nginx `error_page 404 /404.html`; `_redirects` stays Chat→Contact 301 only (no SPA fallback). Local nginx: unknown path → **404** + branded page. Worker already 404s missing files; Zone should set `not_found_handling = "404-page"` on next upload. |
| P0-6 | **Favicon set** | done | 2026-09-06 — `html/favicon.ico` + `assets/favicon.svg` / `favicon-32.png` / `apple-touch-icon.png`. Pages no longer use `mcking.jpg` as the only icon. Local: `curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/favicon.ico` → 200. |
| P0-7 | **Home “Website progress 10%”** | done | 2026-09-06 — progress-block removed (no owner-approved metric; did not invent a %). Home keeps honest “Project Underway” + waitlist CTA. Local: Home HTML has no “Website progress” / `10%`. |

### Deferred — Apex (not active P0)

IDs kept so old links resolve. Do not treat these as current P0.

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P0-1 | **Apex auth readable in container** | deferred | Was live `/api/apex/health` 503 (auth mount `600` / user mismatch). `apps/website/` has no Apex sidecar (Pages cutover). Revisit only if Ben/Lead puts chat back in scope. |
| P0-2 | **Apex offline UX if chat stays down** | deferred | Follows P0-1. Contact/Chat must not imply a working assistant while Apex is out of scope. |

---

## P1 — Conversion / UX

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P1-1 | **Home primary CTAs** | open | Strong actions: waitlist / membership interest, Discord join, Contact. Secondary: About / The Shop. Less feature laundry on home. Waitlist form itself is **done** (P1-5). |
| P1-2 | **Chat page honesty** | done | 2026-09-06 — Chat page/nav stripped in PR #5. No public chat copy left to overpromise. Do not revive. |
| P1-3 | **Contact: only live channels** | open | Keep email + Discord. Collapse Phone / IG / TikTok / YouTube / Skool “Coming soon” into one line until URLs exist. |
| P1-4 | **Nav weight** | deferred | Optional: Home · About · Shop · Membership · Contact in primary nav; Roadmap/Chat in footer until chat is real. |
| P1-5 | **Interest capture (waitlist)** | done | 2026-09-06 — Membership/Contact `POST` JSON to `https://api.projectcar.ca/waitlist` (`apps/website/html/waitlist.js`). Name, email, optional phone/notes. No pricing / book-now. Ops: `cors-origins.md`, `api-stay-up.md`. |

---

## P2 — SEO / share / tech hygiene

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P2-1 | **Absolute Open Graph URLs** | open | `og:image` / `og:url` as `https://projectcar.ca/...`. Add `og:type`, `twitter:card`. Prefer ~1200×630 share image. |
| P2-2 | **Canonical links per page** | open | `<link rel="canonical">` on each public HTML page. |
| P2-3 | **Asset / CSS cache version single source** | open | about.html at `?v=29`, others mostly `?v=28`. One bump strategy; no-cache all HTML; long-cache fingerprinted static assets. |
| P2-4 | **Security headers at origin** | open | e.g. `X-Content-Type-Options`, `Referrer-Policy`, frame denial / CSP baseline for static site (+ CF as today). |
| P2-5 | **Image weight / modern formats** | deferred | shop ~444K, mcking ~312K OK; WebP/AVIF + srcset when polishing mobile. |
| P2-6 | **JSON-LD LocalBusiness/Organization** | deferred | Only when real public location/hours exist—no invented NAP. |
| P2-7 | **Put site tree under git** | done | 2026-09-06 — `apps/website/` is the git SSOT (imported from Doc live tree). |

---

## P3 — Copy (page lanes)

Follow skill **project-car-web-copy**. Tighten; don’t rewrite the story. No fake prices/dates.

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P3-1 | **Home: pitch + CTA, not full feature dump** | open | Move long capability lists to Shop / Membership. Keep 2–3 sentence pitch + status + CTAs. |
| P3-2 | **About value cards shorter** | open | Target ~one short sentence per card; keep structure (problem → who → pieces → experience → heading → not promising → CTA). |
| P3-3 | **About “Parts” / “Member app” destinations** | open | Listed without pages. Add honest stubs (“not live”) or stop presenting as navigable destinations. |
| P3-4 | **Shop vs Home bullet overlap** | open | Shop should emphasize facility/standards; Membership owns access packaging; Home stays high-level. |
| P3-5 | **Tense consistency for “24/7”** | open | Membership correctly hedges “when operational”; Home/Shop sometimes state 24/7 as present fact. Align voice. |

---

## P4 — Growth / later

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P4-1 | **Real progress photography** | deferred | One honest build-out photo beats another generated hero for trust. |
| P4-2 | **Discord as equal CTA on Home/Membership** | open | Invite already works; surface it next to email. |
| P4-3 | **YouTube / Skool links** | deferred | Post-MVP documenting the business build—only when channel/community URLs exist. |
| P4-4 | **Analytics** | deferred | Privacy-friendly (e.g. CF Web Analytics) to see which CTA works. |
| P4-5 | **Synthetic monitors** | deferred | Homepage 200 + Apex health + Discord invite check. |

---

## Suggested implementation order

1. P1-1 / P1-3 (home CTA weight, Contact channel honesty)  
2. P2-1 … P2-4 (OG, canonical, cache, headers)  
3. P3 copy pass  
4. P4 as interest grows  

Brochure hygiene is **already live** on Worker `projectcar-brochure` (re-uploaded 2026-09-06). Do not invent another Zone upload for that ship. Owner + Member booking are live on Doc demo; `app.projectcar.ca` is still not claimed. Mission Control cockpit still needs **Ben GO**.

Waitlist (P1-5), Chat strip (P1-2), git home (P2-7), and P0-3…P0-7 are **done** (git + live Worker). Apex (P0-1 / P0-2) is **deferred** — do not start the queue there.  

---

## Quick verification commands (Doc)

```bash
# Local from apps/website (python http.server 8088 --directory html)
curl -sSI http://127.0.0.1:8088/robots.txt | head -8
curl -sS http://127.0.0.1:8088/robots.txt
curl -sSI http://127.0.0.1:8088/sitemap.xml | head -8
curl -sS -o /dev/null -w '%{http_code} %{content_type}\n' http://127.0.0.1:8088/favicon.ico
# nginx (optional): unknown path must be HTTP 404 + 404.html, not Home
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/this-should-404

# Live (after next Worker Direct Upload). HTML may 403 under CF challenge from datacenters.
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca
curl -sSI https://projectcar.ca/robots.txt | head -5
curl -sS https://projectcar.ca/robots.txt | head -20
curl -sSI https://projectcar.ca/sitemap.xml | head -5
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/this-should-404

# Apex — deferred (not an active P0). Skip unless chat is back in scope.
# curl -sS http://127.0.0.1:8088/api/apex/health
# curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/api/apex/health

# Waitlist API (Lead owns uvicorn; Zone owns tunnel — see api-stay-up.md / cors-origins.md)
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health

# Discord
curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' -L https://discord.gg/projectcar
```

---

## Explicit non-goals (for now)

- Full member app / bay booking on the marketing site  
- Live pricing tables or fake open dates  
- Reintroducing n8n or bolting Mission Control onto projectcar.ca  
- Pixar/Disney McQueen IP in branding assets  
- Treating Chat as shipped product until a real join path exists  

---

## Changelog

| Date | Change |
|------|--------|
| 2026-09-06 | Reality sync ~11:20 America/Edmonton: P0-3…P0-7 **already live** on Worker (re-uploaded). No pending hygiene upload. Owner + Member booking live on Doc demo; `app.projectcar.ca` not claimed; MC cockpit still needs Ben GO. |
| 2026-09-06 | P0-3…P0-7 **done** in `apps/website/` (robots, sitemap, 404.html, favicon set, Home progress bar removed). Live origin noted as Worker Direct Upload, not Doc `:8088`. P1-2 Chat strip **done** (PR #5). Next product path: Owner booking; MC held. |
| 2026-09-06 | Status sync: P1-5 waitlist **done**; P2-7 site-under-git **done**; Apex P0-1 / P0-2 **deferred** (not active P0). |
| 2026-08-12 | Initial living doc from full live + local audit (Doc). P0–P4 backlog, maintain rules, verify commands. Linked from `website-webapp-specification.md`. |

---

## Decision log

| Date | Decision | By |
|------|----------|-----|
| 2026-09-06 | Brochure live host is Worker Direct Upload (`projectcar-brochure`), not Doc `:8088`. Classic Pages git skipped. Hygiene P0s are in git **and already live** (Worker re-uploaded 2026-09-06). | Ben (task) · Garage (site) · Zone (CF) |
| 2026-09-06 | Waitlist on brochure is **done**. Apex is **deferred**, not active P0. `Docs/` is SSOT; `apps/website/WEBSITE-*` files are pointers only. | Status sync (living ops) |
| 2026-08-12 | Keep improvements as a **living git doc** in Project-Car `Docs/`, separate from architecture spec. | Ben (request) · Doc (author) |

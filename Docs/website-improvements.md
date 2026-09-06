# Project Car — Website Improvements (Living)

**Status:** Living document — update when items ship, get deferred, or new issues are found  
**Last audited:** 2026-09-06 (status sync: waitlist shipped, Apex deferred — not a full live re-audit)  
**Owner:** Ben (decisions) · Doc (implement / infra on M1 Max host) · Porsche (coord)  
**Canonical:** `Coombzy/Project-Car` → `Docs/website-improvements.md`  
**Local clone:** `~/src/Project-Car/Docs/website-improvements.md`  
**Desktop mirror:** `~/Desktop/Project Car/docs/website-improvements.md`  
**Site code:** `apps/website/` (git SSOT). Doc runtime copy may still live under `~/hermes-tools/project-car-website`. Apex is **deferred** (stripped from this tree).  
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

## Snapshot (2026-08-12)

| Check | Result |
|--------|--------|
| https://projectcar.ca HTTPS | 200, SSL OK (~0.5s from Doc/YVR) |
| Local http://127.0.0.1:8088 | 200 |
| Docker `project-car-website` | Up, healthy, `:8088→80` |
| Docker `project-car-apex` | **Deferred** — not an active P0. Pages-ready `apps/website/` has no Apex sidecar. |
| Waitlist | **Done** — Membership/Contact `POST` to `https://api.projectcar.ca/waitlist` |
| Pages live | Home, About, The Shop, Membership, Roadmap, Chat, Contact |
| Discord invite | `https://discord.gg/projectcar` → 200 |
| Soft-404 | Missing paths (incl. robots/sitemap/favicon) return **200 + Home HTML** |
| Mission Control | Separate (`:8080`); not this site |

**Overall:** Brochure waitlist is shipped. Highest leverage left is remaining P0 hygiene (robots/404/favicon/home bar) and conversion—not Apex, not a redesign.

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
| P0-3 | **Real `robots.txt`** | open | Today returns Home HTML (200). Add static file; nginx must serve it as `text/plain`. |
| P0-4 | **Real `sitemap.xml`** | open | List canonical public HTML URLs; `application/xml`. Keep in sync when pages added/removed. |
| P0-5 | **Stop soft-404 SPA fallback for static site** | open | nginx `try_files … /index.html` makes unknown paths look live. Prefer real **404** page with status 404 (optional branded 404.html). Keep pretty paths only if intentional. |
| P0-6 | **Favicon set** | open | `/favicon.ico` soft-404s; pages use full JPEG portrait as icon. Add proper ICO/PNG/SVG. |
| P0-7 | **Home “Website progress 10%”** | open | Undercuts a 7-page live site. Drop bar, reframe as **shop build-out**, or set an honest metric with owner approval—do not leave stale 10%. |

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
| P1-2 | **Chat page honesty** | open | Copy reads like live human+AI member chat. Label **planned / not live**, fold into Roadmap, or ship a real join path. No fake “you get” present tense. |
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

1. P0-3 … P0-6 (robots, sitemap, 404, favicon) + nginx tweak  
2. P0-7 + P1-1 (home status + CTAs)  
3. P1-2, P1-3 (Chat/Contact honesty)  
4. P2-1 … P2-4 (OG, canonical, cache, headers)  
5. P3 copy pass  
6. P4 as interest grows  

Waitlist (P1-5) and git home (P2-7) are **done**. Apex (P0-1 / P0-2) is **deferred** — do not start the queue there.  

---

## Quick verification commands (Doc)

```bash
# Site + local
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/
docker ps --filter name=project-car --format '{{.Names}} {{.Status}}'

# Must NOT be HTML forever
curl -sSI https://projectcar.ca/robots.txt | head -5
curl -sS https://projectcar.ca/robots.txt | head -20
curl -sSI https://projectcar.ca/sitemap.xml | head -5

# Soft-404 check (want 404, not 200 home)
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
| 2026-09-06 | Status sync: P1-5 waitlist **done**; P2-7 site-under-git **done**; Apex P0-1 / P0-2 **deferred** (not active P0). |
| 2026-08-12 | Initial living doc from full live + local audit (Doc). P0–P4 backlog, maintain rules, verify commands. Linked from `website-webapp-specification.md`. |

---

## Decision log

| Date | Decision | By |
|------|----------|-----|
| 2026-09-06 | Waitlist on brochure is **done**. Apex is **deferred**, not active P0. `Docs/` is SSOT; `apps/website/WEBSITE-*` files are pointers only. | Status sync (living ops) |
| 2026-08-12 | Keep improvements as a **living git doc** in Project-Car `Docs/`, separate from architecture spec. | Ben (request) · Doc (author) |

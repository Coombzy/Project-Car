# Project Car — Website Improvements (Living)

**Status:** Living document — update when items ship, get deferred, or new issues are found  
**Last audited:** 2026-09-07 (P2-3 live-verified on Worker `projectcar-brochure` from Garage PR #57 / `be60a01` — Zone Direct Upload ~16:01 America/Regina; smoke PASS: `styles.css?v=34` + `banner-logo.png?v=30` on public HTML (Home/About/Contact at minimum; apex+www)). P2-1 / P2-2 already LIVE. P2-4 stays **open** (Zone checklist `brochure-security-headers.md` — plan only, not live).  
**Owner:** Ben (decisions) · Garage (brochure HTML/CSS) · Zone (Cloudflare Worker upload) · Doc (Shop API host)  
**Canonical:** `Coombzy/Project-Car` → `Docs/website-improvements.md`  
**Local clone:** `~/src/Project-Car/Docs/website-improvements.md`  
**Desktop mirror:** `~/Desktop/Project Car/docs/website-improvements.md`  
**Site code:** `apps/website/` (git SSOT). **Live origin:** Cloudflare Worker `projectcar-brochure` Direct Upload of `apps/website/html` (not Doc `:8088` tunnel). Classic Pages git skipped for now. Apex is **deferred** (stripped from this tree).  
**Related:**
- `website-webapp-specification.md` — domain, tunnel, email, architecture (SSOT; do not dual-author a second plan under `apps/website/`)
- `brochure-worker-deploy.md` — standing Zone Direct Upload of `apps/website/html` onto Worker `projectcar-brochure`
- `brochure-security-headers.md` — P2-4 Zone checklist (plan only; do not apply from a docs PR)
- `brochure-pages-cutover.md` — Classic Pages git plan (blocked on CF ↔ GitHub auth; do not start)
- `api-stay-up.md` / `cors-origins.md` — public Shop API stay-up + waitlist CORS
- `member-host-cutover.md` — Member UI on projectcar.ca (plan only; **Ben GO**). P1-6 waits on that cutover.
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

## Snapshot (2026-09-07)

| Check | Result |
|--------|--------|
| https://projectcar.ca / www | Worker `projectcar-brochure` Direct Upload of `apps/website/html` (P2-3 PR #57 / `be60a01` **LIVE**; P2-2 PR #56 / `ed41d23`; P2-1 PR #55 / `453e44d`; P1-1 / P1-3 PR #52 / `5361212`). P2-4 **open** (checklist only). HTML from this agent often hits CF challenge (403); SSL in front is Cloudflare. |
| robots.txt / sitemap / favicon / Home bar | Pre-upload snapshot from earlier 2026-09-06 is **stale**. Worker was re-uploaded later that day with P0-3…P0-7. Do not treat hygiene as pending. |
| Waitlist | **e2e PASS** — Membership/Contact `POST` to `https://api.projectcar.ca/waitlist` |
| Pages | Home, About, The Shop, Membership, Roadmap, Contact. Chat nav stripped (PR #5). |
| Discord invite | `https://discord.gg/projectcar` |
| Soft-404 | Live Worker 404s missing static files. Git has `404.html` + nginx `error_page 404`. Do not add SPA `/* /index.html 200`. |
| Mission Control | Separate; ops + Member booking are live on Doc demo, **`https://ops.projectcar.ca`**, and the temporary alias `https://app.projectcar.ca`. Cockpit still needs **Ben GO** — do not start it from brochure work. |

**Overall:** Waitlist is live. P1-1 Home `cta-hero` waitlist CTA weight and P1-3 Contact `contact-soon` collapse are **LIVE** on Worker `projectcar-brochure` (PR #52 / `5361212`; 2026-09-07 smoke PASS). P2-1 is **LIVE** on that Worker (PR #55 / `453e44d`; absolute `og:url` / `og:image` + `twitter:card`; Zone smoke PASS). P2-2 canonicals are **LIVE** on that Worker (PR #56 / `ed41d23`; Zone Direct Upload ~2026-09-07 15:48 America/Regina; Zone smoke PASS: `rel=canonical` matches `og:url` apex on Home + Membership; www serves apex canonicals). P2-3 cache `?v=` SSOT is **LIVE** on that Worker (PR **#57** / `be60a01`; Zone Direct Upload ~2026-09-07 16:01 America/Regina; smoke PASS: `styles.css?v=34` + `banner-logo.png?v=30` on public HTML — Home/About/Contact at minimum; apex+www). P2-4 stays **open** (checklist `brochure-security-headers.md` — not applied). Brochure Chat/Apex stay gone (Apex sidecar deferred; public Chat page stays stripped). Shop OS **Chat v1** (human / polling) is **LIVE** on the ops/app demo — not the brochure. Brochure hygiene P0-3…P0-7 is **already live** on the Worker. Ops + Member booking, Chat #27, and Dashboard #28 are live on Doc demo, **`https://ops.projectcar.ca`**, and the temporary alias `https://app.projectcar.ca`. Some clients still have flaky local DNS for `ops.` — use `app.`. Not Mission Control, not Apex. The shop is not open. P1-6 stays deferred.

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
| P1-1 | **Home primary CTAs** | done | 2026-09-07 live verify — Garage PR #52 → main `5361212`. Home `cta-hero` waitlist CTA weight (Join the waitlist is the dominant above-the-fold action). Zone Direct Upload Worker `projectcar-brochure` **LIVE** from that tip; smoke PASS (Home CTA; apex/www 200). |
| P1-2 | **Chat page honesty** | done | 2026-09-06 — Chat page/nav stripped in PR #5. No public chat copy left to overpromise. Do not revive. |
| P1-3 | **Contact: only live channels** | done | 2026-09-07 live verify — Garage PR #52 → main `5361212`. Phone / IG / TikTok / YouTube / Skool collapsed to one `contact-soon` line. Email + Discord + waitlist stay. Zone Direct Upload Worker `projectcar-brochure` **LIVE** from that tip; smoke PASS (Contact; apex/www 200). |
| P1-4 | **Nav weight** | deferred | Optional: Home · About · Shop · Membership · Contact in primary nav; Roadmap/Chat in footer until chat is real. |
| P1-5 | **Interest capture (waitlist)** | done | 2026-09-06 — Membership/Contact `POST` JSON to `https://api.projectcar.ca/waitlist` (`apps/website/html/waitlist.js`). Name, email, optional phone/notes. No pricing / book-now. Ops: `cors-origins.md`, `api-stay-up.md`. Public **OPTIONS** / **POST /waitlist** **530 / 1033** while Doc is asleep is expected lid-close — not a CORS regression. `waitlist.js` **mailto fallback** is the user path; e2e only when **GET /health** is **200**. |
| P1-6 | **Membership secondary CTA: “Already a member? Sign in”** | deferred | After Member cutover — **Ben GO** (not now; not done). Link **only** apex `https://projectcar.ca/member/login`. Never www, never ops/app. Waitlist stays the interest path. No book-now / pricing / shop-open claims. Do **not** implement brochure HTML from a docs PR. P1-1 / P1-3 already shipped (#52); this item still waits on cutover. Plan: `member-host-cutover.md`, STATUS Next #1. |

---

## P2 — SEO / share / tech hygiene

| ID | Item | Status | Notes / acceptance |
|----|------|--------|-------------------|
| P2-1 | **Absolute Open Graph URLs** | done | 2026-09-07 live verify — Garage PR #55 → main `453e44d` already on Worker. Absolute `og:url` / `og:image` + `twitter:card` (`og:type` / `twitter:image` too) at `https://projectcar.ca/...` on all brochure HTML. Zone Direct Upload Worker `projectcar-brochure` **LIVE**; Zone smoke PASS. Dedicated ~1200×630 share crop still later. |
| P2-2 | **Canonical links per page** | done | 2026-09-07 live verify — Garage PR #56 → main `ed41d23` already on Worker (Zone Direct Upload ~15:48 America/Regina). `<link rel="canonical" href="https://projectcar.ca/...">` on every public HTML page (Home `/`, about, the-shop, membership, roadmap, contact, 404). Apex host only (not www). Paths match P2-1 `og:url`. Zone smoke PASS: `rel=canonical` matches `og:url` apex on Home + Membership; www serves apex canonicals. Do not invent P2-4 as done. |
| P2-3 | **Asset / CSS cache version single source** | done | 2026-09-07 live verify — Garage PR #57 → main `be60a01` already on Worker (Zone Direct Upload ~16:01 America/Regina). All public HTML uses `styles.css?v=34` and `banner-logo.png?v=30`. Shared `shop-config.js?v=1` + `waitlist.js?v=2` already matched. Page-only images left as-is. Smoke PASS: Home/About/Contact at minimum; apex+www. HTML no-cache / CF header config is **not** live (P2-4 checklist: `brochure-security-headers.md`). Do not invent P2-4 as done. |
| P2-4 | **Security headers at origin** | open | Plan only — Zone checklist: `brochure-security-headers.md`. Target Worker `projectcar-brochure`: `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY` **or** CSP `frame-ancestors 'none'`, optional static-site `Permissions-Policy`, plus HTML `no-cache, must-revalidate` vs long-cache `?v=` assets (P2-3). Live Worker **200**s have **none** of those headers today. Do **not** apply from a docs PR — Zone after Lead GO. Status stays **open**. |
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
| P4-5 | **Synthetic monitors** | done | **Partial.** Lookout **`projectcar-api-health-watch`** owns API health flips (`https://api.projectcar.ca/health` — 200 when Doc origin is up; lid-close 502/530). Brochure homepage 200 optional. **Apex dropped** (sidecar deferred; do not monitor `/api/apex/health`). Discord invite check stays optional/deferred. Do not invent extra shipped monitors. Matches STATUS Lookout lock. |

---

## Suggested implementation order

1. P2-4 (security headers at origin) — Zone after Lead GO; checklist `brochure-security-headers.md`; not this PR  
2. P3 copy pass  
3. P4 as interest grows  
4. P1-6 only **after Member cutover GO** — still deferred; no brochure HTML from a docs PR.

Brochure hygiene is **already live** on Worker `projectcar-brochure` (re-uploaded 2026-09-06). P1-1 / P1-3 are **LIVE** on that Worker (PR #52 / `5361212`; 2026-09-07 smoke PASS). P2-1 is **LIVE** on that Worker (PR #55 / `453e44d`; Zone smoke PASS). P2-2 is **LIVE** on that Worker (PR #56 / `ed41d23`; Zone Direct Upload ~2026-09-07 15:48 America/Regina; Zone smoke PASS). P2-3 is **LIVE** on that Worker (PR **#57** / `be60a01`; Zone Direct Upload ~2026-09-07 16:01 America/Regina; smoke PASS: `styles.css?v=34` + `banner-logo.png?v=30` on public HTML — Home/About/Contact at minimum; apex+www). P2-4 stays **open** (checklist `brochure-security-headers.md` — not applied). Ops + Member booking are live on Doc demo **and** the temporary `app.` alias. Intended management host is **`ops.`**. Mission Control cockpit still needs **Ben GO**. The shop is not open.

Waitlist (P1-5), Chat strip (P1-2), Home CTA weight (P1-1), Contact channel honesty (P1-3), absolute OG (P2-1), canonicals (P2-2), cache `?v=` SSOT (P2-3), git home (P2-7), and P0-3…P0-7 are **done** (git + live Worker). P1-6 stays **deferred**. P2-4 stays **open** (Zone checklist only — not applied). Apex (P0-1 / P0-2) is **deferred** — do not start the queue there.  

---

## Quick verification commands (Doc)

```bash
# Local from apps/website (python http.server 8088 --directory html)
# P2-2: one apex canonical per public HTML page (paths match og:url)
rg -n 'rel="canonical"' html/*.html
# P2-3: one styles.css?v= and one banner-logo.png?v= across public HTML
rg -n 'styles\.css\?v=' html/*.html
rg -n 'banner-logo\.png\?v=' html/*.html
# leftover mismatched cache versions must be empty
rg -n 'styles\.css\?v=(32|33)' html/*.html || true
rg -n 'banner-logo\.png\?v=(28|29)' html/*.html || true
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

- Shipping Member booking onto projectcar.ca **in a brochure / this-docs PR** — that host migration is **Next**, not live  
- Live pricing tables or fake open dates  
- Reintroducing n8n or bolting Mission Control onto projectcar.ca  
- Pixar/Disney McQueen IP in branding assets  
- Treating **brochure** Chat as shipped product / reviving Apex (Shop OS Chat v1 is LIVE on ops/app; that is not this site)  
- Cutting the `app.` alias from a docs PR — `ops.` is already LIVE; alias stays until Ben cuts that DNS  

---

## Changelog

| Date | Change |
|------|--------|
| 2026-09-07 | P2-3 **done** with Worker live verify. Garage PR #57 → main `be60a01` already on Worker (Zone Direct Upload ~16:01 America/Regina): `styles.css?v=34` + `banner-logo.png?v=30` on public HTML (Home/About/Contact at minimum; apex+www). P2-1 / P2-2 already LIVE. P2-4 stays **open** (checklist on main — not applied). P1-6 stays deferred. Tip fold: `348375e` / **#58**. |
| 2026-09-07 | P2-4 Zone checklist landed (`brochure-security-headers.md`). Target Worker `projectcar-brochure` headers + HTML vs `?v=` cache split. Status stays **open** / plan — not applied, not live. Zone after Lead GO. Do not invent P2-4 done. Tip fold: `be60a01` / **#57**. |
| 2026-09-07 | P2-2 **done** with Worker live verify. Garage PR #56 → main `ed41d23` already on Worker (Zone Direct Upload ~15:48 America/Regina): `rel=canonical` matches `og:url` apex on Home + Membership; www serves apex canonicals. P2-3 **done** with git/`rg` verify PR **#57** / `be60a01` (`styles.css?v=34` + `banner-logo.png?v=30` on all public HTML). P2-4 stays **open**. P1-6 stays deferred. |
| 2026-09-07 | P2-1 **done** with Worker live verify. Garage PR #55 → main `453e44d` already on Worker: absolute `og:url` / `og:image` + `twitter:card`. Zone smoke PASS. P2-2 tags landed in PR #56 / `ed41d23` (later Worker-live; see row above). |
| 2026-09-07 | P1-1 / P1-3 **done** (live verify). Garage PR #52 → main `5361212`. Home `cta-hero` waitlist CTA weight; Contact Phone/IG/TikTok/YouTube/Skool collapsed to one `contact-soon` line. Zone Direct Upload Worker `projectcar-brochure` **LIVE** from that tip; smoke PASS (Home CTA + Contact; apex/www 200). P1-6 stays deferred. P2 not invented as done. |
| 2026-09-07 | P1-6 stub: Membership secondary “Already a member? Sign in” → apex `https://projectcar.ca/member/login` only. **Deferred** until Member cutover GO. Never www / ops / app. Waitlist stays the interest path. No brochure HTML in this docs PR. |
| 2026-09-07 | P1-5 note: lid-close public **530 / 1033** on OPTIONS / POST /waitlist is expected — not a CORS regression. `waitlist.js` mailto fallback while origin is down; e2e only when GET /health is 200. See `cors-origins.md`. |
| 2026-09-07 | P4-5 synthetic monitors **done / partial**: Lookout `projectcar-api-health-watch` live on `api.projectcar.ca/health`. Apex dropped (deferred). Brochure homepage 200 + Discord invite optional/deferred. Spec roadmap row 2 **Done** on Worker `projectcar-brochure`. |
| 2026-09-06 | Reality sync ~16:16 America/Edmonton (`main` `afb37f9`): **`ops.projectcar.ca` LIVE** → Doc `:3000`; `app.` = temporary alias. Calendar #18 / fill #20 / placeholders #21 / inventory #26 / Chat #27 / Dashboard #28 are Live on Doc. Brochure Chat/Apex stay stripped. MC cockpit still needs Ben GO. No Stripe. The shop is not open. |
| 2026-09-06 | Reality sync ~14:10 America/Edmonton (`main` `91c547e`): **`ops.projectcar.ca` LIVE** → Doc `:3000`; `app.` = temporary alias. Calendar #18 / fill #20 / placeholders #21 / schedule harden #24 are Live. Chat planned, not live (superseded ~16:16). MC cockpit still needs Ben GO. No Stripe. The shop is not open. |
| 2026-09-06 | Reality sync ~12:28 America/Edmonton: host split locked — customer = projectcar.ca; management = **`ops.projectcar.ca`**; `app.` = temporary alias (live). Member UI on projectcar.ca is Next. No DNS cut. MC cockpit still needs Ben GO. No Stripe. The shop is not open. |
| 2026-09-06 | Reality sync ~11:52 America/Edmonton: `https://app.projectcar.ca` **LIVE** (Ben GO ~11:41) pointing at Doc demo. Owner + Member booking reachable on the public app host. MC cockpit still needs Ben GO. No Stripe. The shop is not open. |
| 2026-09-06 | Reality sync ~11:20 America/Edmonton: P0-3…P0-7 **already live** on Worker (re-uploaded). No pending hygiene upload. Owner + Member booking live on Doc demo; `app.projectcar.ca` not claimed; MC cockpit still needs Ben GO. |
| 2026-09-06 | P0-3…P0-7 **done** in `apps/website/` (robots, sitemap, 404.html, favicon set, Home progress bar removed). Live origin noted as Worker Direct Upload, not Doc `:8088`. P1-2 Chat strip **done** (PR #5). Next product path: Owner booking; MC held. |
| 2026-09-06 | Status sync: P1-5 waitlist **done**; P2-7 site-under-git **done**; Apex P0-1 / P0-2 **deferred** (not active P0). |
| 2026-08-12 | Initial living doc from full live + local audit (Doc). P0–P4 backlog, maintain rules, verify commands. Linked from `website-webapp-specification.md`. |

---

## Decision log

| Date | Decision | By |
|------|----------|-----|
| 2026-09-06 | Host split: customer = `projectcar.ca` / www; management = **`ops.projectcar.ca` LIVE** (staff on shift + Owner, not Owner-only); `app.` = temporary alias until Ben cuts that DNS. | Ben (via Master Chief) |
| 2026-09-06 | Brochure live host is Worker Direct Upload (`projectcar-brochure`), not Doc `:8088`. Classic Pages git skipped. Hygiene P0s are in git **and already live** (Worker re-uploaded 2026-09-06). | Ben (task) · Garage (site) · Zone (CF) |
| 2026-09-06 | Waitlist on brochure is **done**. Apex is **deferred**, not active P0. `Docs/` is SSOT; `apps/website/WEBSITE-*` files are pointers only. | Status sync (living ops) |
| 2026-08-12 | Keep improvements as a **living git doc** in Project-Car `Docs/`, separate from architecture spec. | Ben (request) · Doc (author) |

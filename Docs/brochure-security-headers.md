# Brochure security + cache headers — Worker `projectcar-brochure`

**Status:** **LIVE** — Zone Transform Rules applied on Worker `projectcar-brochure` (apex + www). 2026-09-07 Worker **200** smoke PASS. Do **not** re-apply from a docs PR.  
**Updated:** 2026-09-07  
**Related:** `website-improvements.md` **P2-4** (**done**), `brochure-worker-deploy.md` (standing HTML upload), `website-webapp-specification.md` §3, `STATUS.md` Live brochure, `apps/website/README.md`

This file is the **Zone** record for website-improvements **P2-4** (security headers at origin) plus the HTML vs `?v=` **cache split** that P2-3 already named. Zone applied the three Transform Rules below. A docs merge is **not** a re-apply and is **not** a Worker upload.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, Apex revival, or API / Doc recovery. This file does **not** ping Ben. DNS / tunnels were **untouched**.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Do not re-apply from a docs PR** | Merging this file is **not** an apply. Do not edit Cloudflare, Transform Rules, Worker settings, or `apps/website/html/_headers` from docs work. No Garage / Zone / Hatch fan-out from this PR. |
| **P2-4 is LIVE** | 2026-09-07 Worker **200** smoke PASS (below). Challenge **403** headers are WAF, not origin — do not treat them as a fail or a re-apply trigger. |
| **P2-3 is LIVE** | Zone Direct Upload ~2026-09-07 16:01 America/Regina from `main` **`be60a01`** (Website **#57**). `styles.css?v=34` + `banner-logo.png?v=30` on public HTML (Home/About/Contact at minimum; apex+www). P2-4 cache-split headers are **also** live (this file). |
| **DNS / tunnels** | Untouched. Do not retarget `ops.` / `app.` / `api.` from this record. |

---

## Applied Transform Rules (2026-09-07)

Zone applied these on Worker **`projectcar-brochure`** for **apex** `projectcar.ca` and **www**:

| Rule | What |
|------|------|
| **`brochure-security-headers`** | `X-Content-Type-Options: nosniff`. `Referrer-Policy: strict-origin-when-cross-origin`. `X-Frame-Options: DENY`. `Permissions-Policy` static defaults (no cam / mic / geo / payment / USB — see Target headers). |
| **`brochure-html-no-cache`** | `/` + `*.html`: `Cache-Control: no-cache, must-revalidate` |
| **`brochure-asset-immutable`** | `?v=` `.css` / `.js` / `.png`: `Cache-Control: public, max-age=31536000, immutable` |

---

## Reality today (2026-09-07 live)

| Surface | Reality |
|---------|---------|
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html`. Apex + www. |
| **Security headers on Worker 200** | **Present:** `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY`, `Permissions-Policy` static defaults. |
| **Cache today** | HTML (`/` + `*.html`): `Cache-Control: no-cache, must-revalidate`. Fingerprinted `?v=` `.css` / `.js` / `.png`: `public, max-age=31536000, immutable`. Unversioned `robots.txt`: `max-age=0` (not long-cached). |
| **HTML from some networks** | Cloudflare challenge (**403**, `cf-mitigated: challenge`). Those interstitial headers (challenge CSP, `X-Frame-Options: SAMEORIGIN`, …) are **WAF**, not Worker origin. Do **not** treat them as a P2-4 fail. See `brochure-worker-deploy.md` Smoke. |
| **P2-3 `?v=` SSOT** | **LIVE** on Worker (PR **#57** / `be60a01`; Zone Direct Upload ~16:01 America/Regina). All public HTML uses `styles.css?v=34` and `banner-logo.png?v=30`. Shared `shop-config.js?v=1` + `waitlist.js?v=2` already matched. Smoke PASS: Home/About/Contact at minimum; apex+www. |
| **`html/_headers`** | MIME hints for robots / sitemap only. Worker Direct Upload does **not** honor Pages `_headers` for this slice. Live headers came from Transform Rules, not that file. |
| **Classic Pages git** | **Skipped** (`brochure-pages-cutover.md`). Do not start. |
| **Member edge / Apex / CF↔GitHub** | Out of scope. Not shipped. |

---

## Target headers (Worker `projectcar-brochure` — applied)

On **apex** `projectcar.ca` and **www**, Worker responses (HTML + static) include:

| Header | Value | Required |
|--------|--------|----------|
| `X-Content-Type-Options` | `nosniff` | **Yes** — applied |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | **Yes** — applied |
| Frame denial | `X-Frame-Options: DENY` | **Yes** — applied (CSP `frame-ancestors` was the alternate; not used) |
| `Permissions-Policy` | Sensible static-site defaults | Applied |

Optional `Permissions-Policy` for this static brochure (no cam / mic / geo / payment / USB):

```
accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
```

Do **not** add a full script/style CSP in this slice. Waitlist is `shop-config.js` + `waitlist.js` `POST` to `https://api.projectcar.ca/waitlist`. Frame denial only. A later CSP would need an allowlist for `self` + that API — not this record.

Do **not** copy challenge-page headers (`X-Frame-Options: SAMEORIGIN`, challenge CSP) onto the Worker.

---

## Cache split (ties to P2-3 — applied)

P2-3 is the git `?v=` bump. This row is the **origin cache** half. Without the split, visitors can keep stale HTML that still points at old `?v=`, or pay a revalidate on every fingerprinted asset.

| Class | `Cache-Control` | Why |
|-------|-----------------|-----|
| **HTML** — `/`, `/*.html`, branded `404.html` | `no-cache, must-revalidate` | Revalidate so the next Zone upload of a Garage `?v=` bump is picked up. **LIVE** (`brochure-html-no-cache`). |
| **Long-cache `?v=` / fingerprinted assets** — `styles.css?v=`, `banner-logo.png?v=`, `shop-config.js?v=`, `waitlist.js?v=` | `public, max-age=31536000, immutable` | Query string changes on bump (`website-improvements.md` P2-3). **LIVE** (`brochure-asset-immutable`). |
| **Unversioned static** — `robots.txt`, `sitemap.xml`, `favicon.ico` without `?v=` | Keep short / revalidate (`max-age=0`) | Do **not** long-cache these. Smoke: `robots.txt` is `max-age=0`. |

Exact match syntax (Transform Rule vs Worker) is **Zone’s**. Do not long-cache HTML. Do not re-apply from a docs PR.

---

## Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Response headers + cache split on Worker **`projectcar-brochure`** (Transform Rules already applied). Confirm apex / www still attach to this Worker. | HTML content, waitlist e2e, uvicorn, DNS cuts, Member path-split, Pages git, CF↔GitHub |
| **Lead** | GO was for the apply that is now live. A docs fold is **not** a re-apply GO. | Worker uploads, Cloudflare header rules |
| **Garage** | Brochure HTML / `?v=` bumps (P2-3) | Direct Upload, CF header config |

Alerts can come from anyone who sees a broken public page. **Recovery of a bad header apply is Zone** (rollback below).

---

## Applied (Zone — 2026-09-07; do not re-run from this PR)

Historical — already done. Do **not** invent a required host or re-open the dashboard from a docs PR.

1. Lead GO was confirmed for this header apply. A docs merge, a standing HTML-upload GO, or a Garage HTML PR is **not** a re-apply GO.
2. Existing Worker: Cloudflare dashboard → Workers & Pages → Workers → **`projectcar-brochure`**. No new Worker or Pages project.
3. Transform Rules on apex + www: **`brochure-security-headers`**, **`brochure-html-no-cache`**, **`brochure-asset-immutable`** (tables above).
4. Hosts confirmed. Apex and www still attach to this Worker. DNS / `ops.` / `app.` / `api.` / Classic Pages git / `member-zone-edge.md` were **not** touched.
5. Smoke (below) passed from Worker **200**s, not challenge **403**.

Do **not** upload shop-web. Do **not** treat `html/_headers` as the live path. Do **not** start Pages git or CF↔GitHub auth from this file.

---

## Smoke (2026-09-07 PASS — Worker **200**s, not challenge 403)

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed header apply — check from a normal browser if `curl` is challenged (`website-improvements.md`). Judge P2-4 only on **Worker 200** bodies.

| Check | Result (2026-09-07) |
|-------|---------------------|
| `https://projectcar.ca/` | **200**. Required security headers. HTML `Cache-Control: no-cache, must-revalidate`. |
| `https://www.projectcar.ca/` | Same (brochure stays dual-host). |
| `styles.css?v=34` | **200**. Same security headers. `Cache-Control: public, max-age=31536000, immutable`. |
| `robots.txt` | **200** `text/plain`. Security headers. `max-age=0` — **not** long-cached. |
| Challenge **403** | Ignore interstitial headers. Not a P2-4 pass or fail. |
| Waitlist | Unchanged. Headers must not block Membership / Contact `POST` to `https://api.projectcar.ca/waitlist`. Health first: `api-stay-up.md`. Do **not** invent API recovery from this record. |

```bash
curl -sSI https://projectcar.ca/
curl -sSI https://www.projectcar.ca/
curl -sSI https://projectcar.ca/robots.txt
curl -sSI "https://projectcar.ca/styles.css?v=34"
```

On Home **200**, grep the four required names (`x-content-type-options`, `referrer-policy`, `x-frame-options`, plus HTML `cache-control`). Do **not** re-apply from a docs PR.

---

## Rollback

A bad header apply is a **Worker / Transform Rule** problem. Do **not** cut DNS. Do **not** touch ops/app. Do **not** restart uvicorn.

1. **Preferred:** Cloudflare dashboard → disable or revert the header / cache rules on Worker **`projectcar-brochure`** (`brochure-security-headers`, `brochure-html-no-cache`, `brochure-asset-immutable`).
2. **If the same change bundled a Direct Upload:** roll back the Worker version (`brochure-worker-deploy.md` Rollback).
3. Re-smoke Home (Worker **200**) — target headers gone or restored to the previous known-good rule set; pages still 200.
4. If pages look right but waitlist fails: API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to cut `projectcar.ca` off the Worker.

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Re-applying these headers | **This PR does not.** Already live. Do not re-run Transform Rules from docs. |
| Member host / path-split | `member-host-cutover.md` / `member-zone-edge.md` — **Ben GO**. Do not start. Not shipped. |
| Classic Pages git / CF↔GitHub | `brochure-pages-cutover.md`. Skipped. Do not start. |
| Apex sidecar | Deferred. Do not revive. |
| DNS / `app.` alias | Untouched. Do not cut or retarget. |
| Garage HTML / `?v=` bump | P2-3 **LIVE** on Worker (**#57** / `be60a01`; Zone Direct Upload ~16:01 America/Regina). P2-4 cache-split headers are a separate apply — also **LIVE**. |
| Shop API / shop-web | Lead (`:8000`) / `com.projectcar.shop-web`. Not this Worker. Do not invent recovery. |

**Ownership (unchanged):** Zone owns Worker headers + upload. Garage owns HTML. Lead owns Doc `:8000`.

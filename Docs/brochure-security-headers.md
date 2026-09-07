# Brochure security + cache headers — Worker `projectcar-brochure`

**Status:** Checklist / plan only — **not applied**. Do **not** execute from a docs PR.  
**Updated:** 2026-09-07  
**Related:** `website-improvements.md` **P2-4** (status stays **open**), `brochure-worker-deploy.md` (standing HTML upload), `website-webapp-specification.md` §3, `STATUS.md` Live brochure, `apps/website/README.md`

This file is the **Zone** checklist for website-improvements **P2-4** (security headers at origin) plus the HTML vs `?v=` **cache split** that P2-3 already named. Zone implements **after Lead GO**. A docs merge is **not** GO and is **not** a Worker upload.

Live Worker **200** responses today (robots / CSS / favicon from this probe) carry **none** of the target security headers. `Cache-Control` is `public, max-age=0, must-revalidate` on those 200s — no HTML vs asset split. Do **not** invent P2-4 **done**. Do **not** invent P2-3 Worker-live.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival. This file does **not** ping Ben.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Do not execute from a docs PR** | Merging this file is **not** an apply. Do not edit Cloudflare, Transform Rules, Worker settings, or `apps/website/html/_headers` from docs work. No Garage / Zone / Hatch fan-out from this PR. |
| **Lead GO before Zone applies** | Zone implements the table below **after Lead GO**. Standing brochure HTML upload GO (`brochure-worker-deploy.md`) is **not** this GO. |
| **P2-4 stays open** | Until a Worker **200** smoke (below) passes. Challenge **403** headers are WAF, not origin. |
| **P2-3 stays git-only** | Until Zone Direct Uploads `apps/website/html` from `main` **`be60a01`** (Website **#57**). Do not call the `?v=` bump live. |

---

## Reality today (do not claim this is done)

| Surface | Reality |
|---------|---------|
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html`. Apex + www. |
| **Security headers on Worker 200** | **None** of `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Content-Security-Policy` `frame-ancestors`, or `Permissions-Policy`. |
| **Cache today** | Worker 200s use `Cache-Control: public, max-age=0, must-revalidate` (robots, CSS, favicon). No long-cache for `?v=` assets. |
| **HTML from some networks** | Cloudflare challenge (**403**, `cf-mitigated: challenge`). Those interstitial headers (challenge CSP, `X-Frame-Options: SAMEORIGIN`, …) are **WAF**, not Worker origin. Do **not** treat them as P2-4 live. See `brochure-worker-deploy.md` Smoke. |
| **P2-3 `?v=` SSOT** | On git (PR **#57** / `be60a01`): all public HTML uses `styles.css?v=34` and `banner-logo.png?v=30`. Shared `shop-config.js?v=1` + `waitlist.js?v=2` already matched. **Not** Worker-live until Zone upload. |
| **`html/_headers`** | MIME hints for robots / sitemap only. Worker Direct Upload does **not** honor Pages `_headers` for this slice. Do not invent applying P2-4 by editing that file in a docs PR. |
| **Classic Pages git** | **Skipped** (`brochure-pages-cutover.md`). Do not start. |
| **Member edge / Apex / CF↔GitHub** | Out of scope. |

---

## Target headers (Worker `projectcar-brochure`)

Apply on **apex** `projectcar.ca` and **www** so Worker responses (HTML + static) include:

| Header | Value | Required |
|--------|--------|----------|
| `X-Content-Type-Options` | `nosniff` | **Yes** |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | **Yes** |
| Frame denial | `X-Frame-Options: DENY` **or** CSP `frame-ancestors 'none'` | **Yes** — pick one (both OK) |
| `Permissions-Policy` | Sensible static-site defaults (optional) | Optional |

Optional `Permissions-Policy` for this static brochure (no cam / mic / geo / payment / USB):

```
accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
```

Do **not** add a full script/style CSP in this slice. Waitlist is `shop-config.js` + `waitlist.js` `POST` to `https://api.projectcar.ca/waitlist`. Frame denial only. A later CSP would need an allowlist for `self` + that API — not this checklist.

Do **not** copy challenge-page headers (`X-Frame-Options: SAMEORIGIN`, challenge CSP) onto the Worker.

---

## Cache split (ties to P2-3)

P2-3 is the git `?v=` bump. This row is the **origin cache** half. Without the split, visitors can keep stale HTML that still points at old `?v=`, or pay a revalidate on every fingerprinted asset.

| Class | `Cache-Control` | Why |
|-------|-----------------|-----|
| **HTML** — `/`, `/*.html`, branded `404.html` | `no-cache, must-revalidate` | Revalidate so the next Zone upload of a Garage `?v=` bump is picked up. |
| **Long-cache `?v=` / fingerprinted assets** — `styles.css?v=`, `banner-logo.png?v=`, `shop-config.js?v=`, `waitlist.js?v=` | `public, max-age=31536000, immutable` | Query string changes on bump (`website-improvements.md` P2-3). |
| **Unversioned static** — `robots.txt`, `sitemap.xml`, `favicon.ico` without `?v=` | Keep short / revalidate (today’s `max-age=0, must-revalidate` is fine) | Do **not** long-cache these. |

Exact match syntax (Transform Rule vs Worker) is **Zone’s** after GO. Do not long-cache HTML.

---

## Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Response headers + cache split on Worker **`projectcar-brochure`** (Transform Rules / Worker settings — Zone’s click-path). Confirm apex / www still attach to this Worker. | HTML content, waitlist e2e, uvicorn, DNS cuts, Member path-split, Pages git, CF↔GitHub |
| **Lead** | **GO** before Zone applies this checklist | Worker uploads, Cloudflare header rules |
| **Garage** | Brochure HTML / `?v=` bumps (P2-3) | Direct Upload, CF header config |

Alerts can come from anyone who sees a broken public page. **Recovery of a bad header apply is Zone** (rollback below).

---

## Steps (Zone — after Lead GO; not this PR)

Use whatever machine already has Cloudflare access for Worker **`projectcar-brochure`**. Do **not** invent a required host.

1. **Confirm Lead GO** for this header apply. A docs merge, a standing HTML-upload GO, or a Garage HTML PR is **not** this GO.
2. **Open the existing Worker.** Cloudflare dashboard → Workers & Pages → Workers → **`projectcar-brochure`**. Do **not** create a new Worker or a Pages project.
3. **Set the target headers** (table above) on Worker responses for `projectcar.ca` and `www.projectcar.ca`. Typical: Response Header Transform (or equivalent Worker/custom-domain rules). Exact product is Zone’s.
4. **Set the cache split** (HTML `no-cache, must-revalidate` vs long-cache `?v=` assets).
5. **Confirm hosts.** Apex and www still attach to this Worker. Do **not** edit DNS, retarget `ops.` / `app.` / `api.`, connect Classic Pages git, or execute `member-zone-edge.md`.
6. **Smoke** the list below from a path that is a Worker **200**, not a challenge **403**.

Do **not** upload shop-web. Do **not** treat `html/_headers` as applied on this Worker. Do **not** start Pages git or CF↔GitHub auth from this file.

---

## Smoke (after apply — not this PR)

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed header apply — check from a normal browser if `curl` is challenged (`website-improvements.md`). Judge P2-4 only on **Worker 200** bodies (Home HTML, or `robots.txt` / CSS when HTML is challenged).

| Check | Expect |
|-------|--------|
| Home (Worker **200**) | `X-Content-Type-Options: nosniff`. `Referrer-Policy: strict-origin-when-cross-origin`. `X-Frame-Options: DENY` **or** CSP contains `frame-ancestors 'none'`. `Cache-Control` includes `no-cache` and `must-revalidate`. Optional `Permissions-Policy` if Zone set it. |
| www Home | Same headers (brochure stays dual-host). |
| `?v=` asset | Long-cache (`max-age` large / `immutable`). Same security headers as Zone applied site-wide. |
| Unversioned `robots.txt` | Still **200** `text/plain`. **Not** long-cached. Security headers if Zone applied them site-wide. |
| Challenge **403** | Ignore interstitial headers. Not a P2-4 pass or fail. |
| Waitlist | Unchanged. Headers must not block Membership / Contact `POST` to `https://api.projectcar.ca/waitlist`. Health first: `api-stay-up.md`. |

```bash
curl -sSI https://projectcar.ca/
curl -sSI https://www.projectcar.ca/
curl -sSI https://projectcar.ca/robots.txt
curl -sSI "https://projectcar.ca/styles.css?v=34"
```

On Home **200**, grep the four required names (`x-content-type-options`, `referrer-policy`, plus `x-frame-options` **or** `frame-ancestors`, plus HTML `cache-control`). Do **not** run this apply from a docs PR.

---

## Rollback

A bad header apply is a **Worker / Transform Rule** problem. Do **not** cut DNS. Do **not** touch ops/app. Do **not** restart uvicorn.

1. **Preferred:** Cloudflare dashboard → disable or revert the header / cache rules on Worker **`projectcar-brochure`**.
2. **If the same change bundled a Direct Upload:** roll back the Worker version (`brochure-worker-deploy.md` Rollback).
3. Re-smoke Home (Worker **200**) — target headers gone or restored to the previous known-good rule set; pages still 200.
4. If pages look right but waitlist fails: API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to cut `projectcar.ca` off the Worker.

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Applying these headers | **This PR does not.** Zone after Lead GO. |
| Inventing P2-4 **done** | Status stays **open** until Worker **200** smoke. |
| Member host / path-split | `member-host-cutover.md` / `member-zone-edge.md` — **Ben GO**. Do not start. |
| Classic Pages git / CF↔GitHub | `brochure-pages-cutover.md`. Skipped. Do not start. |
| Apex sidecar | Deferred. Do not revive. |
| DNS / `app.` alias | Do not cut or retarget. |
| Garage HTML / `?v=` bump | Already on git (P2-3 / **#57**). Zone upload is a separate standing deploy. |
| Shop API / shop-web | Lead (`:8000`) / `com.projectcar.shop-web`. Not this Worker. |

**Ownership (unchanged):** Zone owns Worker headers + upload. Garage owns HTML. Lead owns Doc `:8000` and the GO for this apply.

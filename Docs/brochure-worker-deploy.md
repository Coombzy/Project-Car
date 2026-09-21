# Brochure Worker deploy — `projectcar-brochure`

**Status:** Standing runbook  
**Updated:** 2026-09-21  
**Related:** `STATUS.md` Live brochure + Option A smoke-gate lock, `website-webapp-specification.md` §3, `website-improvements.md`, `brochure-security-headers.md` (P2-4 **LIVE** — do not re-apply from this runbook), `api-stay-up.md`, `shop-web-stay-up.md`, `cors-origins.md`, `brochure-pages-cutover.md`, `member-zone-edge.md`, `apps/website/README.md`

Re-deploy the public brochure after Garage merges HTML on `main`. This is the **locked live method**. It is not a one-off for a single hygiene ship.

This file describes the process **when Ben / Zone already have standing GO** for brochure uploads after Garage merges. It does **not** assign live work, change DNS, or start a Pages-git / Apex / Member-host project.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival.

---

## Locked live reality

| Piece | Reality |
|-------|---------|
| **Git SSOT** | `apps/website/html` on `main` (`Coombzy/Project-Car`) |
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** |
| **Deploy method** | **Direct Upload** of `apps/website/html` from the `main` tip you are shipping |
| **Public hosts** | https://projectcar.ca and https://www.projectcar.ca |
| **Not the origin** | Doc `:8088`, `~/hermes-tools/project-car-website`, optional local nginx preview |
| **Classic Pages git** | **Skipped** pending CF ↔ GitHub auth. Plan only: `brochure-pages-cutover.md`. Do not invent a live cutover from this runbook. |
| **Apex sidecar** | **Deferred.** Do not revive. |

Waitlist on Membership / Contact is a **browser POST** to the Shop API (`https://api.projectcar.ca/waitlist`). The Worker only serves static HTML/JS. API health and CORS live in `api-stay-up.md` and `cors-origins.md` — a green upload does not prove waitlist.

---

## Trigger

After Garage merges brochure HTML changes on `main` under `apps/website/html`, Zone re-deploys Worker **`projectcar-brochure`** via Direct Upload of that tree.

- Garage ships the HTML PR. Zone uploads. Lead does not own brochure edge.
- Do not upload from a dirty tree, a feature branch, or `~/hermes-tools/project-car-website`.
- Do not treat a docs-only merge (this file, STATUS, specs) as a deploy trigger.

---

## Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Direct Upload of `apps/website/html` onto Worker **`projectcar-brochure`**. Confirm Worker name + apex / www still attach to this Worker. | HTML content, waitlist e2e, uvicorn, DNS cuts, ops/app tunnels |
| **Garage** | Brochure HTML PRs under `apps/website/html`. Waitlist e2e after public `GET /health` is **200**. | Direct Upload, Cloudflare Worker versions, tunnel, uvicorn |
| **Lead** | Doc `:8000` / LaunchAgent `com.projectcar.shop-api` (`api-stay-up.md`) | Brochure edge. Do not hand Worker uploads to Lead. |

Alerts can come from anyone who sees a bad public page. **Recovery of a bad upload is Zone** (rollback below). **Recovery of a down API is Lead** (process) / **Zone** (tunnel only).

---

## Steps (Zone)

Use whatever machine already has Cloudflare access for this Worker. Checkout `main` there; do not invent a required host.

1. **Confirm the merge.** Garage’s brochure HTML is on `origin/main` under `apps/website/html`. Note the tip SHA you will ship.
2. **Get that tree.** On the upload machine:
   ```bash
   git fetch origin main
   git checkout <main-tip-sha>
   # or: git checkout main && git pull origin main
   ls apps/website/html
   ```
   Expect at least: `index.html`, `about.html`, `the-shop.html`, `membership.html`, `roadmap.html`, `contact.html`, `waitlist.js`, `shop-config.js`, `styles.css`, `robots.txt`, `sitemap.xml`, `404.html`, `favicon.ico`, `_redirects`, `_headers`, `assets/`. Chat page stays **absent** (`_redirects` is Chat → Contact 301 only).
3. **Open the existing Worker.** Cloudflare dashboard → Workers & Pages → Workers → **`projectcar-brochure`**. Do **not** create a new Worker or a Pages project.
4. **Direct Upload** the **`apps/website/html` directory** (that folder is the site root). Confirm the Worker name is still **`projectcar-brochure`** before you commit the deploy.
5. **Confirm hosts.** Apex `projectcar.ca` and `www.projectcar.ca` still attach to this Worker. Do **not** edit DNS, retarget `ops.` / `app.` / `api.`, or connect Classic Pages git.
6. **Optional Zone setting** (already noted in `apps/website/README.md`): static `not_found_handling = "404-page"` so branded `404.html` is used. Do not add an SPA `/* → /index.html` fallback.
7. **Smoke** the list below. If this upload is the Option A HTML finish (open **#82** leftover: Home `index.html` + thin `_redirects`), also run the **Option A Worker-live smoke gate** — **FAIL** until **PASS**. Then Garage runs waitlist e2e once public `GET /health` is **200**.

Do not upload shop-web (`apps/project-car/web`). Do not point the Worker at Doc `:8088`.

---

## Smoke after deploy

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed upload — check from a normal browser if `curl` is challenged (`website-improvements.md`).

| Check | Expect |
|-------|--------|
| Home | **200** Worker HTML. Waitlist / honest CTA present. **No** “Website progress” / `10%` bar (STATUS hygiene). Status line is “Project Underway” only — do not invent a %. |
| Chat | **No** Chat nav or Chat page (stripped, PR #5). `_redirects` maps `/chat.html` and `/chat` → Contact 301 if the Worker honors it. Contact stays email + Discord. |
| Pages | Home, About, The Shop, Membership, Roadmap, Contact all **200** from Worker HTML on **apex and www**. |
| Waitlist API first | `GET https://api.projectcar.ca/health` → **200** `{"status":"ok","service":"project-car-api"}`. If **502** or **530 / error 1033**, Doc lid-close / tunnel — `api-stay-up.md`. Do not treat that as a bad HTML upload. |
| Waitlist e2e | **Garage** after health is 200: Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist` → **PASS**. CORS allowlist: `cors-origins.md`. |

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/
curl -sS -o /dev/null -w '%{http_code}\n' https://www.projectcar.ca/
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/about.html
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/the-shop.html
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/membership.html
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/roadmap.html
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/contact.html
# Chat must not be a live page:
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/chat.html
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
```

Home HTML must not contain `Website progress` or a `10%` progress bar. Chat must stay gone (404 / redirect to Contact is fine; a Chat page is not).

A green general smoke (200 pages + no Chat) is **not** Option A HTML finish. Reality tip / Option A finish **cannot** claim live HTML is done until the gate below is **PASS**.

---

## Option A Worker-live smoke gate

**FAIL / fail unless all three are true** on **live** Worker HTML **after** Zone Direct Upload of `apps/website/html`. Do **not** stamp Reality tip or “Option A HTML finish” from git merge, Zone Redirect Rules, or this docs file.

| # | Check | PASS only if (live HTML) | FAIL if |
|---|--------|--------------------------|---------|
| 1 | Home / nav Home links | `href="index.html"` (relative) on Home nav and other public pages’ Home links | Bare `href="/"` |
| 2 | Home `rel=canonical` + `og:url` | Both exactly `https://projectcar.ca/index.html` | `https://projectcar.ca/` or www |
| 3 | Worker `_redirects` | Thin **chat-only**: `/chat` + `/chat.html` → Contact **301**. No `/` or `/shop` 302s | Worker 302 on `/` or `/shop` (Zone **301** pretty-URL pack owns `/` `/shop` `/membership` `/about` → `*.html`) |

`main` git may still list leftover `/shop` 302s in `apps/website/html/_redirects` until **#82** lands. Those leftovers are **not** the live pretty-URL SSOT. After the Option A upload, live `_redirects` must be thin chat-only.

CF challenge **403** is WAF, not this gate (same as the general smoke). Soft-530 / **1033** on `api.` / `ops.` / `app.` is Doc origin down — **not** a brochure HTML fail.

```bash
# Option A smoke — live HTML after Direct Upload. FAIL unless all three pass.
# 1) Home/nav: href="index.html" (not href="/")
curl -sS https://projectcar.ca/index.html | rg -n 'href="/"|href="index.html"'
# 2) canonical + og:url must both be https://projectcar.ca/index.html
curl -sS https://projectcar.ca/index.html | rg -n 'rel="canonical"|property="og:url"'
# 3) Worker _redirects stay thin — /shop must not be a Worker 302
#    Zone 301 pretty-URL pack owns / and /shop. A Worker 302 to /the-shop is FAIL.
curl -sSI https://projectcar.ca/shop
```

### Locks (do not weaken)

| Lock | Meaning |
|------|---------|
| **Zone 301 pretty-URL pack alone ≠ Option A HTML finish** | Apex+www Redirect **301**s can make `/` and `/shop` work while live Home still has bare `href="/"` + canonical/og `https://projectcar.ca/`. Pretty URLs live ≠ Worker HTML done. |
| **merge #82 ≠ Worker-live ≠ Reality tip-fold** | Open Website **#82** is the HTML leftover (nav / canonical / og / thin `_redirects`). Merge to `main` is not live. Live is Zone Direct Upload **then** this smoke **PASS**. Do **not** fold Reality tip or claim Option A finish until **PASS**. |
| **Soft-530 OPEN `home_expected`** | When Doc origin is down, public `api.` / `ops.` / `app.` (and waitlist) **530 / 1033** is quiet-ops — **not** an incident stamp. Do **not** treat Soft-530 as a failed Option A smoke or a reason to flip the Worker. Restore: `doc-lid-restore.md`. |

This docs lock ≠ Soft-530 restore ≠ Doc unfreeze ≠ vault retarget ≠ **#82** Worker-live execute. Do **not** tip-fold onto held **#70**. Do **not** amend held **#70**, **#75–#79**, **#81–#85**, **#86**.

---

## Rollback

A bad Direct Upload is a **Worker version** problem. Do **not** cut DNS. Do **not** touch ops/app. Do **not** restart uvicorn.

1. **Preferred:** Cloudflare dashboard → Worker **`projectcar-brochure`** → Deployments / Versions → roll back to the previous successful version.
2. **Or:** checkout the last known-good `main` tip and **re-upload** that `apps/website/html` tree (same steps as deploy).
3. Re-smoke Home + the six pages + no Chat.
4. If pages look right but waitlist fails: that is API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to cut `projectcar.ca` off the Worker.

---

## Security + cache headers (P2-4 — LIVE)

Worker **`projectcar-brochure` 200s** send the P2-4 security headers (2026-09-07 smoke PASS). Cache is split: HTML `no-cache, must-revalidate` vs `?v=` `.css`/`.js`/`.png` `public, max-age=31536000, immutable`. Unversioned `robots.txt` stays `max-age=0`. Record: **`brochure-security-headers.md`**. Zone Transform Rules: `brochure-security-headers`, `brochure-html-no-cache`, `brochure-asset-immutable` (apex+www). Do **not** re-apply headers, Transform Rules, or `_headers` from this runbook or a docs PR. P2-3 `?v=` is **LIVE** on Worker (`be60a01` / **#57**; Zone Direct Upload ~2026-09-07 16:01 America/Regina).

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Member host cutover | `member-host-cutover.md` — **Ben GO**. Zone path-split: `member-zone-edge.md`. Do not start from a brochure upload. |
| Mission Control cockpit | Needs **Ben GO**. Not this Worker. |
| Stripe / shop-open claims | Locked off. Interest waitlist only. |
| P2-4 security / cache headers | **LIVE** (2026-09-07). Record: `brochure-security-headers.md`. Do not re-apply from this upload. |
| Classic Pages git | Skipped. Plan: `brochure-pages-cutover.md`. Do not invent a git-connected Pages cutover here. |
| Apex sidecar | Deferred. Do not revive. |
| DNS / `app.` alias | Do not cut or retarget. |
| Shop API / shop-web process | Lead (`:8000`) / `com.projectcar.shop-web` (`next start` on `:3000`). See `api-stay-up.md` / `shop-web-stay-up.md`. |
| Option A HTML finish / **#82** execute | Smoke gate above. This runbook does **not** merge **#82**, upload the leftover tree, or fold Reality tip. |
| Soft-530 restore / Doc unfreeze / vault retarget | `doc-lid-restore.md` / `doc-unfreeze.md`. Quiet-ops when Doc is down — not this upload. |

**Ownership (unchanged):** Zone owns the Worker upload. Garage owns HTML + waitlist e2e. Lead owns Doc `:8000`.

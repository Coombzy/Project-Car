# Brochure → Classic Pages git cutover

**Status:** Checklist / plan only — **not shipped**  
**Updated:** 2026-09-11  
**Related:** `STATUS.md` Live brochure + Option A **FULL 10/10** lock, `website-webapp-specification.md` §3 / §9, `brochure-worker-deploy.md` (Option A matrix), `member-host-cutover.md`, `member-zone-edge.md`, `ship-mvp-cut.md`, `api-stay-up.md`, `cors-origins.md`, `apps/website/README.md`

Plan the future cut from live Worker **`projectcar-brochure`** (Direct Upload of `apps/website/html`) to **Classic Cloudflare Pages git** connected to this repo. This file is a runbook. It does **not** change DNS, invent a live cutover, or start Zone / Garage work.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, Apex revival, or Google Calendar OAuth.

Until Ben finishes Cloudflare ↔ GitHub auth, **Direct Upload remains the locked live method** (`brochure-worker-deploy.md`). This file does **not** execute **#82**, Bulk Phase1, or Zone/Garage. **#82** Home canonical/og/sitemap `/index.html` is **not yet Worker-live** — that gate is **unchanged**.

---

## Reality today (do not claim this is done)

| Piece | Reality |
|-------|---------|
| **Git SSOT** | `apps/website/` in `Coombzy/Project-Car` (`website-webapp-specification.md` §3). Apex sidecar **stripped**. |
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** |
| **Deploy method** | **Direct Upload** of `apps/website/html` from `main` (`brochure-worker-deploy.md`). **Locked** until CF ↔ GitHub auth. |
| **Public hosts** | https://projectcar.ca and https://www.projectcar.ca |
| **Option A Dynamic pack** | **FULL 10/10** Active Dynamic **301**s (apex+www) — **LIVE**. Owns pretty-URL 301s: brochure-root-to-index (`/`→`/index.html`), brochure-shop-to-the-shop, brochure-shop-html-to-the-shop (`/shop.html`→`/the-shop.html`), membership/about/the-shop/contact/roadmap-to-html (+ trailing-slash). Receipt: `brochure-worker-deploy.md`. |
| **Worker `_redirects`** | **Thin** — **chat → contact only** (no `/` or `/shop`). Stays thin **after #82**. Do **not** fatten `_redirects` to replace the Zone pack. |
| **Pages `_redirects` ≠ pack** | Classic Pages `_redirects` is the same thin chat → contact file. It does **not** replace the Option A pack. Cutover must **keep** those Zone rules **or Bulk-import** them. |
| **Classic Pages git** | **Skipped.** Blocked on Cloudflare ↔ GitHub OAuth / auth. Not connected. Direct Upload stays the locked live method. |
| **Not the origin** | Doc `:8088`, `~/hermes-tools/project-car-website`, optional local nginx preview |
| **Apex sidecar** | **Deferred.** Do not revive. |
| **Member UI** | Still shop-UI `/member` on **`ops.`** + temporary **`app.`**. Separate plan: `member-host-cutover.md`. |

Waitlist on Membership / Contact is a **browser POST** to `https://api.projectcar.ca/waitlist`. Pages (like the Worker) only serve static HTML/JS. A green Pages deploy does not prove waitlist — Garage e2e after public `GET /health` is **200 when Doc origin is up** (`api-stay-up.md`). Lid-close mornings can be **530 / 1033**.

---

## 1. Prerequisite — Cloudflare ↔ GitHub auth (Ben)

Classic Pages git cannot connect until Ben finishes **Cloudflare ↔ GitHub OAuth / auth** on the account that owns `projectcar.ca`.

| Gate | Who | Notes |
|------|-----|--------|
| **CF ↔ GitHub OAuth / app install** | **Ben** | Cloudflare dashboard must be allowed to read `Coombzy/Project-Car` and create the Pages webhook. Agents do not complete this. |
| Until that lands | Zone | Keep **Direct Upload** of `apps/website/html` onto Worker **`projectcar-brochure`**. That is the locked live method. |
| After auth is done | Zone | Follow this plan. Do **not** start from this file alone while auth is still missing. |

Do not treat a docs merge as auth-complete. Do not invent a Pages project, a git connection, or a domain bind from this PR.

---

## 2. Target — Classic Pages from git

Verified against `website-webapp-specification.md` §3 and the live Worker upload path:

| Setting | Value | Why |
|---------|--------|-----|
| **Product** | **Classic Cloudflare Pages** (git-connected). Not Workers Assets as a new name for the same upload. Not Wrangler from CI in this plan. | Spec target is Pages. Worker Direct Upload is the interim. |
| **Repo** | `Coombzy/Project-Car` | Git SSOT. |
| **Production branch** | `main` | Same tip Garage merges HTML to. |
| **Pages root / output directory** | **`apps/website/html`** | This folder is the **site root** today (Worker Direct Upload). It holds `index.html`, the six pages, `waitlist.js`, `shop-config.js`, `styles.css`, `robots.txt`, `sitemap.xml`, `404.html`, favicons, `_redirects`, `_headers`, `assets/`. |
| **Git tree (SSOT)** | `apps/website/` | Spec §3. Docker / nginx in that folder are **local preview only** — do **not** set the Pages root to `apps/website` (no `index.html` at that path). |
| **Build command** | **None.** Framework preset None / static. | Static HTML. Do not add a Next.js or Vite build. |
| **Custom domains** | Bind **`projectcar.ca`** and **`www.projectcar.ca`** to the Pages project | Same public hosts as today. |
| **Not this project** | `apps/project-car/web` (shop-web) | Member / ops stay on Doc `:3000`. Do not fold Member into Pages. |

`_redirects` stays **thin**: Chat → Contact 301 only (**after #82** still thin — no `/` or `/shop`). `_headers` (robots/sitemap MIME) already live in `html/`. Classic Pages honors those at the publish root. Do **not** add an SPA `/* → /index.html` fallback.

**Pretty URLs are not in `_redirects`.** Option A Zone Dynamic Redirect pack is **FULL 10/10** and owns `/`, `/shop`, extensionless → `*.html` **301**s. A Pages cutover must **keep** those Zone rules **or Bulk-import** them. Do **not** assume Pages `_redirects` alone replace the pack.

Exact Pages project **name** is Zone’s when creating it. Do not reuse Worker **`projectcar-brochure`** as if it were already a Pages project.

---

## 3. Cut steps (Zone — only after §1)

Do **not** run these from this PR. Auth first. Member host (`STATUS.md` Next #1) still outranks starting this.

1. **Confirm auth.** Cloudflare can see `Coombzy/Project-Car`. If the GitHub connect screen still fails, stop. **Direct Upload stays the locked live method.** Do **not** start this cut while auth is missing.
2. **Create Classic Pages** from git: repo + `main` + root **`apps/website/html`**. No build. Wait for the first production deployment of the current `main` tip.
3. **Preview smoke on the `*.pages.dev` hostname** (or the Pages preview URL) before touching custom domains: six pages **200**, Home waitlist CTA present, **no** Chat nav/page, thin `_redirects` Chat → Contact if Pages honors it. Preview may **lack** Zone pretty-URL 301s (`/` / `/shop` / extensionless) — that is expected on `*.pages.dev`. Do not bind apex/www yet if the six pages or Chat check is wrong. Do **not** treat missing preview pretty-URLs as “Pages `_redirects` will cover them on apex.”
4. **Keep or Bulk-import the Option A pretty-URL pack** before / when binding custom domains. Zone Dynamic Redirect pack is **FULL 10/10** and owns `/` → `/index.html`, `/shop` (+ `/shop.html` → `/the-shop.html`), extensionless → `*.html`. Pages `_redirects` is chat → contact only (**after #82** still thin). **Keep** those Zone rules on apex+www **or Bulk-import** the pretty-URL pack. Do **not** detach/delete the pack and rely on Pages `_redirects` alone. Do **not** execute Bulk Phase1 / Redirect A from this file (parked Member-precondition — not a Pages shortcut). **#82** Worker-live gate is **unchanged**.
5. **Bind custom domains** `projectcar.ca` and `www.projectcar.ca` to the Pages project. Unbind / stop serving those hosts from Worker **`projectcar-brochure`**. Do **not** retarget `ops.`, `app.`, or `api.`.
6. **Confirm DNS** still points those two names at Cloudflare (already on CF). This is a **Pages custom-domain attach**, not a registrar move and not an `app.` cut.
7. **Public smoke** (§4) — include pretty-URL **301**s (`/` / `/shop` / extensionless → `*.html`). Then Garage waitlist e2e once `GET https://api.projectcar.ca/health` is **200** (skip e2e if lid-close **530 / 1033** — that is Doc, not Pages).
8. Leave the Worker project in place so rollback (§6) is a re-upload + re-attach, not a rebuild from memory.

Do not upload shop-web. Do not point Pages at Doc `:8088`. Do not revive Apex.

---

## 4. Smoke after cut

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed Pages deploy — check from a normal browser if `curl` is challenged (`website-improvements.md`).

| Check | Expect |
|-------|--------|
| Home | **200** Pages HTML. Waitlist / honest CTA present (“Join the waitlist” → Membership). **No** “Website progress” / `10%` bar. Status line is “Project Underway” only. |
| Pretty URLs | Zone pack **or Bulk-imported** equivalent still owns **301**s: `/` → `/index.html`, `/shop` → `/the-shop` (and `/shop.html` → `/the-shop.html`), extensionless → `*.html`. Fail if those 301s are gone and only Pages `_redirects` (chat → contact) remains. |
| Chat | **No** Chat nav or Chat page (stripped, PR #5). Thin `_redirects` maps `/chat.html` and `/chat` → Contact 301 if Pages honors it (Zone pack also has chat 301s — keep or Bulk-import; do not drop both). Contact stays email + Discord. |
| Pages | Home, About, The Shop, Membership, Roadmap, Contact all **200** from Pages HTML on **apex and www**. |
| Waitlist API first | `GET https://api.projectcar.ca/health` → **200** `{"status":"ok","service":"project-car-api"}` **when Doc origin is up**. If **502** or **530 / error 1033**, Doc lid-close / tunnel — `api-stay-up.md`. Do not treat that as a bad Pages deploy. |
| Waitlist e2e | **Garage** after health is 200: Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist` → **PASS**. CORS allowlist: `cors-origins.md`. |

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/
curl -sS -o /dev/null -w '%{http_code}\n' https://www.projectcar.ca/
# Pretty URLs must still 301 via Zone pack or Bulk-import (not Pages _redirects alone):
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/shop
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/membership
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

---

## 5. Locks (do not weaken)

- **No Apex revival.** Brochure stays Worker / Pages — no Apex sidecar, no brochure Chat page.
- **No `app.` alias cut.** Temporary alias stays until Ben cuts that DNS (`STATUS.md` Next #2). This plan does not touch `ops.` / `app.` tunnels.
- **Member host cutover is separate.** Customer-host Member UI is `member-host-cutover.md` (STATUS Next #1, **Ben GO**). Zone path-split: `member-zone-edge.md`. Both **outrank** executing this Pages plan. Do not start Member work from a Pages bind.
- **Do not replace the Option A pack with Pages `_redirects` alone.** Pretty URLs stay Zone Dynamic **301**s (**FULL 10/10**) **or** a Bulk import of that pack. Thin `_redirects` (chat → contact, **after #82** still thin) is not the pretty-URL SSOT.
- **#82 gate unchanged.** Home canonical/og/sitemap `/index.html` is **not yet Worker-live**. This plan does **not** execute #82, Bulk Phase1, or a main Reality-tip reconcile.
- **Direct Upload stays locked** until CF ↔ GitHub auth. Do not invent a live Pages cut from this file.
- **No Stripe / shop-open.** Interest waitlist only. Do not publish live prices or “book now.”
- **Shop API stays the lab tunnel.** `api.projectcar.ca` → Doc `:8000`. Pages does not host FastAPI.
- **Lead does not own brochure edge.** Do not hand Pages, Worker uploads, or domain binds to Lead.

---

## 6. Rollback

A bad Pages cut is an **origin / domain-bind** problem. Do **not** cut `app.`. Do **not** restart uvicorn. Do **not** start Member host work as a “fix.”

1. **Re-attach** `projectcar.ca` and `www.projectcar.ca` to Worker **`projectcar-brochure`**.
2. **Re-upload** per `brochure-worker-deploy.md`:
   - **Preferred:** roll back to the previous successful **Worker version**, or
   - **Or:** Direct Upload the last known-good `apps/website/html` tree from `main`.
3. Re-smoke Home + the six pages + no Chat on apex and www. Confirm pretty-URL **301**s still fire (Zone pack kept or Bulk-imported — not Pages `_redirects` alone).
4. If pages look right but waitlist fails: that is API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to leave apex/www on a broken Pages project.

Direct Upload stays the documented rollback path even after Pages is live.

---

## 7. Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Classic Pages project, git connect, custom-domain bind for `projectcar.ca` / `www`, DNS attach, Worker detach / rollback upload. **Keep** Option A Zone Dynamic **301**s **or Bulk-import** them at cut — do not drop the pack. | HTML content, waitlist e2e, uvicorn, Member host migration, `app.` cut, executing #82 / Bulk Phase1 from this file |
| **Garage** | Brochure HTML PRs under `apps/website/html`. Waitlist e2e after public `GET /health` is **200**. | Pages project, CF ↔ GitHub auth, DNS, Worker versions, tunnel |
| **Lead** | Doc `:8000` / LaunchAgent `com.projectcar.shop-api` (`api-stay-up.md`) | Brochure edge. Do not hand Pages or Worker uploads to Lead. |
| **Ben** | CF ↔ GitHub OAuth / auth. GO before anyone executes §3. | — |

Alerts can come from anyone who sees a bad public page. **Recovery of a bad Pages cut is Zone** (rollback above). **Recovery of a down API is Lead** (process) / **Zone** (tunnel only).

---

## 8. Sequencing vs STATUS Next #1

This plan exists so the steps are clear **when auth is ready**. It is **not** a reason to start Pages work, polish the brochure edge, or skip Member host.

| Order | Gate | Notes |
|-------|------|--------|
| **Now** | Direct Upload stays locked live | `brochure-worker-deploy.md`. Garage HTML PRs still upload via Zone. Option A pack stays **FULL 10/10** Zone **301**s. CF ↔ GitHub still blocks Pages git. |
| **Product Next #1** | Member UI → projectcar.ca | `member-host-cutover.md` + Zone path-split `member-zone-edge.md`. **Outranks** polishing or executing Pages git. |
| **This plan** | Classic Pages git | After Ben’s CF ↔ GitHub auth. Zone executes §3. Not a substitute for Next #1. |
| **Do not start** | Google Calendar OAuth / two-way sync | `ship-mvp-cut.md` **DEFER**. STATUS Next #6 — outranked by Member host. ICS + Connect stub stay thin. |
| **Later** | Ben cuts `app.` | STATUS Next #2. Not this file. |

**Out of scope for this file:** app code, DNS edits, Garage/Zone fan-out, Member host execution, Apex, Stripe, shop-open, Calendar OAuth, Mission Control cockpit, **#82** Worker upload, Bulk Phase1 execute, main Reality-tip reconcile.

**Ownership (unchanged):** Zone owns Cloudflare Pages / DNS / domains. Garage owns HTML + waitlist e2e. Lead does not own brochure edge.

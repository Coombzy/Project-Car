# Brochure → Classic Pages git cutover

**Status:** Checklist / plan only — **not shipped**  
**Updated:** 2026-09-07  
**Related:** `STATUS.md` Live brochure, `website-webapp-specification.md` §3 / §9, `brochure-worker-deploy.md`, `member-host-cutover.md`, `member-zone-edge.md`, `ship-mvp-cut.md`, `api-stay-up.md`, `cors-origins.md`, `apps/website/README.md`

Plan the future cut from live Worker **`projectcar-brochure`** (Direct Upload of `apps/website/html`) to **Classic Cloudflare Pages git** connected to this repo. This file is a runbook. It does **not** change DNS, invent a live cutover, or start Zone / Garage work.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, Apex revival, or Google Calendar OAuth.

Until Ben finishes Cloudflare ↔ GitHub auth, **Direct Upload remains the locked live method** (`brochure-worker-deploy.md`).

---

## Reality today (do not claim this is done)

| Piece | Reality |
|-------|---------|
| **Git SSOT** | `apps/website/` in `Coombzy/Project-Car` (`website-webapp-specification.md` §3). Apex sidecar **stripped**. |
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** |
| **Deploy method** | **Direct Upload** of `apps/website/html` from `main` (`brochure-worker-deploy.md`) |
| **Public hosts** | https://projectcar.ca and https://www.projectcar.ca |
| **Classic Pages git** | **Skipped.** Blocked on Cloudflare ↔ GitHub OAuth / auth. Not connected. |
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

`_redirects` (Chat → Contact 301 only) and `_headers` (robots/sitemap MIME) already live in `html/`. Classic Pages honors those at the publish root. Do **not** add an SPA `/* → /index.html` fallback.

Exact Pages project **name** is Zone’s when creating it. Do not reuse Worker **`projectcar-brochure`** as if it were already a Pages project.

---

## 3. Cut steps (Zone — only after §1)

Do **not** run these from this PR. Auth first. Member host (`STATUS.md` Next #1) still outranks starting this.

1. **Confirm auth.** Cloudflare can see `Coombzy/Project-Car`. If the GitHub connect screen still fails, stop. Direct Upload stays live.
2. **Create Classic Pages** from git: repo + `main` + root **`apps/website/html`**. No build. Wait for the first production deployment of the current `main` tip.
3. **Preview smoke on the `*.pages.dev` hostname** (or the Pages preview URL) before touching custom domains: six pages **200**, Home waitlist CTA present, **no** Chat nav/page, `_redirects` Chat → Contact if Pages honors it. Do not bind apex/www yet if preview is wrong.
4. **Bind custom domains** `projectcar.ca` and `www.projectcar.ca` to the Pages project. Unbind / stop serving those hosts from Worker **`projectcar-brochure`**. Do **not** retarget `ops.`, `app.`, or `api.`.
5. **Confirm DNS** still points those two names at Cloudflare (already on CF). This is a **Pages custom-domain attach**, not a registrar move and not an `app.` cut.
6. **Public smoke** (§4). Then Garage waitlist e2e once `GET https://api.projectcar.ca/health` is **200** (skip e2e if lid-close **530 / 1033** — that is Doc, not Pages).
7. Leave the Worker project in place so rollback (§6) is a re-upload + re-attach, not a rebuild from memory.

Do not upload shop-web. Do not point Pages at Doc `:8088`. Do not revive Apex.

---

## 4. Smoke after cut

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed Pages deploy — check from a normal browser if `curl` is challenged (`website-improvements.md`).

| Check | Expect |
|-------|--------|
| Home | **200** Pages HTML. Waitlist / honest CTA present (“Join the waitlist” → Membership). **No** “Website progress” / `10%` bar. Status line is “Project Underway” only. |
| Chat | **No** Chat nav or Chat page (stripped, PR #5). `_redirects` maps `/chat.html` and `/chat` → Contact 301 if Pages honors it. Contact stays email + Discord. |
| Pages | Home, About, The Shop, Membership, Roadmap, Contact all **200** from Pages HTML on **apex and www**. |
| Waitlist API first | `GET https://api.projectcar.ca/health` → **200** `{"status":"ok","service":"project-car-api"}` **when Doc origin is up**. If **502** or **530 / error 1033**, Doc lid-close / tunnel — `api-stay-up.md`. Do not treat that as a bad Pages deploy. |
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

---

## 5. Locks (do not weaken)

- **No Apex revival.** Brochure stays Worker / Pages — no Apex sidecar, no brochure Chat page.
- **No `app.` alias cut.** Temporary alias stays until Ben cuts that DNS (`STATUS.md` Next #2). This plan does not touch `ops.` / `app.` tunnels.
- **Member host cutover is separate.** Customer-host Member UI is `member-host-cutover.md` (STATUS Next #1, **Ben GO**). Zone path-split: `member-zone-edge.md`. Both **outrank** executing this Pages plan. Do not start Member work from a Pages bind.
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
3. Re-smoke Home + the six pages + no Chat on apex and www.
4. If pages look right but waitlist fails: that is API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to leave apex/www on a broken Pages project.

Direct Upload stays the documented rollback path even after Pages is live.

---

## 7. Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Classic Pages project, git connect, custom-domain bind for `projectcar.ca` / `www`, DNS attach, Worker detach / rollback upload. | HTML content, waitlist e2e, uvicorn, Member host migration, `app.` cut |
| **Garage** | Brochure HTML PRs under `apps/website/html`. Waitlist e2e after public `GET /health` is **200**. | Pages project, CF ↔ GitHub auth, DNS, Worker versions, tunnel |
| **Lead** | Doc `:8000` / LaunchAgent `com.projectcar.shop-api` (`api-stay-up.md`) | Brochure edge. Do not hand Pages or Worker uploads to Lead. |
| **Ben** | CF ↔ GitHub OAuth / auth. GO before anyone executes §3. | — |

Alerts can come from anyone who sees a bad public page. **Recovery of a bad Pages cut is Zone** (rollback above). **Recovery of a down API is Lead** (process) / **Zone** (tunnel only).

---

## 8. Sequencing vs STATUS Next #1

This plan exists so the steps are clear **when auth is ready**. It is **not** a reason to start Pages work, polish the brochure edge, or skip Member host.

| Order | Gate | Notes |
|-------|------|--------|
| **Now** | Direct Upload stays locked live | `brochure-worker-deploy.md`. Garage HTML PRs still upload via Zone. |
| **Product Next #1** | Member UI → projectcar.ca | `member-host-cutover.md` + Zone path-split `member-zone-edge.md`. **Outranks** polishing or executing Pages git. |
| **This plan** | Classic Pages git | After Ben’s CF ↔ GitHub auth. Zone executes §3. Not a substitute for Next #1. |
| **Do not start** | Google Calendar OAuth / two-way sync | `ship-mvp-cut.md` **DEFER**. STATUS Next #6 — outranked by Member host. ICS + Connect stub stay thin. |
| **Later** | Ben cuts `app.` | STATUS Next #2. Not this file. |

**Out of scope for this file:** app code, DNS edits, Garage/Zone fan-out, Member host execution, Apex, Stripe, shop-open, Calendar OAuth, Mission Control cockpit.

**Ownership (unchanged):** Zone owns Cloudflare Pages / DNS / domains. Garage owns HTML + waitlist e2e. Lead does not own brochure edge.

# Brochure Worker deploy — `projectcar-brochure`

**Status:** Standing runbook  
**Updated:** 2026-09-07  
**Related:** `STATUS.md` Live brochure, `website-webapp-specification.md` §3, `website-improvements.md`, `api-stay-up.md`, `cors-origins.md`, `apps/website/README.md`

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
| **Classic Pages git** | **Skipped.** Do not invent a Pages-git cutover from this runbook. |
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
7. **Smoke** the list below. Then Garage runs waitlist e2e once public `GET /health` is **200**.

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

---

## Rollback

A bad Direct Upload is a **Worker version** problem. Do **not** cut DNS. Do **not** touch ops/app. Do **not** restart uvicorn.

1. **Preferred:** Cloudflare dashboard → Worker **`projectcar-brochure`** → Deployments / Versions → roll back to the previous successful version.
2. **Or:** checkout the last known-good `main` tip and **re-upload** that `apps/website/html` tree (same steps as deploy).
3. Re-smoke Home + the six pages + no Chat.
4. If pages look right but waitlist fails: that is API / CORS / lid-close (`api-stay-up.md`, `cors-origins.md`) — not a reason to cut `projectcar.ca` off the Worker.

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Member host cutover | `member-host-cutover.md` — **Ben GO**. Do not start from a brochure upload. |
| Mission Control cockpit | Needs **Ben GO**. Not this Worker. |
| Stripe / shop-open claims | Locked off. Interest waitlist only. |
| Classic Pages git | Skipped. Do not invent a git-connected Pages cutover here. |
| Apex sidecar | Deferred. Do not revive. |
| DNS / `app.` alias | Do not cut or retarget. |
| Shop API / shop-web process | Lead (`:8000`) / `com.projectcar.shop-web` (`next start` on `:3000`). |

**Ownership (unchanged):** Zone owns the Worker upload. Garage owns HTML + waitlist e2e. Lead owns Doc `:8000`.

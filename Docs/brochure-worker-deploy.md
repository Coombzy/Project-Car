# Brochure Worker deploy — `projectcar-brochure`

**Status:** Standing runbook  
**Updated:** 2026-09-11  
**Related:** `STATUS.md` Live brochure + Option A **FULL 10/10** lock, `website-webapp-specification.md` §3, `website-improvements.md`, `brochure-security-headers.md` (P2-4 **LIVE** — do not re-apply from this runbook), `api-stay-up.md`, `shop-web-stay-up.md`, `cors-origins.md`, `brochure-pages-cutover.md`, `member-zone-edge.md` (Next #1 capacity-blocked until #82 + Bulk Phase1; **#83** is CI-only after **#82** base — **not** Bulk-gated; **never #81**), `apps/website/README.md`, `brochure-worker-ci.md` (paper CI + Option A Member-precondition receipt — **#82** mandatory purge Worker/Cache apex+www before body-freshness asserts; **never** Direct Upload from **#81**).

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
| **Option A Dynamic pack** | **FULL 10/10** Active Dynamic **301**s (apex+www) — capacity lock. No new Dynamic rules for brochure pretty-URLs. See lock below. |

Waitlist on Membership / Contact is a **browser POST** to the Shop API (`https://api.projectcar.ca/waitlist`). The Worker only serves static HTML/JS. API health and CORS live in `api-stay-up.md` and `cors-origins.md` — a green upload does not prove waitlist.

---

## Option A URL SSOT — Dynamic capacity lock (FULL 10/10)

**Paper lock — do not apply Zone Redirect / Bulk changes from this runbook.**

Cloudflare Dynamic Redirect Rules for Option A are **FULL 10/10** Active **301**s (apex+www). That pack owns live pretty URLs: brochure-root-to-index (`/`→`/index.html`), brochure-shop-to-the-shop, brochure-shop-html-to-the-shop (`/shop.html`→`/the-shop.html`), membership/about/the-shop/contact/roadmap-to-html (+ trailing-slash), brochure-chat-to-contact, brochure-chat-slash-to-contact. Worker Assets **`html_handling: none`** — `*.html` is canonical. Worker `_redirects` stays **thin**: chat → contact.html only (no `/` or `/shop`).

**Garage must not** invent new brochure extensionless pretty-URLs that need another Dynamic Redirect Rule until after **#82** is Worker-live **and** Bulk Phase1 frees Dynamic slots.

Redirect plan A is already parked (agent `/workspace` parking is outside this repo). In-repo Member-precondition receipt (Option A matrix + **#82 mandatory purge** before body-freshness): `brochure-worker-ci.md`. This table stays the upload-runbook copy. Bulk Phase1 brochure redirects apply **after #82 live** — do **not** execute from this runbook.

| Stay on Dynamic until migrate | Move to Bulk Phase1 (drafted, not live) |
|-------------------------------|-----------------------------------------|
| `root` / `index` / `shop` / `chat` (the live Dynamic rules that own them) | `membership` / `about` / `the-shop` / `contact` / `roadmap` ± slash → `*.html` |

**Keep `root` / `shop` Dynamic** until Member **needs** those remaining slots. Bulk Phase1 frees pretty-URL slots so Next #1 can add `/member*` path/tunnel ranking **BEFORE** the brochure Redirect pack, plus www→apex `/member*` **301** without fighting brochure dual-host. Do **not** migrate `root` / `shop` just to “make room.”

**Anti-collision (Member-precondition):** `/membership` / `/membership/` → **301** `/membership.html` is live Option A. `/member*` is **not** that rule. Today `/member*` is Worker **404**. Apex+www `/member/login` must **never** 301 into `membership.html`. `/member` is a prefix of `/membership` — rank + exact path, not `starts_with /member`.

**STATUS Next #1 is capacity-blocked** until **#82** Worker-live + this Bulk Phase1 slot-free. That is **not** Member GO, **not** this upload, **not** this tip-fold. **#83** is **not** this gate.

Do **not** create a new Dynamic Redirect Rule for a new pretty path. Do **not** execute Bulk Phase1 or Redirect A from a docs PR or this upload. **#82** Home canonical/og/sitemap `/index.html` is **not yet Worker-live**. Soft-530 **#80** (`waitlist.js?v=3` + `styles.css?v=36`) stays Worker-live. Soft-530 is **CLEAR** / **LIVE** — that does **not** unlock Member edge or Bulk Phase1.

---

## Hard lock / prefer merge (paper)

**Never #81.** Wrong lock was `#82 → Zone Direct Upload → Bulk Phase1 → #83`.

| Order | What | Gate |
|-------|------|------|
| **1** | **#82** Ben GO | Unchanged. Not executed from this runbook. |
| **2** | Zone Direct Upload + mandatory purge/freshness smoke | Ordered gate below. |
| **3** | **#83** merge after **#82** base | CI-only thin `_redirects` assert. **May run in parallel with the upload.** Does **not** need Bulk Phase1. Prefer merge on the **#82** base — do **not** wait for Bulk. |
| **4** | Bulk Phase1 | **After** that upload **only** to free Dynamic slots for Member edge. |

Do **not** write `#82 → upload → Bulk Phase1 → #83`. Option A **FULL 10/10** still capacity-blocks new Dynamic pretty-URLs and Member edge until Bulk — that is **not** a **#83** gate. Soft-530 companions **HOLD**. Reality quarantine until **#82** unchanged. Paper only — no Zone/Garage execute.

---

## STATUS Reality quarantine (held #70)

Until **#82** is Worker-live via Zone Direct Upload, **held #70 STATUS Reality tip / Option A** is brochure live SSOT. Do **not** execute Zone or Garage from **`main` STATUS Reality tip** — `main` still documents the pre-Option-A Worker (`_redirects` `/shop` **302** + `styles.css?v=35`). After **#82** upload, smoke is **ordered** (Direct Upload → **mandatory purge** → body freshness — gate below). **Then** **one** STATUS tip-fold reconciles `main` Reality to live: Home canonical/og/sitemap `https://projectcar.ca/index.html`; nav/logo not `href="/"`; Zone Redirect pack SSOT (**FULL 10/10** / Bulk Phase1 path); assets `waitlist.js?v=3` + `styles.css?v=36`; `/shop.html` → `/the-shop.html` **301 via Zone** (never reintroduce Worker `/shop` **302**); Worker `_redirects` **thin** (chat → contact only). Keep `/member*` Worker **404** until Member edge Ben GO after Bulk Phase1 — never **301** into `membership.html` (`member-zone-edge.md`). Soft-530 companion watches are **HOLD / not armed** (Ben skipped companion-watch approval ~14:35 America/Edmonton — do **not** re-ask). **#82** Ben GO unchanged. This runbook does **not** execute that upload, purge, reconcile, Bulk Phase1, or Member edge. Canonical banner + checklist: `STATUS.md`.

---

## #82 Worker Direct Upload smoke gate (paper — not executed)

**#82 Ben GO unchanged.** Soft-530 companion watches stay **HOLD / not armed**. This section does **not** execute Zone or Garage.

After **#82** is GO'd, Zone smoke is **ordered**. Do **not** skip purge. Do **not** treat `Cache-Control: no-cache, must-revalidate` as proof the new HTML is live — Worker HTML steady-state is `cf-cache-status: HIT` **plus** no-cache. Stale HIT HTML fails body freshness.

| Order | Gate | Pass |
|-------|------|------|
| **1** | **Direct Upload** `apps/website/html` onto Worker **`projectcar-brochure`** from the **#82** `main` tip | Worker version committed. Apex + www still attach. |
| **2** | **Mandatory purge** Worker / Cache for **`projectcar-brochure`** (**apex + www**) | Purge complete **before** any body curl. |
| **3** | **Then** assert body freshness (apex + www) | All rows below. |

**Body freshness (step 3 — after purge only):**

| Assert | Expect |
|--------|--------|
| Home canonical / og / sitemap | `https://projectcar.ca/index.html` (not `/`) |
| Nav / logo | **not** `href="/"` |
| `/shop.html` → `/the-shop.html` | **301 via Zone** (never Worker `/shop` **302**) |
| Worker `_redirects` | **thin**: chat → contact only (no `/` or `/shop`) |
| Soft-530 assets | `waitlist.js?v=3` + `styles.css?v=36` |

Generic post-deploy smoke below still applies for non-#82 uploads. **#82** must not treat that list as a substitute for this ordered gate.

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
4. **Direct Upload** the **`apps/website/html` directory** (that folder is the site root). Confirm the Worker name is still **`projectcar-brochure`** before you commit the deploy. **#82:** after this upload, **mandatory purge** Worker/Cache for **`projectcar-brochure`** (**apex + www**) **before** smoke. Do **not** skip. See the #82 smoke gate above.
5. **Confirm hosts.** Apex `projectcar.ca` and `www.projectcar.ca` still attach to this Worker. Do **not** edit DNS, retarget `ops.` / `app.` / `api.`, or connect Classic Pages git.
6. **Optional Zone setting** (already noted in `apps/website/README.md`): static `not_found_handling = "404-page"` so branded `404.html` is used. Do not add an SPA `/* → /index.html` fallback.
7. **Smoke** the list below. **#82** uses the ordered gate above (Direct Upload → **mandatory purge** → body freshness) — not this generic list alone. Then Garage runs waitlist e2e once public `GET /health` is **200**.

Do not upload shop-web (`apps/project-car/web`). Do not point the Worker at Doc `:8088`.

---

## Smoke after deploy

HTML from some networks hits a Cloudflare challenge (**403**). That is WAF, not a failed upload — check from a normal browser if `curl` is challenged (`website-improvements.md`).

**#82** is the ordered gate above: Direct Upload → **mandatory purge** `projectcar-brochure` Worker/Cache (apex+www) → **then** body freshness. Do **not** treat `Cache-Control: no-cache, must-revalidate` as sufficient — live HTML steady-state is `cf-cache-status: HIT` + no-cache.

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

## Security + cache headers (P2-4 — LIVE)

Worker **`projectcar-brochure` 200s** send the P2-4 security headers (2026-09-07 smoke PASS). Cache is split: HTML `no-cache, must-revalidate` vs `?v=` `.css`/`.js`/`.png` `public, max-age=31536000, immutable`. Unversioned `robots.txt` stays `max-age=0`. Record: **`brochure-security-headers.md`**. Zone Transform Rules: `brochure-security-headers`, `brochure-html-no-cache`, `brochure-asset-immutable` (apex+www). Do **not** re-apply headers, Transform Rules, or `_headers` from this runbook or a docs PR. P2-3 `?v=` is **LIVE** on Worker (`be60a01` / **#57**; Zone Direct Upload ~2026-09-07 16:01 America/Regina). Do **not** treat HTML `Cache-Control: no-cache, must-revalidate` as proof a new upload is live — Worker HTML steady-state is `cf-cache-status: HIT` **plus** no-cache. **#82** body-freshness asserts require the **mandatory purge** first.

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Member host cutover | `member-host-cutover.md` — **Ben GO** only after **#82** Worker-live + Bulk Phase1. Zone path-split: `member-zone-edge.md` §0. Capacity-blocked by Option A **FULL 10/10**. **#83** is CI-only after **#82** base — **not** this Bulk gate. **Never #81.** Do not start from a brochure upload. |
| `brochure-worker-ci.md` | **Drafted** (held **#70**). Paper CI + Option A Member-precondition receipt. **#82** ordered gate: Direct Upload → **mandatory** Worker/Cache purge (apex+www) → body freshness. **Never** Direct Upload from **#81** (draft + superseded). This runbook stays the upload click-path. |
| Mission Control cockpit | Needs **Ben GO**. Not this Worker. |
| Stripe / shop-open claims | Locked off. Interest waitlist only. |
| P2-4 security / cache headers | **LIVE** (2026-09-07). Record: `brochure-security-headers.md`. Do not re-apply from this upload. |
| Classic Pages git | Skipped. Plan: `brochure-pages-cutover.md`. Do not invent a git-connected Pages cutover here. |
| Apex sidecar | Deferred. Do not revive. |
| New brochure pretty-URLs / new Dynamic Redirect Rules | **FULL 10/10** lock. Wait for **#82** Worker-live + Bulk Phase1. Redirect A parked. |
| Bulk Phase1 / Redirect A apply | Parked paper. Do not execute from this runbook. |
| DNS / `app.` alias | Do not cut or retarget. |
| Shop API / shop-web process | Lead (`:8000`) / `com.projectcar.shop-web` (`next start` on `:3000`). See `api-stay-up.md` / `shop-web-stay-up.md`. |

**Ownership (unchanged):** Zone owns the Worker upload. Garage owns HTML + waitlist e2e. Lead owns Doc `:8000`.

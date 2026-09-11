# Project Car — Docs index

**Canonical:** `Coombzy/Project-Car` → `Docs/`  
**Engineering clone:** `~/src/Project-Car/Docs/`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (read copy; do not author there)  
**Updated:** 2026-09-11

`Coombzy/Automation/Docs/` is a **historical mirror**. Do not author product specs there.  
`~/Desktop/Project-Car-Docs/` is **retired**.  
Hermes skill `project-car/references/` holds **pointers + agent-only notes**, not a second full copy.

---

## Start here (product lock, 2026-09-06)

| Doc | What |
|-----|------|
| [master-overview-specification.md](master-overview-specification.md) | Vision and map |
| [platform-architecture.md](platform-architecture.md) | Monorepo, stack, bans |
| [project-car-application-specification.md](project-car-application-specification.md) | Shop product v1 (waitlist + Owner hoist booking) |
| [token-pricing.md](token-pricing.md) | Shop OS token pricing v1 (bands + overlay + fill; Owner-editable defaults) |
| [mission-control-architecture.md](mission-control-architecture.md) | Ben-only cockpit over Nextcloud (parked until Ben GO). 2026-09-11 honesty: dual-tunnel + vault LIVE on McKing (VW not Doc compose host); shop CF cutover paper; Soft-530 five-row = Doc shop hosts only |
| [integration-plan.md](integration-plan.md) | How the pieces connect |
| [high-level-apps-and-business-specification.md](high-level-apps-and-business-specification.md) | Two products + later fitness widget |
| [website-webapp-specification.md](website-webapp-specification.md) | Domain, tunnel, email, public site architecture |

---

## Living ops

| Doc | What |
|-----|------|
| [STATUS.md](STATUS.md) | What’s live, what’s next, locks — start here for 2026-09-11 (**git tip** `main` **`2dd61a2`** / **#74** [doc-unfreeze.md](doc-unfreeze.md) checklist **on `main`**; green **shop-os-ci** / lid-restore process-wake are **not** Ben GO unfreeze; [shop-os-ci.md](shop-os-ci.md) + workflow on `main` are git-only, not a Doc unfreeze; **#72** lid-restore no-auto-pull; **#71** google-calendar-oauth plan on `main`; OwnerShell **#69** / `b9f9019` stays **git-only**, not LIVE on Doc; Doc checkout **frozen** at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** until **Ben GO**; same **git-only** bucket as **#36**). OwnerShell + bay-hero dashboard are **on git** (not LIVE on Doc): primary nav Dashboard / Schedule / Chat / Members; secondary Inventory (Parts/Tools), Floor (Jobs/Cameras/Hoists), Admin (Payments/Tiers/Fill/Waitlist); compact dismissible demo banner; 3 primary metrics + 3×2 bay grid + Parts/To-dos split. Reality tip is the last **product/Docs** SHA — not finance tip-of-main `de290e2` (or later CCJ / Health Audit stamps). Shop-web host allowlist **#36** (`f952cd3`) and OwnerShell **#69** (`b9f9019`) are **git-only**. Doc checkout **frozen** at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) until **Ben GO** — plan-improve / Chief / Lead must **not** re-propose Doc pull/rebuild. Do **not** invent #36 or #69 LIVE on Doc. After **Ben GO**, pull is [doc-unfreeze.md](doc-unfreeze.md). **Soft-530 restore LIVE** 2026-09-11 ~06:50 America/Edmonton (Lead verified: public GET /health **200**; ops/app **307** → `/login`). Lookout **`projectcar-api-health-watch`** **resumed** (`enabled:true`) 2026-09-11 ~06:52 America/Edmonton (Lookout confirmed; live `/health` **200**). Lead interim probe ended. Docs **#30–#74** already on `main` (website **#52–#67**; Soft-530 **#80** Worker-live; **#71** google-calendar-oauth plan; **#72** lid-restore no-auto-pull; **#73** Shop OS CI; **#74** doc-unfreeze checklist). Brochure P1-1 / P1-3 **LIVE** on Worker (PR #52 / `5361212`). P2-1 **LIVE** on Worker (PR #55 / `453e44d` — absolute `og:url` / `og:image` + `twitter:card`). P2-2 **LIVE** on Worker (PR #56 / `ed41d23` — apex `rel=canonical` matches `og:url`; www serves apex canonicals). P2-3 **LIVE** on Worker (PR **#57** / `be60a01` — Zone Direct Upload ~16:01 America/Regina; `styles.css?v=34` + `banner-logo.png?v=30` on public HTML; Home/About/Contact at minimum; apex+www). P2-4 **LIVE** on Worker (2026-09-07 smoke PASS — Transform Rules `brochure-security-headers` / `brochure-html-no-cache` / `brochure-asset-immutable`; apex+www; Worker **200**s). P3-1 **LIVE** on Worker (PR **#61** / `88c9820` — Zone Direct Upload ~16:50 America/Regina; Home pitch + `cta-hero` Join the waitlist + Project Underway + Shop/Membership pointers; no feature-bullet dump). P3-5 **LIVE** on Worker (PR **#62** / `9d83bfc` — Zone Direct Upload; Shop/Membership/Roadmap “24/7 shop access (when operational)”; Home and About/Contact have no absolute 24/7). P3-4 **LIVE** on Worker (PR **#65** / `f191ad5` — Zone Direct Upload ~18:46 America/Regina; Shop facility/standards; Membership keeps “24/7 shop access (when operational)”; Home stays P3-1 pitch + `cta-hero` waitlist + Project Underway; no capability-bullet dump; `styles.css?v=34`; P2-4 headers still present). P4-2 **LIVE** on Worker (PR **#67** / `2b772ff` — Zone Direct Upload ~19:15 America/Regina; Home equal `cta-hero` Join the waitlist + Join Discord (`discord.gg/projectcar`); contact email · Discord; Membership waitlist form unchanged; Discord contact-primary + alongside-waitlist copy; sitemap lastmod bumps (2026-09-08 present); `styles.css?v=35` at that upload; P2-4 headers still; P3-4 Shop facility bullets still). **Live URL SSOT (Option A):** Zone Redirect pack is **FULL 10/10** Active Dynamic **301**s (apex+www) — capacity lock; no new Dynamic rules for brochure pretty-URLs. Owns pretty URLs: brochure-root-to-index (`/`→`/index.html`), brochure-shop-to-the-shop, brochure-shop-html-to-the-shop (`/shop.html`→`/the-shop.html`), membership/about/the-shop/contact/roadmap-to-html (+ trailing-slash), brochure-chat-to-contact, brochure-chat-slash-to-contact. Garage must **not** invent new brochure extensionless pretty-URLs until **#82** Worker-live + Bulk Phase1 (Redirect A parked). Worker Assets **`html_handling: none`** — `*.html` is canonical. Worker `_redirects` is **thin**: **chat → contact.html only** (no `/` or `/shop` in Worker `_redirects`). Soft-530 **#80** Worker-live: `waitlist.js?v=3` + `styles.css?v=36` + Soft-530 Discord honesty on Membership/Contact. Home canonical/og/sitemap must be `/index.html` after **#82** — **#82 not yet Worker-live**. **Brochure Reality quarantine (held #70):** until **#82** Worker-live + Zone Direct Upload, **#70 Reality tip / Option A** is brochure live SSOT — do **not** execute Zone/Garage from **`main` Reality tip** (`main` still pre-Option-A Worker `/shop` 302 + `styles.css?v=35`). After **#82**, one tip-fold reconciles `main` Reality (STATUS Live checklist). Soft-530 companions **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask). `/member*` stays Worker **404** until Member edge Ben GO after Bulk Phase1. P3-2 / P3-3 About stay held/deferred. **`ops.projectcar.ca` LIVE** when Doc origin is up (staff-on-shift, not Owner-only); `app.` = temporary alias. Calendar #18 + fill #20 + placeholders #21 + cookies #22 + Docs #23/#25/#30–#74 + schedule harden #24 + inventory #26 + Chat #27 + Dashboard #28 are Live on Doc. OwnerShell **#69** is **git-only** — Doc frozen until Ben GO. **#71** / **#72** / **#73** / **#74** are on `main` (plan + lid-restore freeze + git-only Shop OS CI + doc-unfreeze checklist). Inventory prefixes locked: B1–B6 / TC / PT (CM later). Chat v1 (human / polling) LIVE on ops/app demo. Build breadth vs Ship-MVP cut stay two gates. Stripe / shop-open / Apex / MC cockpit still need Ben GO. **Anti-goal:** McKing Tailnet Frigate **0.17.2** + Jellyfin lab ≠ Shop OS `/cameras` live and does **not** flip `pc.cameras`; Later cameras stays **Later**. |
| [token-pricing.md](token-pricing.md) | Token pricing lock (bands + overlay; Basic 1000 / Premium 1500; 6 hoists; shop hoist = Owner-only) |
| [website-improvements.md](website-improvements.md) | P0–P4 backlog for projectcar.ca (tick status as work ships) |
| [nextcloud-progress.md](nextcloud-progress.md) | Last live hub check on Doc (no secrets; 2026-08-16). Public-site / `:8088` rows point at STATUS / home-lab / Worker — not a new hub probe. |
| [doc-software-baseline.md](doc-software-baseline.md) | Doc M1 Max apps / settings |
| [home-lab-specification.md](home-lab-specification.md) | Host lock (2026-09-11): Doc tunnel = `cloud.` + `api.` + `app.` + `ops.` only (shop Soft-530 / KeepAlive); McKing / `lightning` = `vault.projectcar.ca` LIVE → `localhost:8222` (`/api/config` **2026.6.0**). Vault OUT of lid-restore / Doc KeepAlive. Shop CF cutover still paper. Brochure is Worker `projectcar-brochure`, not Doc. McKing Tailnet Frigate **0.17.2** + Jellyfin lab ≠ Shop OS `/cameras` / `pc.cameras`. |
| [doc-lid-restore.md](doc-lid-restore.md) | Ordered Lead wake/restore after lid-close / morning **530 / 1033**. Sequence only — process wake, **not** a `git pull`. Essays stay in api-stay-up / shop-web-stay-up / doc-software-baseline. After Ben GO, pull is [doc-unfreeze.md](doc-unfreeze.md). |
| [doc-unfreeze.md](doc-unfreeze.md) | Ordered **Ben GO** pull on Doc (`~/src/Project-Car`): confirm GO → `git pull` → alembic if needed → shop-web rebuild (`next start`) → new `BUILD_ID` ≠ `5swmVz` → #36 / #69 / OwnerDemoBanner smoke → public health + waitlist CORS. Green Shop OS CI is **not** this GO. Lid-restore stays process-only. |
| [api-stay-up.md](api-stay-up.md) | Keep https://api.projectcar.ca up (uvicorn on Doc; Zone owns tunnel). Brochure is Worker `projectcar-brochure`, not Doc `:8088`. |
| [shop-web-stay-up.md](shop-web-stay-up.md) | Keep https://ops.projectcar.ca (and temporary `app.`) up — LaunchAgent `com.projectcar.shop-web` runs **`next start`** on Doc `:3000`. Zone owns tunnel/DNS. |
| [deployment-guide.md](deployment-guide.md) | Index of stay-up / deploy runbooks (lid-close restore, Doc unfreeze after Ben GO, shop-web, API, Shop OS CI, member cutover + Zone path-split + `app.` alias cut plans, McKing shop-host cutover plan, brochure Worker, P2-4 headers (LIVE), Pages git plan, ship-MVP cut draft, Google Calendar OAuth plan, ops demo hardening **#79** Soft-530-CLEAR Next Ben GO). |
| [shop-os-ci.md](shop-os-ci.md) | Shop OS GitHub Actions quality gate (shop-api pytest + shop-web lint / typecheck / `next build`). Git-only — no Doc deploy, no tunnel secrets, no Worker upload. Green CI is **not** Doc unfreeze GO ([doc-unfreeze.md](doc-unfreeze.md)). Doc checkout stays frozen at `4cf8924` / `5swmVz`. |
| [brochure-worker-deploy.md](brochure-worker-deploy.md) | Standing brochure re-deploy: Zone Direct Upload of `apps/website/html` onto Worker `projectcar-brochure`. Classic Pages git skipped until auth — plan: `brochure-pages-cutover.md`. |
| [brochure-security-headers.md](brochure-security-headers.md) | P2-4 Zone Transform Rules **LIVE** (2026-09-07 smoke PASS): Worker `projectcar-brochure` security headers + HTML vs `?v=` cache split. Do **not** re-apply from a docs PR. |
| [brochure-pages-cutover.md](brochure-pages-cutover.md) | Brochure Worker → Classic Pages git checklist (plan only; blocked on CF ↔ GitHub auth). Do not start from this file. Member host + Zone path-split (`member-host-cutover.md`, `member-zone-edge.md`) outrank executing Pages git. |
| [cors-origins.md](cors-origins.md) | `CORS_ORIGINS` for brochure waitlist from https://projectcar.ca |
| [member-host-cutover.md](member-host-cutover.md) | Member UI → apex `projectcar.ca` checklist (plan only; Ben GO before Garage/Zone). Canonical cookie host = apex; planned 301 `www…/member*` → apex. Linked from STATUS Next #1. Edge / path-split slice: `member-zone-edge.md`. Does **not** require cutting `app.` first (`app-alias-cut.md`). |
| [member-zone-edge.md](member-zone-edge.md) | Zone Cloudflare path-split for `/member*` on apex (plan only). **Capacity-blocked** by Option A **FULL 10/10** — Ben GO only after **#82** Worker-live + Bulk Phase1. `/member*` ranked **BEFORE** brochure Redirect pack. Anti-collision: `/member/login` must **not** 301 into `membership.html` (today Worker 404). Brochure stays dual-host. Do not execute from this file. Cookie / CORS essay stays in `member-host-cutover.md`. |
| brochure-worker-ci.md | **Not drafted** (queued). Option A matrix / Member-precondition receipt lives in [brochure-worker-deploy.md](brochure-worker-deploy.md) until that file exists. |
| [app-alias-cut.md](app-alias-cut.md) | Temporary `app.projectcar.ca` cut checklist (plan only; STATUS Next #2). Do **not** execute DNS / tunnel / CORS from this file. Member cutover does **not** require this first. **`ops.` stays** the management host. |
| [ship-mvp-cut.md](ship-mvp-cut.md) | Draft public-MVP cut-vs-keep table (proposed candidates, not a Ben lock). Linked from STATUS Ship-MVP cut. |
| [google-calendar-oauth.md](google-calendar-oauth.md) | Google Calendar OAuth / two-way sync standing plan (plan only; STATUS Next #6 — not a GO). Env names, scopes, 501→live, token store, Apple ICS-only, rollback. |
| [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) | McKing Docker shop-host cutover (plan only — **not** Next #1, **not** GO). shop-api / shop-web / cloudflared + tunnel hostname reuse. Brochure stays Worker. No live cut from this file. |
| [ops-demo-hardening.md](ops-demo-hardening.md) | Soft-530-CLEAR **Next Ben GO** (**#79**, elevated on held **#70**). Strip plaintext `/login` password (email ok). Optional Cloudflare Access on `ops` (+ optional `app`) until OIDC; brochure stays public; exclude `api` waitlist. Do **not** execute Garage/Zone from this tip-fold. |

---

## Fleet process

| Doc | What |
|-----|------|
| [ai-agents-constitution.md](ai-agents-constitution.md) | Roles and routing |
| [agent-profiles-specification.md](agent-profiles-specification.md) | Hardware + jobs |
| [heartbeat-standards.md](heartbeat-standards.md) | Heartbeat loop; notes go in `MissionControl/Heartbeats/` |
| [security-playbook.md](security-playbook.md) | Incident response |
| [code-mater-android-integration-guide.md](code-mater-android-integration-guide.md) | Phone / Android agent |

---

## Later / do not implement from these

| Doc | Status |
|-----|--------|
| [eBay-Automation-Module-Spec.md](eBay-Automation-Module-Spec.md) | LATER / NOT V1 |
| [estate-sale-app-specification.md](estate-sale-app-specification.md) | LATER / NOT V1 |
| [project-car-integrated-marketplace-specification.md](project-car-integrated-marketplace-specification.md) | LATER / NOT V1 |

---

## Retired stubs (filenames kept so old links resolve)

| Doc | Go here instead |
|-----|-----------------|
| [deployment-guide.md](deployment-guide.md) | Now a living-ops index — lid-close restore, Doc unfreeze (Ben GO), shop-web / API stay-up, Shop OS CI, member cutover + Zone path-split + `app.` alias cut plans, McKing shop-host cutover plan, brochure Worker, P2-4 headers (LIVE), Pages git plan, Google Calendar OAuth plan, ops demo hardening **#79** |
| [phase-0-nextcloud-roadmap.md](phase-0-nextcloud-roadmap.md) | MC Phase A + nextcloud-progress |
| [doc-nextcloud-headscale-setup-guide.md](doc-nextcloud-headscale-setup-guide.md) | Tailscale + MariaDB — not Headscale/Postgres |

---

## Authoring rule

Edit files in this folder on `Coombzy/Project-Car`. After edits: commit + push. Mirror to Desktop **without** `--delete`.

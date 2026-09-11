# Deployment guide — living-ops index

**Status:** Index (filename kept so old links resolve)  
**Updated:** 2026-09-11  
**Canonical:** `Coombzy/Project-Car` → `Docs/deployment-guide.md`

This file is **not** a runbook. Use the living docs below.

---

## Stay-up / deploy

| Need | Doc |
|------|-----|
| Doc lid-close / morning 530 restore (ordered Lead sequence — process wake only) | `doc-lid-restore.md` |
| Doc unfreeze after **Ben GO** (pull / migrate / rebuild / `BUILD_ID` / smoke) | `doc-unfreeze.md` |
| Shop UI stay-up on Doc (`ops.` / temporary `app.`, `:3000`, **`next start`**) | `shop-web-stay-up.md` |
| Shop API stay-up on Doc (`api.`, `:8000`, uvicorn) | `api-stay-up.md` |
| Shop OS GitHub Actions quality gate (pytest + web typecheck / `next build`; git-only — **not** Doc deploy, **not** unfreeze GO) | `shop-os-ci.md` |
| Member UI → projectcar.ca (plan only; **Ben GO**) | `member-host-cutover.md` |
| Member path-split on projectcar.ca / www (Zone; plan only; **capacity-blocked** by Option A **FULL 10/10** — Ben GO only after **#82** Worker-live + Bulk Phase1) | `member-zone-edge.md` |
| Brochure Worker CI / Option A matrix (queued — **not drafted**; Member-precondition receipt is the parked Redirect inventory) | `brochure-worker-deploy.md` (until `brochure-worker-ci.md` exists) |
| Temporary `app.` alias cut (plan only; STATUS Next #2 — do **not** execute) | `app-alias-cut.md` |
| Public MVP cut-vs-keep (draft; not a Ben lock) | `ship-mvp-cut.md` |
| Brochure Worker Direct Upload (`projectcar-brochure`) | `brochure-worker-deploy.md` |
| Brochure security + cache headers (P2-4; **LIVE** — do **not** re-apply) | `brochure-security-headers.md` |
| Brochure → Classic Pages git (plan only; blocked on CF ↔ GitHub auth) | `brochure-pages-cutover.md` |
| Google Calendar OAuth / two-way sync (plan only; STATUS Next #6 — not a GO) | `google-calendar-oauth.md` |
| McKing shop-host cutover (plan only — Docker + tunnel hostname reuse; Soft-530 dual-run gate before public CF cut; **not** Next #1, **not** GO) | `mcking-shop-host-cutover.md` |
| Ops demo hardening — Soft-530-CLEAR **Next Ben GO** (**#79**): stop printing login password + optional Access on `ops` / `app` until OIDC (plan only; do **not** execute Garage/Zone from this tip-fold) | `ops-demo-hardening.md` |
| Dual-tunnel ownership (**separate** from shop CF cutover — vault **LIVE verified**): Doc = `cloud.` + `api.` + `app.` + `ops.` only; McKing-only `vault.` → `:8222` (`/alive` Lead **200** prefer; `/api/config` **2026.6.0**, Chief verified). Soft-530 five-row gate = shop hosts only (vault EXCLUDED). Lookout vault flip watch **LIVE/armed** (`enabled:true`, Lookout confirmed) on `/alive` every **5m** (fallback `/api/config` if `/alive` 404s) — Soft-530 / `api.` `/health` can stay green while vault dies; vault watch ≠ Soft-530 / Doc lid-restore. | `STATUS.md` Live / Locks · `home-lab-specification.md` · `api-stay-up.md` · `mcking-shop-host-cutover.md` |

---

## Elsewhere

| Need | Doc |
|------|-----|
| What’s live / host split | `STATUS.md` |
| Stack, host plan, bans | `platform-architecture.md` |
| Nextcloud / Vaultwarden / cockpit (parked). Dual-tunnel + vault LIVE on McKing (VW not Doc compose host); shop CF cutover paper; Soft-530 five-row = Doc shop hosts only | `mission-control-architecture.md` |
| Live hub / dual-tunnel machine map (Doc shop hosts + McKing vault LIVE) | `home-lab-specification.md` |
| Older hub probe on Doc (2026-08-16 rows can be stale) | `nextcloud-progress.md` |
| Doc apps / LaunchAgents / sleep | `doc-software-baseline.md` |
| Public site origin + tunnel | `website-webapp-specification.md` |
| Shop app first code slice | `project-car-application-specification.md` §13 |

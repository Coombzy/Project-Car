# Deployment guide — living-ops index

**Status:** Index (filename kept so old links resolve)  
**Updated:** 2026-09-08  
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
| Lookout `projectcar-api-health-watch` **paused** (`enabled:false`); Lead owns interim morning/public probe until re-armed | `api-stay-up.md` (Health / Ownership) · `STATUS.md` Live Shop API / Ops |
| Shop OS GitHub Actions quality gate (pytest + web typecheck / `next build`; git-only — **not** Doc deploy, **not** unfreeze GO) | `shop-os-ci.md` |
| Member UI → projectcar.ca (plan only; **Ben GO**) | `member-host-cutover.md` |
| Member path-split on projectcar.ca / www (Zone; plan only; **Ben GO**) | `member-zone-edge.md` |
| Temporary `app.` alias cut (plan only; STATUS Next #2 — do **not** execute) | `app-alias-cut.md` |
| Public MVP cut-vs-keep (draft; not a Ben lock) | `ship-mvp-cut.md` |
| Brochure Worker Direct Upload (`projectcar-brochure`) | `brochure-worker-deploy.md` |
| Brochure security + cache headers (P2-4; **LIVE** — do **not** re-apply) | `brochure-security-headers.md` |
| Brochure → Classic Pages git (plan only; blocked on CF ↔ GitHub auth) | `brochure-pages-cutover.md` |
| Google Calendar OAuth / two-way sync (plan only; STATUS Next #6 — not a GO) | `google-calendar-oauth.md` |

---

## Elsewhere

| Need | Doc |
|------|-----|
| What’s live / host split | `STATUS.md` |
| Stack, host plan, bans | `platform-architecture.md` |
| Nextcloud / Vaultwarden / cockpit | `mission-control-architecture.md` |
| Live hub status on Doc | `nextcloud-progress.md` |
| Doc apps / LaunchAgents / sleep | `doc-software-baseline.md` |
| Public site origin + tunnel | `website-webapp-specification.md` |
| Shop app first code slice | `project-car-application-specification.md` §13 |

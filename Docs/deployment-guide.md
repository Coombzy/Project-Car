# Deployment guide — living-ops index

**Status:** Index (filename kept so old links resolve)  
**Updated:** 2026-09-08  
**Canonical:** `Coombzy/Project-Car` → `Docs/deployment-guide.md`

This file is **not** a runbook. Use the living docs below.

---

## Required secrets

The API refuses to start unless `SHOP_DEV_MODE=1` when any of these is a dev placeholder, empty, or too short. Binding `127.0.0.1` does not count as dev. The startup error names the setting and does not print the value.

| Setting | Production rule |
|---------|-----------------|
| `OWNER_API_SECRET` | 32+ characters |
| `AI_API_SECRET` | 32+ characters |
| `SESSION_SECRET` | 32+ characters |
| `OWNER_PASSWORD` | 12+ characters, not the demo default |
| `SHOP_PROXY_SECRET` | 32+ characters when set (shared with the shop UI). Empty disables `X-Shop-Client-IP`. |
| `COOKIE_SECURE` | Leave unset so the session cookie is `Secure`. Set `false` only for local HTTP. `SHOP_DEV_MODE=1` also leaves it unset-by-default off. |
| `CLIENT_IP_HEADER` | Supported production value: `CF-Connecting-IP`. `X-Forwarded-For` is refused. The header is trusted only for peers in `TRUSTED_PROXIES` (default loopback). |
| `CORS_PUBLIC_ORIGINS` | Brochure hosts. `POST /waitlist` only, no credentials. |
| `CORS_CREDENTIALED_ORIGINS` | Shop UI hosts that may send cookies. |

`SHOP_DEV_MODE=1` is local dev only. A copy of `.env.example` with that line removed does not boot.

## Stay-up / deploy

| Need | Doc |
|------|-----|
| Doc lid-close / morning 530 restore (ordered Lead sequence — process wake only) | `doc-lid-restore.md` |
| Doc unfreeze after **Ben GO** (pull / migrate / rebuild / `BUILD_ID` / smoke) | `doc-unfreeze.md` |
| Shop UI stay-up on Doc (`ops.` / temporary `app.`, `:3000`, **`next start`**) | `shop-web-stay-up.md` |
| Shop API stay-up on Doc (`api.`, `:8000`, uvicorn) | `api-stay-up.md` |
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

# Deployment guide — living-ops index

**Status:** Index (filename kept so old links resolve)  
**Updated:** 2026-09-14  
**Canonical:** `Coombzy/Project-Car` → `Docs/deployment-guide.md`

This file is **not** a runbook. Use the living docs below.

---

## Stay-up / deploy

| Need | Doc |
|------|-----|
| Doc lid-close / morning 530 restore (ordered Lead sequence — process wake only). Weekend `api.` `/health` flip (plan-improve off Sat/Sun) uses this same wake — **not** unfreeze, **not** **#82**. After Soft-530 CLEAR: **post-CLEAR stay-up evidence** (cloudflared lastExit / KeepAlive loaded / caffeinate·CDM / Tailscale) for the next CF 1033. Soft-530 still **OPEN** this fold — paper does **not** invent CLEAR. | `doc-lid-restore.md` |
| Doc unfreeze after **Ben GO** (pull / migrate / rebuild / `BUILD_ID` / smoke). Soft-530 **CLEAR** Friday ≠ this GO. | `doc-unfreeze.md` |
| Shop UI stay-up on Doc (`ops.` / temporary `app.`, `:3000`, **`next start`**). Companion watches **HOLD**; weekend control plane = KeepAlive / lid-close. | `shop-web-stay-up.md` |
| Shop API stay-up on Doc (`api.`, `:8000`, uvicorn). Weekend flip coverage = Lookout `api.` `/health` + vault `/alive` **only**. | `api-stay-up.md` |
| McKing Vaultwarden + `cloudflared` stay-up (`vault.projectcar.ca` → `:8222`). Lookout `/alive` **separate** from Soft-530 `api.` `/health`. Weekend dual-outage proved Soft-530 (Doc) and vault (McKing) fail independently. Vault flip ≠ Doc lid-restore; Doc Soft-530 ≠ McKing vault wake. After vault CLEAR: **post-CLEAR stay-up evidence** (cloudflared.service / VW+DOMAIN / Tailscale / 1033→200 vs 502→200). Bitwarden import/rotate **blocked** until vault CLEAR. | `vault-stay-up.md` |
| Weekend dual-OPEN recovery glue (Soft-530 OPEN + vault OPEN): wake **Doc first, then McKing**; parallel only if both hosts appear on ListMachines. Identity lock: `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning` — no wrong-host Shell (`Mac.lan` is not Doc shop host). Independent CLEAR: Soft-530 = `api.` `/health` **200** + `ops.`/`app.` → `/login` + waitlist OPTIONS **200** + `cloud.` `status.php`; vault = `/alive` **200** + VW `/api/config`. Not Doc unfreeze, not **#82**, not Zone Direct Upload. Companions **HOLD**. Bitwarden import/rotate **blocked** until vault CLEAR. Wake order only — Soft-530 post-CLEAR is `doc-lid-restore.md`; vault post-CLEAR is `vault-stay-up.md`. | `dual-host-outage.md` |
| Soft-530 post-CLEAR stay-up evidence (next CF 1033): after lid-restore CLEAR, stamp cloudflared lastExit / KeepAlive loaded / caffeinate·CDM / Tailscale before walking away. Dual-host-outage is wake order; this is **Doc forensics**. Soft-530 still **OPEN** this fold as CF **1033** — paper does **not** invent CLEAR. | `doc-lid-restore.md` · `api-stay-up.md` · `STATUS.md` Live |
| Vault post-CLEAR stay-up evidence (next vault flip): after McKing vault CLEAR, stamp cloudflared.service ActiveState/Result/ExecMainStatus (or lastExit) / VW container healthy + `DOMAIN=https://vault.projectcar.ca` / Tailscale / whether recovery was **1033→200** vs **502→200**. Dual-host-outage is wake order; Soft-530 post-CLEAR is Doc forensics; this is **McKing forensics**. Living OPEN class: Soft-530 = CF **1033** tunnel-down; vault = **502** origin-down on `/alive` + `/api/config` (**not** 1033). Paper does **not** invent CLEAR. | `vault-stay-up.md` · `STATUS.md` Live |
| Weekend Soft-530 coverage (plan-improve off Sat/Sun): KeepAlive / lid-close control plane; no weekend Zone Direct Upload / Worker; first Monday plan-improve resumes Soft-530 smoke. Vault flips stay on `vault-stay-up.md`. Dual-OPEN glue: `dual-host-outage.md`. Soft-530 post-CLEAR: `doc-lid-restore.md`. Vault post-CLEAR: `vault-stay-up.md`. | `STATUS.md` Live / Locks · `api-stay-up.md` · `shop-web-stay-up.md` · `doc-lid-restore.md` · `vault-stay-up.md` · `dual-host-outage.md` |
| Shop OS GitHub Actions quality gate (pytest + web typecheck / `next build`; git-only — **not** Doc deploy, **not** unfreeze GO) | `shop-os-ci.md` |
| Member UI → projectcar.ca (plan only; **Ben GO**) | `member-host-cutover.md` |
| Member path-split on projectcar.ca / www (Zone; plan only; **capacity-blocked** by Option A **FULL 10/10** — Ben GO only after **#82** Worker-live + Bulk Phase1) | `member-zone-edge.md` |
| Brochure Worker CI / Option A **FULL 10/10** receipt (paper — Direct Upload → **mandatory** purge apex+www → body freshness; **never #81**) | `brochure-worker-ci.md` (upload click-path stays `brochure-worker-deploy.md`) |
| Temporary `app.` alias cut (plan only; STATUS Next #2 — do **not** execute) | `app-alias-cut.md` |
| Public MVP cut-vs-keep (draft; not a Ben lock) | `ship-mvp-cut.md` |
| Brochure Worker Direct Upload (`projectcar-brochure`) | `brochure-worker-deploy.md` |
| Brochure security + cache headers (P2-4; **LIVE** — do **not** re-apply) | `brochure-security-headers.md` |
| Brochure → Classic Pages git (plan only; blocked on CF ↔ GitHub auth) | `brochure-pages-cutover.md` |
| Google Calendar OAuth / two-way sync (plan only; STATUS Next #6 — not a GO) | `google-calendar-oauth.md` |
| McKing shop-host cutover (plan only — Docker + tunnel hostname reuse; Soft-530 dual-run gate before public CF cut; **not** Next #1, **not** GO) | `mcking-shop-host-cutover.md` |
| Ops demo hardening — Soft-530-CLEAR **Next Ben GO** (**#79**, **parallel to #82**): Garage **#79.1** strip-changeme is **git-only until Doc unfreeze+pull** (merge ≠ public `/login` clear while freeze holds `4cf8924` / **`5swmVz`**) + optional Access on `ops` / `app` until OIDC (plan only; do **not** execute Garage/Zone from this tip-fold) | `ops-demo-hardening.md` |
| Dual-tunnel ownership (**separate** from shop CF cutover — vault **LIVE verified**): Doc = `cloud.` + `api.` + `app.` + `ops.` only; McKing-only `vault.` → `:8222` (`/alive` Lead **200** prefer; `/api/config` **2026.6.0**, Chief verified) + **unpublished** NC. Public `cloud.` stays on **Doc** until Ben GO. McKing `/opt/mission-control` NC is lab/hub loopback-only. Paper path = Tailscale Serve HTTPS (mirror VW Serve at `lightning.tailbe8f55.ts.net`) + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a `cloud.*` CF cutover. Do **not** point `cloud.*` tunnel/CNAME at McKing until `status.php` parity vs Doc **and** Ben GO. Soft-530 five-row gate = shop hosts only (vault EXCLUDED). Lookout vault flip watch **LIVE/armed** (`enabled:true`, Lookout confirmed) on `/alive` every **5m** (fallback `/api/config` if `/alive` 404s) — Soft-530 / `api.` `/health` can stay green while vault dies; vault watch ≠ Soft-530 / Doc lid-restore. Weekend dual-outage proved the planes fail independently. Never touch the Doc mission-control tunnel token for `vault.`. | `vault-stay-up.md` · `STATUS.md` Live / Locks · `home-lab-specification.md` · `api-stay-up.md` · `mcking-shop-host-cutover.md` |

---

## Elsewhere

| Need | Doc |
|------|-----|
| What’s live / host split | `STATUS.md` |
| Stack, host plan, bans | `platform-architecture.md` |
| Nextcloud / Vaultwarden / cockpit (parked). Dual-tunnel + vault LIVE on McKing (VW not Doc compose host); shop CF cutover paper; Soft-530 five-row = Doc shop hosts only | `mission-control-architecture.md` |
| Live hub / dual-tunnel machine map (Doc shop hosts + McKing vault LIVE). Vault stay-up essay: `vault-stay-up.md`. Dual-OPEN glue: `dual-host-outage.md` | `home-lab-specification.md` |
| Older hub probe on Doc (2026-08-16 rows can be stale) | `nextcloud-progress.md` |
| Doc apps / LaunchAgents / sleep | `doc-software-baseline.md` |
| Public site origin + tunnel | `website-webapp-specification.md` |
| Shop app first code slice | `project-car-application-specification.md` §13 |

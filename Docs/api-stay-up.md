# API stay-up — `api.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-11  
**Public URL:** https://api.projectcar.ca  
**Related:** `doc-lid-restore.md` (ordered wake), `cors-origins.md`, `brochure-worker-deploy.md`, `member-host-cutover.md`, `shop-web-stay-up.md`, `mcking-shop-host-cutover.md` (future McKing **shop** host — plan only; **not** a cut; dual-tunnel vault is a **separate** living-ops row — **LIVE verified**), `apps/project-car/api/README.md`, `doc-software-baseline.md`, `nextcloud-progress.md` §3.5

Keep the Shop API reachable. This is operational reality, not a product-lock rewrite. Product-lock status: `STATUS.md` and `project-car-application-specification.md` §13.

---

## What serves it

| Piece | Reality (as of this repo) |
|-------|---------------------------|
| Process | **uvicorn** FastAPI app from `apps/project-car/api` (`app.main:app`) on `:8000` |
| **Primary stay-up** | LaunchAgent **`com.projectcar.shop-api`** on Doc (`KeepAlive`) |
| Wrapper | `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000` |
| Manual / local bind | `127.0.0.1:8000` — `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000` (dev only; KeepAlive is how prod-on-Doc stays up) |
| Working tree on Doc | `~/src/Project-Car` |
| Compose | `infra/compose/compose.yaml` is **shop Postgres only** (`shop-postgres`). It does **not** start the API. Do not invent an API container. |
| Edge | Host **cloudflared** on Doc for **this** API hostname. Zone owns the `api.projectcar.ca` hostname / DNS rule. Confirm the live Cloudflare mapping; do not assume a compose service. |
| Brochure site | Separate stack. **Live** origin is Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` — **not** the Doc `:8088` tunnel, **not** `~/hermes-tools/project-car-website`. Optional local nginx in `apps/website/` still maps to `:8088` for preview only. Not this API process. |
| Shop-web (ops / app) | LaunchAgent **`com.projectcar.shop-web`** on Doc runs **`next start`** (not `next dev`) on `:3000`. Not this API process. Stay-up: `shop-web-stay-up.md`. |

The LaunchAgent lives on **Doc**, not in this git repo. Compose still does not start the API. KeepAlive is the primary stay-up for process crashes / logout-style exits. **Lid-close / sleep still kills the Mac** — launchd cannot outrun sleep.

**Future host (plan only):** Shop API later moves to **McKing Docker** with Cloudflare tunnel **hostname reuse** (`api.projectcar.ca` stays the public name). Dual-run Doc KeepAlive, then cut — paper: `mcking-shop-host-cutover.md`. **Not** Next #1. **Not** GO’d. Do **not** execute from this stay-up file. Today’s origin is still Doc.

**Dual-tunnel ownership (separate from shop CF cutover — vault LIVE verified):** Doc tunnel = **`cloud.` + `api.` + `app.` + `ops.` only** (this API hostname stays on that Doc tunnel / Soft-530 KeepAlive). McKing-only tunnel **`vault.projectcar.ca` is LIVE**: `cloudflared` → `localhost:8222`; `/alive` Lead **200** (prefer); `/api/config` **2026.6.0** (Chief verified). Soft-530 five-row dual-run gate is **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**. Soft-530 / this API `GET /health` can stay **green while vault dies**. Lookout vault flip watch is **LIVE/armed** (`enabled:true`, Lookout confirmed) on `https://vault.projectcar.ca/alive` every **5m** (fallback `/api/config` if `/alive` 404s) — vault watch ≠ Soft-530 / Soft-530 companion watches / Doc lid-restore. Flip-only alerts: Chief + Lead only on 200↔non-200; never Ben; never mutate. Soft-530 five-row is Doc shop hosts `cloud.` / `api.` / `app.` / `ops.`, but Lookout Soft-530 coverage was **api-only** (`/health`) — `ops.` / `app.` (and `cloud.`) can **530 while this API stays 200** (same class as pre-vault-watch). Lookout **GO'd to arm** Soft-530 companion watches on `ops.` / `app.` `/login` (optional `cloud.` `/login`; Lead probed **200**) — **GO'd / arming** until Lookout confirms `enabled`. Companion watches ≠ vault `/alive` watch ≠ Doc lid-restore. Soft-530 **CLEAR** live. STATUS Live / Locks is canonical. Never move the Doc mission-control token for `vault.`. Soft-530 lid-restore / LaunchAgent KeepAlive must **not** recreate `vault.` ingress on Doc. Vault LIVE ≠ shop hostname leave ≠ Doc unfreeze. Shop CF cutover stays paper. Essay: `mcking-shop-host-cutover.md`.

---

## Lid-close / sleep

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel.

**Public symptom:** Cloudflare **502** or **530 / error 1033** (tunnel origin unreachable) on https://api.projectcar.ca. Brochure waitlist `POST /waitlist` fails in the browser. Treat **1033** alongside **502** — both mean the edge cannot reach Doc, not “Garage restart uvicorn.”

A Cloudflare **403** HTML challenge (`cf-mitigated: challenge`) is edge/WAF, not lid-close. Zone owns that. Do not treat it as “restart uvicorn.”

Mitigation already on Doc: Amphetamine + plugged-in no-sleep (`doc-software-baseline.md`) plus LaunchAgent KeepAlive once the host is awake. Those are not a guarantee. If the lid is closed, the public API is down until Doc is awake; KeepAlive should then start the wrapper again. If local `:8000` is still dead after wake, Lead checks `com.projectcar.shop-api` + `run-shop-api.sh`. Ordered wake after lid-close: `doc-lid-restore.md`.

---

## Health

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** — `{"status":"ok","service":"project-car-api"}` |
| Optional local (process up on Doc) | `GET http://127.0.0.1:8000/health` — same body |

**Blind spot:** this `/health` **200** does **not** prove `ops.` / `app.` / `cloud.` are up. Soft-530 five-row is Doc shop hosts `cloud.` / `api.` / `app.` / `ops.`, but Lookout Soft-530 coverage was **api-only**. `ops.` / `app.` (and `cloud.`) can **530 while this API stays 200** — same class as pre-vault-watch. Lookout **GO'd to arm** Soft-530 companion watches (STATUS Live): `https://ops.projectcar.ca/login` and `https://app.projectcar.ca/login` — ok = **200** (or **307** → `/login` then **200**); down = **502 / 530 / 1033 / timeout**. Optional `https://cloud.projectcar.ca/login` for five-row parity (Lead probed **200**). Cadence ≈ this api watch. Baselines (Lookout-owned): `/workspace/lookout/projectcar-ops-health-baseline.json` + `projectcar-app-health-baseline.json` (+ cloud if armed). Flip-only: **Chief + Lead only**; **never Ben**; never restart / mutate. **GO'd / arming** until Lookout confirms `enabled`. Soft-530 companion watches ≠ vault `/alive` watch ≠ Doc lid-restore. Soft-530 **CLEAR** live. Vault flip watch stays **LIVE/armed**. Shop-web probes: `shop-web-stay-up.md`.

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
# optional, on Doc:
curl -sS http://127.0.0.1:8000/health
```

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lookout** | `projectcar-api-health-watch` **resumed** (`enabled:true`) 2026-09-11 ~06:52 America/Edmonton (Lookout confirmed; live `/health` **200**). Lead interim probe ended. **#78:** freeze does **not** block this re-arm — watch is already **`enabled:true`** while Doc stays frozen at `4cf8924` / `5swmVz`. Soft-530 companion watches on `ops.` / `app.` `/login` (optional `cloud.` `/login`) are **GO'd to arm** — **GO'd / arming** until Lookout confirms `enabled`. Companion watches ≠ this api `/health` watch ≠ vault `/alive` watch ≠ Doc lid-restore. | Process restore on Doc; Cloudflare tunnel / DNS edits; claiming companion watches `enabled:true` before Lookout confirms |
| **Lead** | uvicorn / process stay-up and recovery on Doc | Cloudflare tunnel / DNS edits; interim morning probe (ended 2026-09-11) |
| **Zone** | Cloudflare tunnel + DNS for `api.projectcar.ca` | Restarting uvicorn |
| **Garage** | Browser e2e of the brochure waitlist only | Restarting uvicorn, tunnel, or DNS |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, or a failed waitlist submit. **Recovery of the process is Lead only.** Lookout owns the live api watch (`enabled:true`) and **GO'd to arm** Soft-530 companion watches (`ops.` / `app.` `/login`). Do not instruct Garage (or anyone else) to restart uvicorn. Companion flip alerts: **Chief + Lead only**; **never Ben**; never restart / mutate.

---

## Recovery checklist

Morning lid-close / **530 / 1033** (ordered sequence): `doc-lid-restore.md`.

1. **Public health.** `GET https://api.projectcar.ca/health` → 200? If yes, stop. 403 challenge page → Zone (not Lead).
2. **Doc awake?** Lid closed / sleep → **502** or **530 / error 1033**. Wake Doc (Amphetamine session if it should stay up).
3. **Lead — origin.** On Doc, `GET http://127.0.0.1:8000/health`. If it fails after wake, Lead checks LaunchAgent `com.projectcar.shop-api` (KeepAlive) and `~/hermes-tools/mission-control/shop-api/run-shop-api.sh`. Do not hand that restart to Garage or Zone.
4. **Postgres (only if origin errors on DB).** `docker compose -f infra/compose/compose.yaml` is the shop DB, not the API process. Lead checks it if uvicorn is up but requests 5xx.
5. **Zone — edge.** Local `:8000` health OK but public **502** / **530 / 1033** / DNS miss → Zone checks host cloudflared + the `api.projectcar.ca` hostname rule. Lead does not edit Cloudflare.
6. **Garage — after.** When public health is 200, Garage may re-run brochure waitlist e2e. Form only. No process restarts.

CORS / waitlist preflight after an `.env` change: `cors-origins.md`.

Public HTTPS session cookies: shop-web KeepAlive **`com.projectcar.shop-web`** runs **`next start`** (`NODE_ENV=production`), not `next dev`. Doc already uses `COOKIE_SECURE=true` (API) and `SHOP_COOKIE_SECURE=true` (shop UI) so Firefox will store cookies on `app.` / `ops.`. Local `http://127.0.0.1:3000` should leave those unset or false. See `shop-web-stay-up.md` and `apps/project-car/web/README.md`. Member-on-projectcar.ca cookie / CORS plan: `member-host-cutover.md` (not shipped).

# API stay-up — `api.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-11  
**Public URL:** https://api.projectcar.ca  
**Related:** `doc-lid-restore.md` (ordered wake), `cors-origins.md`, `brochure-worker-deploy.md`, `member-host-cutover.md`, `shop-web-stay-up.md`, `apps/project-car/api/README.md`, `doc-software-baseline.md`, `nextcloud-progress.md` §3.5

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

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
# optional, on Doc:
curl -sS http://127.0.0.1:8000/health
```

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lookout** | `projectcar-api-health-watch` (resume GO’d 2026-09-11; re-arm in progress — do **not** claim `enabled:true` until Lookout confirms). Lead interim probe ended. | Process restore on Doc; Cloudflare tunnel / DNS edits |
| **Lead** | uvicorn / process stay-up and recovery on Doc | Cloudflare tunnel / DNS edits; interim morning probe (ended 2026-09-11) |
| **Zone** | Cloudflare tunnel + DNS for `api.projectcar.ca` | Restarting uvicorn |
| **Garage** | Browser e2e of the brochure waitlist only | Restarting uvicorn, tunnel, or DNS |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, or a failed waitlist submit. **Recovery of the process is Lead only.** Lookout owns the live watch when re-armed. Do not instruct Garage (or anyone else) to restart uvicorn.

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

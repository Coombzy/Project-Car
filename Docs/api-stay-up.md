# API stay-up — `api.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-06  
**Public URL:** https://api.projectcar.ca  
**Related:** `cors-origins.md`, `apps/project-car/api/README.md`, `doc-software-baseline.md`, `nextcloud-progress.md` §3.5

Keep the Shop API reachable. This is operational reality, not a product-lock rewrite. Lead may later sync product-lock wording to match.

---

## What serves it

| Piece | Reality (as of this repo) |
|-------|---------------------------|
| Process | **uvicorn** FastAPI app from `apps/project-car/api` (`app.main:app`) |
| Documented bind | `127.0.0.1:8000` — `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000` |
| Working tree on Doc | `~/src/Project-Car` |
| Compose | `infra/compose/compose.yaml` is **shop Postgres only** (`shop-postgres`). It does **not** start the API. Do not invent an API container. |
| Edge | Host **cloudflared** on Doc (same pattern as the brochure). Zone owns the `api.projectcar.ca` hostname / DNS rule. Confirm the live Cloudflare mapping; do not assume a compose service. |
| Brochure site | Separate stack (`apps/website` / Doc `~/hermes-tools/project-car-website` on `:8088`). Not this process. |

There is no API systemd/launchd unit or API compose service in this repo.

---

## Lid-close / sleep

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel.

**Public symptom:** Cloudflare **502** on https://api.projectcar.ca. Brochure waitlist `POST /waitlist` fails in the browser.

Mitigation already on Doc: Amphetamine + plugged-in no-sleep (`doc-software-baseline.md`). That is a host habit, not a guarantee. If the lid is closed, the public API is down until Doc is awake and uvicorn is running again.

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
| **Lead** | uvicorn / process stay-up and recovery on Doc | Cloudflare tunnel / DNS edits |
| **Zone** | Cloudflare tunnel + DNS for `api.projectcar.ca` | Restarting uvicorn |
| **Garage** | Browser e2e of the brochure waitlist only | Restarting uvicorn, tunnel, or DNS |

Alerts can come from anyone who sees a 502 or a failed waitlist submit. **Recovery of the process is Lead only.** Do not instruct Garage (or anyone else) to restart uvicorn.

---

## Recovery checklist

1. **Public health.** `GET https://api.projectcar.ca/health` → 200? If yes, stop.
2. **Doc awake?** Lid closed / sleep → 502. Wake Doc (Amphetamine session if it should stay up).
3. **Lead — origin.** On Doc, confirm uvicorn in `apps/project-car/api` and `GET http://127.0.0.1:8000/health`. If local health fails, Lead brings uvicorn back. Do not hand that restart to Garage or Zone.
4. **Postgres (only if origin errors on DB).** `docker compose -f infra/compose/compose.yaml` is the shop DB, not the API process. Lead checks it if uvicorn is up but requests 5xx.
5. **Zone — edge.** Local `:8000` health OK but public 502 / DNS miss → Zone checks host cloudflared + the `api.projectcar.ca` hostname rule. Lead does not edit Cloudflare.
6. **Garage — after.** When public health is 200, Garage may re-run brochure waitlist e2e. Form only. No process restarts.

CORS / waitlist preflight after an `.env` change: `cors-origins.md`.

# CORS_ORIGINS — brochure waitlist

**Status:** Living ops  
**Updated:** 2026-09-07  
**Related:** `api-stay-up.md`, `doc-lid-restore.md`, `brochure-worker-deploy.md`, `member-host-cutover.md`, `app-alias-cut.md` (later drop of `https://app.projectcar.ca` — **not** this file), `apps/project-car/api/.env.example`, `apps/project-car/api/app/config.py`, `apps/website/html/waitlist.js`

Browser waitlist from https://projectcar.ca must be allowed to call the Shop API. After any `.env` change, **Lead** restarts the API process on Doc.

---

## What the API uses

Env var: **`CORS_ORIGINS`** (Pydantic `Settings.cors_origins` in `apps/project-car/api/app/config.py`).

Comma-separated Origin allowlist. `*` is **dropped** in code — never set `*` for production, and do not rely on a wildcard “just this once.”

Must include **`https://projectcar.ca`**. Live allowlist also includes `https://www.projectcar.ca`, localhost Owner-UI ports, **`https://ops.projectcar.ca`** (LIVE management origin, 2026-09-06 ~12:55), and the temporary alias **`https://app.projectcar.ca`** (still live until Ben cuts that DNS). Do **not** drop `app.` from a docs PR — plan only: `app-alias-cut.md` (after ops-only smoke). **`ops.` stays.**

```
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://projectcar.ca,https://www.projectcar.ca,https://ops.projectcar.ca,https://app.projectcar.ca
```

Empty `CORS_ORIGINS` → no CORS middleware (browser waitlist will fail).

Live file on Doc: `apps/project-car/api/.env` (copy of `.env.example`; do not commit secrets).

---

## Brochure POST

The public form (`apps/website/html/waitlist.js`, `shop-config.js`) POSTs JSON to:

`https://api.projectcar.ca/waitlist`

`Origin` must be an allowlist entry or the browser drops the response.

---

## After `.env` change

1. Edit `CORS_ORIGINS` on Doc (`apps/project-car/api/.env`).
2. **Lead** restarts the uvicorn process on Doc. Settings are loaded at process start (`get_settings` is cached). No restart → old allowlist stays live.
3. Smoke OPTIONS (below). Then Garage may run brochure waitlist e2e.

Do not ask Garage or Zone to restart uvicorn. Zone owns tunnel/DNS only (`api-stay-up.md`).

---

## OPTIONS smoke

```bash
curl -sS -D - -o /dev/null -X OPTIONS https://api.projectcar.ca/waitlist \
  -H 'Origin: https://projectcar.ca' \
  -H 'Access-Control-Request-Method: POST'
```

**Expect:** HTTP **200** and `Access-Control-Allow-Origin: https://projectcar.ca`.

Wrong or missing origin → no `Access-Control-Allow-Origin: https://projectcar.ca`. Public health can still be 200 (`GET /health`); that does not prove CORS.

---

## Doc lid-close / 530

When Doc is asleep or the tunnel origin is unreachable, public **OPTIONS** and **POST /waitlist** fail with Cloudflare **530 / error 1033**. That is **expected lid-close** — **not a CORS regression**. Do **not** restart uvicorn chasing it.

Brochure `waitlist.js` **mailto fallback** is the user path while the origin is down. Run brochure waitlist e2e **only** when public **GET /health** is **200**.

Live probe: Lookout **`projectcar-api-health-watch`**. Ordered restore: [doc-lid-restore.md](doc-lid-restore.md).

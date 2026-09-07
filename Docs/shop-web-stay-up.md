# Shop-web stay-up — `ops.projectcar.ca` / `app.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-07  
**Public URLs:** https://ops.projectcar.ca (LIVE management) · https://app.projectcar.ca (temporary alias)  
**Related:** `api-stay-up.md`, `doc-software-baseline.md`, `brochure-worker-deploy.md`, `STATUS.md` host split, `member-host-cutover.md` (plan only), `apps/project-car/web/README.md`

Keep the Shop OS UI reachable. This is operational reality, not a product-lock rewrite. Product-lock status: `STATUS.md` and `project-car-application-specification.md` §13.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, or a cut `app.` alias.

---

## What serves it

| Piece | Reality (as of this repo) |
|-------|---------------------------|
| Process | **Next.js** shop-web from `apps/project-car/web` on Doc **`:3000`** |
| **Primary stay-up** | LaunchAgent **`com.projectcar.shop-web`** on Doc (`KeepAlive`) |
| Wrapper | `~/hermes-tools/mission-control/shop-web/run-shop-web.sh` → **`next start`** `:3000` |
| **LOCKED command** | KeepAlive must run **`next start`** (production). **Not** `next dev`. |
| Manual / local bind | `127.0.0.1:3000` — `npm run dev` is **dev only**. KeepAlive is how ops/app-on-Doc stays up. |
| Working tree on Doc | `~/src/Project-Car` |
| Compose | `infra/compose/compose.yaml` is **shop Postgres only**. It does **not** start shop-web. Do not invent a Next.js container. |
| Edge | Host **cloudflared** on Doc for **`ops.`** and the temporary **`app.`** alias. Zone owns those hostname / DNS rules. Origin must be **`http://127.0.0.1:3000`**. |
| Shop API | Separate process. LaunchAgent **`com.projectcar.shop-api`** → uvicorn `:8000`. See `api-stay-up.md`. |
| Brochure site | Separate stack. **Live** origin is Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` — **not** this Next.js process. Re-deploy: `brochure-worker-deploy.md`. |

The LaunchAgent lives on **Doc**, not in this git repo. Compose still does not start shop-web. KeepAlive is the primary stay-up for process crashes / logout-style exits. **Lid-close / sleep still kills the Mac** — launchd cannot outrun sleep.

---

## LOCKED: `next start`, not `next dev`

KeepAlive **must** run **`next start`**. That sets `NODE_ENV=production` and serves the built `.next` tree.

`next dev` on Doc was the **Schedule-outage root cause**. The dev server flaps: **EADDRINUSE**, KeepAlive restart loops, and Cloudflare **connection refused** on the tunnel. Do not “temporarily” point the LaunchAgent at `npm run dev` / `next dev`.

If you see `next dev` in `ps`, repeated LaunchAgent exits, or a missing `.next/BUILD_ID`, that is **process flap** — not lid-close. Fix by enforcing `next start` and the rebuild path below.

---

## Rebuild after web merges on Doc

A `git pull` on `main` does **not** update the running UI. `next start` serves the last **`npm run build`**. Do not leave a stale `.next` behind a new `main` pull.

After Garage merges shop-web (`apps/project-car/web`) onto `main`, **Lead** on Doc:

1. **Note the tip** you intend (`git rev-parse HEAD` in `~/src/Project-Car` after `git pull origin main`).
2. **Boot out** LaunchAgent `com.projectcar.shop-web` so nothing is bound to `:3000`.
3. **`npm run build`** in the Doc working tree (`apps/project-car/web`).
4. **Kickstart** KeepAlive `com.projectcar.shop-web` (wrapper → `next start`).
5. **Verify `.next/BUILD_ID`** matches the tip you intended. If `BUILD_ID` is missing or stale, you are still on the old build — do not call the merge live.

```bash
# on Doc, after pulling the intended main tip into ~/src/Project-Car
launchctl bootout gui/$(id -u)/com.projectcar.shop-web
cd ~/src/Project-Car/apps/project-car/web
npm run build
cat .next/BUILD_ID
launchctl kickstart -k gui/$(id -u)/com.projectcar.shop-web
# confirm next start (not next dev) and BUILD_ID still present
```

Last recorded shop-web **BUILD** on Doc (STATUS): after Dashboard **#28** (`main` `afb37f9`, `BUILD_ID` `5swmVz-T2CqKEQzTk1ifU`). Update STATUS when Lead ships a newer build.

---

## Lid-close / sleep vs process flap

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel. Amphetamine + plugged-in no-sleep (`doc-software-baseline.md`) plus LaunchAgent KeepAlive once the host is awake are mitigation, not a guarantee.

**Same class as `api-stay-up.md` (edge cannot reach Doc):**

- Cloudflare **530 / error 1033**, **502**, or tunnel origin unreachable on `ops.` / `app.`
- **Doc asleep**, lid closed, or **cloudflared dead**

Treat **1033** alongside **530 / 502** — both mean the edge cannot reach Doc, not “Garage restart Next.” Wake Doc. If local `:3000` is still dead after wake, Lead checks `com.projectcar.shop-web` + `run-shop-web.sh`.

**Process flap (not sleep):**

- KeepAlive running **`next dev`**
- **EADDRINUSE** on `:3000`
- Repeated LaunchAgent restart
- **`.next/BUILD_ID` missing** or a stale build after a `main` pull

Fix: enforce **`next start`** + the rebuild path above. Do not treat flap as a DNS rollback or a reason to cut the `app.` alias.

A Cloudflare **403** HTML challenge (`cf-mitigated: challenge`) is edge/WAF, not lid-close and not flap. Zone owns that. Do not treat it as “restart shop-web.”

---

## Tunnel origin

Cloudflare tunnel for **`ops.projectcar.ca`** and the temporary **`app.projectcar.ca`** alias must target **`http://127.0.0.1:3000`**.

Do **not** use bare `localhost`. Bare `localhost` can resolve to IPv6 **`[::1]`** and historically **502**’d the edge while IPv4 `:3000` was fine.

| Role | Owns |
|------|------|
| **Zone** | Tunnel hostname / DNS rules for `ops.` and `app.` |
| **Lead** | Process stay-up on Doc (`:3000`, KeepAlive, rebuild) |

Lead does not edit Cloudflare. Zone does not restart shop-web. Do **not** cut the `app.` alias from this runbook.

---

## Secure cookies

Public HTTPS ops/app demo needs **Secure** session cookies so Firefox (and others) will store them.

| Where | What |
|-------|------|
| Shop UI | `SHOP_COOKIE_SECURE=true` on Doc |
| Shop API | `COOKIE_SECURE=true` on Doc |
| KeepAlive | **`next start`** sets `NODE_ENV=production` — Secure is on even without the env override. Keep the env flags anyway. |
| Local HTTP | `http://127.0.0.1:3000` leaves `COOKIE_SECURE` / `SHOP_COOKIE_SECURE` **unset or false**. A Secure cookie will not stick on plain HTTP. |

Demo cookies (`pc_owner_session` / `pc_member_session`) — **not OIDC**. Member-on-projectcar.ca cookie / CORS plan: `member-host-cutover.md` (**not shipped**).

---

## Public smoke

Probe the **public** hosts. No localhost hop in `Location`. Some clients have **flaky local DNS** for `ops.` — use the **`app.`** alias. That is a client cache miss, **not** a product rollback and **not** “ops is not live.”

| Check | Expect |
|-------|--------|
| `GET https://ops.projectcar.ca/` | Redirect `Location: https://ops.projectcar.ca/login` (no `localhost`) |
| `GET https://ops.projectcar.ca/login` | **200** |
| `GET https://app.projectcar.ca/` | Redirect `Location: https://app.projectcar.ca/login` (no `localhost`) |
| `GET https://app.projectcar.ca/login` | **200** |
| Optional local (process up on Doc) | `GET http://127.0.0.1:3000/login` — **200** |

```bash
curl -sS -D - -o /dev/null https://ops.projectcar.ca/ | grep -iE 'HTTP/|location:'
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
# if ops. DNS is flaky on this client:
curl -sS -D - -o /dev/null https://app.projectcar.ca/ | grep -iE 'HTTP/|location:'
curl -sS -o /dev/null -w '%{http_code}\n' https://app.projectcar.ca/login
# optional, on Doc:
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3000/login
```

Still the Doc demo. Not a shop opening.

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lead** | shop-web process stay-up and recovery on Doc (`com.projectcar.shop-web`, wrapper, `next start`, rebuild / `BUILD_ID`) | Cloudflare tunnel / DNS edits |
| **Zone** | Cloudflare tunnel + DNS for `ops.projectcar.ca` and temporary `app.projectcar.ca` | Restarting shop-web |
| **Garage** | shop-web PRs under `apps/project-car/web` | Restarting shop-web, tunnel, or DNS |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, a login redirect to localhost, or a flapping UI. **Recovery of the process is Lead only.** Do not instruct Garage (or anyone else) to restart shop-web.

---

## Recovery checklist

1. **Public smoke.** `ops.` (or `app.` if local DNS is flaky) `/` → login on the **same public host**, `/login` **200**? If yes, stop. 403 challenge page → Zone (not Lead).
2. **Triage the error class.**
   - **1033 / 530 / 502** and Doc asleep or cloudflared dead → lid-close / tunnel / Mac sleep (`api-stay-up.md` same class). Wake Doc (Amphetamine session if it should stay up).
   - **Process flap** (`next dev`, EADDRINUSE, repeated restart, `BUILD_ID` missing) → skip to step 4.
3. **Doc awake?** Local `GET http://127.0.0.1:3000/login` after wake. If it fails, Lead checks LaunchAgent `com.projectcar.shop-web` (KeepAlive) and `~/hermes-tools/mission-control/shop-web/run-shop-web.sh`. Confirm the process is **`next start`**.
4. **Lead — flap / stale build.** Boot out KeepAlive → `npm run build` in `apps/project-car/web` → kickstart → verify `.next/BUILD_ID`. Do not leave `next dev` in the LaunchAgent.
5. **Zone — edge.** Local `:3000` login OK but public **502** / **530 / 1033** / DNS miss → Zone checks host cloudflared + the `ops.` / `app.` hostname rules. Origin must be **`http://127.0.0.1:3000`**, not bare `localhost`. Lead does not edit Cloudflare. Do not cut the `app.` alias.
6. **Garage — after.** When public smoke is green, Garage may re-walk ops/app UI. No process restarts.

Host split: `STATUS.md`. API stay-up: `api-stay-up.md`. Brochure Worker: `brochure-worker-deploy.md`. Member-on-projectcar.ca: `member-host-cutover.md` (plan only — **Ben GO**, not shipped).

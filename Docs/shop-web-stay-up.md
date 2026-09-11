# Shop-web stay-up — `ops.projectcar.ca` / `app.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-11  
**Public URLs:** https://ops.projectcar.ca (LIVE management) · https://app.projectcar.ca (temporary alias)  
**Related:** `doc-lid-restore.md` (ordered wake — **not** a pull), `doc-unfreeze.md` (Ben GO pull), `api-stay-up.md` (api `/health` is **api-only** — companions live here), `doc-software-baseline.md`, `brochure-worker-deploy.md`, `STATUS.md` host split + Lookout Soft-530 companion watches, `shop-os-ci.md` (green CI ≠ unfreeze), `member-host-cutover.md` (plan only), `member-zone-edge.md` (Zone path-split; plan only), `app-alias-cut.md` (later `app.` cut; plan only), `mcking-shop-host-cutover.md` (future McKing host — plan only; **not** a cut), `apps/project-car/web/README.md`

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

**Future host (plan only):** shop-web later moves to **McKing Docker** with Cloudflare tunnel **hostname reuse** (`ops.` + temporary `app.` stay the public names). Dual-run Doc KeepAlive, then cut — paper: `mcking-shop-host-cutover.md`. **Not** Next #1. **Not** GO’d. Do **not** execute from this stay-up file. Today’s origin is still Doc.

---

## LOCKED: `next start`, not `next dev`

KeepAlive **must** run **`next start`**. That sets `NODE_ENV=production` and serves the built `.next` tree.

`next dev` on Doc was the **Schedule-outage root cause**. The dev server flaps: **EADDRINUSE**, KeepAlive restart loops, and Cloudflare **connection refused** on the tunnel. Do not “temporarily” point the LaunchAgent at `npm run dev` / `next dev`.

If you see `next dev` in `ps`, repeated LaunchAgent exits, or a missing `.next/BUILD_ID`, that is **process flap** — not lid-close. Fix by enforcing `next start` and the rebuild path below.

---

## Rebuild after web merges on Doc

**Frozen until Ben GO.** Doc checkout / shop-web BUILD stay at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**). **#36** and **#69** are **git-only**. Lid-restore / morning wake is **kickstart-if-down only** — do **not** `git pull` or `npm run build` to tip (`doc-lid-restore.md` **#72**). plan-improve / Chief / Lead must **not** treat a merge on `main` as license to pull.

A `git pull` on `main` does **not** update the running UI. `next start` serves the last **`npm run build`**. Do not leave a stale `.next` behind a new `main` pull — and do not pull while frozen.

**While Doc checkout is frozen** (`4cf8924` / `5swmVz-T2CqKEQzTk1ifU`), do **not** run this rebuild from lid-restore or from a green Shop OS CI check. **Ben GO** first; ordered pull + migrate + rebuild + smoke: [doc-unfreeze.md](doc-unfreeze.md). This section is the rebuild essay that unfreeze step 4 calls.

**After Ben GO** (only), Lead on Doc may pull + rebuild:

1. **Note the tip** you intend (`git rev-parse HEAD` in `~/src/Project-Car` after `git pull origin main`).
2. **Boot out** LaunchAgent `com.projectcar.shop-web` so nothing is bound to `:3000`.
3. **`npm run build`** in the Doc working tree (`apps/project-car/web`).
4. **Kickstart** KeepAlive `com.projectcar.shop-web` (wrapper → `next start`).
5. **Verify `.next/BUILD_ID`** matches the tip you intended. If `BUILD_ID` is missing or stale, you are still on the old build — do not call the merge live.

```bash
# ONLY after Ben GO — not on lid-restore, not while checkout is frozen
launchctl bootout gui/$(id -u)/com.projectcar.shop-web
cd ~/src/Project-Car/apps/project-car/web
npm run build
cat .next/BUILD_ID
launchctl kickstart -k gui/$(id -u)/com.projectcar.shop-web
# confirm next start (not next dev) and BUILD_ID still present
```

Last recorded shop-web **BUILD** on Doc (STATUS): Dashboard **#28** — checkout **frozen** at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`**. `main` tip is **`2dd61a2` / #74** (doc-unfreeze checklist on `main` — **not** a Doc unfreeze). Green **shop-os-ci** / lid-restore process-wake are **not** Ben GO. **#36** (`f952cd3`) and **#69** (`b9f9019`) stay **git-only**. Do **not** call them live on Doc. After **Ben GO**, ordered pull: [doc-unfreeze.md](doc-unfreeze.md). Update STATUS only after **Ben GO** + a new BUILD_ID ≠ `5swmVz`.

---

## Lid-close / sleep vs process flap

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel. Amphetamine + plugged-in no-sleep (`doc-software-baseline.md`) plus LaunchAgent KeepAlive once the host is awake are mitigation, not a guarantee. Ordered wake after lid-close: `doc-lid-restore.md`.

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

## Lookout Soft-530 companion watches (GO'd to arm)

**Blind spot:** Soft-530 five-row is Doc shop hosts `cloud.` / `api.` / `app.` / `ops.`, but Lookout Soft-530 coverage was **api-only** (`GET https://api.projectcar.ca/health`). `ops.` / `app.` (and `cloud.`) can **530 while `api.` stays 200** — same class as pre-vault-watch.

Lookout **GO'd to arm** companion flip watches 2026-09-11:

| Watch URL | Ok | Down |
|-----------|----|------|
| `https://ops.projectcar.ca/login` | **200** (or **307** → `/login` then **200**) | **502 / 530 / 1033 / timeout** |
| `https://app.projectcar.ca/login` | same | same |
| Optional `https://cloud.projectcar.ca/login` (five-row parity; Lead probed **200**) | same | same |

Cadence ≈ the api `/health` watch. Baselines (Lookout-owned): `/workspace/lookout/projectcar-ops-health-baseline.json` + `projectcar-app-health-baseline.json` (+ cloud if armed). Flip-only alerts: **Chief + Lead only**; **never Ben**; never restart / mutate.

**GO'd / arming** until Lookout confirms `enabled`. Do **not** claim companion watches `enabled:true` / LIVE/armed until that confirm. Soft-530 companion watches ≠ vault `/alive` watch ≠ Doc lid-restore. Soft-530 **CLEAR** live. Vault flip watch stays **LIVE/armed**. Api `/health` stay-up: `api-stay-up.md`. STATUS Live is canonical.

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lookout** | Soft-530 companion flip watches on `ops.` / `app.` `/login` (**GO'd to arm** 2026-09-11 — **GO'd / arming** until Lookout confirms `enabled`). Optional `cloud.` `/login` for five-row parity. | Process restore on Doc; Cloudflare tunnel / DNS edits; vault `/alive` watch (separate **LIVE/armed**); Doc lid-restore |
| **Lead** | shop-web process stay-up and recovery on Doc (`com.projectcar.shop-web`, wrapper, `next start`, rebuild / `BUILD_ID`) | Cloudflare tunnel / DNS edits |
| **Zone** | Cloudflare tunnel + DNS for `ops.projectcar.ca` and temporary `app.projectcar.ca` | Restarting shop-web |
| **Garage** | shop-web PRs under `apps/project-car/web` | Restarting shop-web, tunnel, or DNS |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, a login redirect to localhost, or a flapping UI. **Recovery of the process is Lead only.** Do not instruct Garage (or anyone else) to restart shop-web. Companion flip alerts: **Chief + Lead only**; **never Ben**; never restart / mutate.

---

## Recovery checklist

1. **Public smoke.** `ops.` (or `app.` if local DNS is flaky) `/` → login on the **same public host**, `/login` **200**? If yes, stop. 403 challenge page → Zone (not Lead).
2. **Triage the error class.**
   - **1033 / 530 / 502** and Doc asleep or cloudflared dead → lid-close / tunnel / Mac sleep (`api-stay-up.md` same class). Wake Doc (Amphetamine session if it should stay up).
   - **Process flap** (`next dev`, EADDRINUSE, repeated restart, `BUILD_ID` missing) → skip to step 4.
3. **Doc awake?** Local `GET http://127.0.0.1:3000/login` after wake. If it fails, Lead checks LaunchAgent `com.projectcar.shop-web` (KeepAlive) and `~/hermes-tools/mission-control/shop-web/run-shop-web.sh`. Confirm the process is **`next start`**.
4. **Lead — flap / down process.** While checkout is **frozen**: **kickstart-if-down only** (keep `next start` on the existing BUILD_ID). Do **not** `git pull` or rebuild to tip. After **Ben GO**, flap / stale-build recovery is bootout → `npm run build` → kickstart → verify `.next/BUILD_ID` ([doc-unfreeze.md](doc-unfreeze.md)). Do not leave `next dev` in the LaunchAgent.
5. **Zone — edge.** Local `:3000` login OK but public **502** / **530 / 1033** / DNS miss → Zone checks host cloudflared + the `ops.` / `app.` hostname rules. Origin must be **`http://127.0.0.1:3000`**, not bare `localhost`. Lead does not edit Cloudflare. Do not cut the `app.` alias.
6. **Garage — after.** When public smoke is green, Garage may re-walk ops/app UI. No process restarts.

Host split: `STATUS.md`. Ordered lid-close restore: `doc-lid-restore.md` (process wake only). After **Ben GO**, pull/rebuild: `doc-unfreeze.md`. API stay-up: `api-stay-up.md`. Brochure Worker: `brochure-worker-deploy.md`. Member-on-projectcar.ca: `member-host-cutover.md` (plan only — **Ben GO**, not shipped). Zone path-split: `member-zone-edge.md` (plan only — **Ben GO**). Temporary `app.` cut: `app-alias-cut.md` (plan only — STATUS Next #2; do **not** execute from stay-up). Future McKing host: `mcking-shop-host-cutover.md` (plan only — **not** Next #1, **not** GO; do **not** execute from stay-up). **`ops.` stays** the management host.

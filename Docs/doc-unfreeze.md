# Doc unfreeze — Ben GO pull checklist

**Status:** Living ops (Lead checklist)  
**Updated:** 2026-09-11  
**Related:** `doc-lid-restore.md` (process wake only — **not** this pull), `shop-web-stay-up.md` (rebuild essay), `api-stay-up.md`, `cors-origins.md`, `shop-os-ci.md` (git-only — **not** this GO), `STATUS.md`, `doc-software-baseline.md`

Ordered **Ben GO** pull/rebuild on Doc after the freeze at `4cf8924` / BUILD_ID `5swmVz-T2CqKEQzTk1ifU` (Dashboard **#28**). This file is the pull sequence. Lid-close wake stays in `doc-lid-restore.md` — do **not** copy that process essay here.

Merging this file is **not** a pull, **not** a rebuild, and **not** a substitute for Ben’s explicit GO.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, Cloudflare ↔ GitHub auth, or About P3-2 / P3-3.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Ben GO required** | Lead does **not** `git pull` or rebuild until Ben says **GO** to unfreeze — in words, not inferred from CI, a docs merge, lid-restore, or Soft-530 **CLEAR** / public `GET /health` **200**. |
| **Green Shop OS CI is not unfreeze GO** | A green `shop-os-ci` check on a later SHA is **expected** and means only that GitHub Actions passed pytest / typecheck / `next build`. It does **not** unfreeze Doc. Runbook: `shop-os-ci.md`. |
| **Lid-restore stays process-only** | Morning **530 / 1033** wake is `doc-lid-restore.md`: cloudflared → shop-api KeepAlive → shop-web **kickstart if down**. Wake must **not** auto-pull or rebuild. |
| **Soft-530 CLEAR / public GET /health 200 is not unfreeze GO** | Soft-530 **CLEAR** and public `GET /health` **200** mean Doc origin is up. That is **not** Ben GO to unfreeze. Same class as green `shop-os-ci` and lid-restore process-wake. |
| **This file is not the pull** | Do not execute from a docs PR. Garage / Zone do **not** pull Doc. |

---

## Why this is separate from lid-restore

| File | When | What |
|------|------|------|
| **`doc-lid-restore.md`** | Doc slept / lid-close / public **530 / 1033** | Wake processes. Same frozen checkout. **No** `git pull`. |
| **`doc-unfreeze.md` (this file)** | Ben said **GO** to unfreeze | Pull tip, migrate if needed, rebuild shop-web, new `BUILD_ID`, smoke **#36** / **#69** / banner honesty. |

Do **not** collapse them. A soft morning 530 is **not** unfreeze GO. Soft-530 **CLEAR** / public `GET /health` **200** is also **not** unfreeze GO.

---

## Reality today (do not claim this is done)

| Clock | Pin | Meaning |
|-------|-----|---------|
| **Git `main`** | Moves with merges (this repo) | **#36** host allowlist (`f952cd3`) and **#69** ops layout (`b9f9019`) are **on git**. Shop OS CI (`#73`) is git-only. |
| **Doc working tree** | Frozen at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) | Live `ops.` / `app.` / `:3000` stay on that build until this checklist finishes **after** Ben GO. |
| **Held #70** | Open docs / honesty PR | Optional tip fold + OwnerDemoBanner honesty copy. **Do not amend #70 from this file.** Merge of #70 is a separate lane — not this checklist. |

Do **not** call **#36** or **#69** live on Doc until step 5 shows a **new** `BUILD_ID` and step 6 / 7 smoke.

---

## Ownership (this run)

| Role | Owns | Does not own |
|------|------|----------------|
| **Ben** | Explicit **GO** to unfreeze | Executing `git pull` / rebuild |
| **Lead** | After GO: pull, alembic if needed, shop-web rebuild, `BUILD_ID` check, smoke | Cloudflare tunnel / DNS, Worker upload, Member cutover, `app.` cut |
| **Garage** | Brochure / waitlist e2e **after** public health is 200 | Doc `git pull`, alembic, shop-web rebuild |
| **Zone** | Tunnel / DNS only if local origin is healthy but public is still **1033** | Doc checkout |
| **Lookout** | Live probes (when enabled) | Doc pull. Morning probe is **Lead** while `projectcar-api-health-watch` is paused. |
| **Chief** | Standing GO for this **checklist**. Plan-improve. | Substituting for Ben’s unfreeze GO. uvicorn / shop-web restarts. |

No edge flip. No CF ↔ GitHub re-ask. No Member GO. No `app.` cut. No OAuth implementation. No tip-only finance stamps.

---

## Ordered pull (after Ben GO only)

Run these **in order**. Stop if Ben has not said GO.

### 1. Confirm Ben GO to unfreeze

Ben must say **GO** to unfreeze Doc (explicit). Record who / when in the heartbeat if that is the house style.

**Not GO:**

- Green Shop OS CI on `main` or on a PR
- Soft-530 **CLEAR** / public `GET /health` **200**
- Merge of this file, `#73`, `#72`, `#71`, or held `#70`
- Lid-restore / morning 530 recovery
- Chief standing GO for tests / CI / this checklist

If there is no explicit Ben GO, stop. Leave checkout frozen. Use `doc-lid-restore.md` if the public hosts are 530 / 1033.

### 2. `git pull` on the Doc checkout

Working tree on Doc is **`~/src/Project-Car`** (`shop-web-stay-up.md` / `api-stay-up.md`). If that path is missing, use the documented Doc clone — do **not** invent a second tree.

```bash
# on Doc
cd ~/src/Project-Car
git fetch origin main
git checkout main
git pull origin main
git rev-parse HEAD
```

Note the tip you actually landed on. That is the SHA you intend to build. Do **not** pull a random feature branch. Do **not** amend held **#70** from Doc.

Garage and Zone do **not** run this step.

### 3. Alembic / migrate if needed (shop-api)

Shop data is dedicated Postgres 16 — never Nextcloud MariaDB. From `apps/project-car/api`:

```bash
# on Doc, shop-api venv
cd ~/src/Project-Car/apps/project-car/api
source .venv/bin/activate   # or the Doc venv you already use
alembic current
alembic heads
```

| Result | Action |
|--------|--------|
| `current` **equals** `heads` | **Skip** migrate. Dashboard **#28** already shipped `20260906_0007` (todos / parts POs / calendar scaffold). **#36** / **#69** are shop-web only. |
| `current` **behind** `heads` | `alembic upgrade head`. Then Lead restarts LaunchAgent `com.projectcar.shop-api` so uvicorn loads the new schema. Local then public `GET /health` → **200**. |

Do **not** `alembic downgrade`. Do **not** re-seed unless Ben asked. Do **not** hand the restart to Garage or Zone. Essay: `api-stay-up.md`.

### 4. shop-web rebuild (`next start`, not `next dev`)

A `git pull` does **not** update the running UI. `next start` serves the last `npm run build`. Rebuild essay: `shop-web-stay-up.md`.

On Doc, after the intended tip is in `~/src/Project-Car`:

1. **Boot out** LaunchAgent `com.projectcar.shop-web` so nothing is bound to `:3000`.
2. **`npm run build`** in `apps/project-car/web`.
3. **Kickstart** KeepAlive `com.projectcar.shop-web` (wrapper → **`next start`**).
4. Confirm `ps` shows **`next start`**, not `next dev`.

```bash
# on Doc — same sequence as shop-web-stay-up.md
launchctl bootout gui/$(id -u)/com.projectcar.shop-web
cd ~/src/Project-Car/apps/project-car/web
npm run build
cat .next/BUILD_ID
launchctl kickstart -k gui/$(id -u)/com.projectcar.shop-web
```

Do **not** point KeepAlive at `npm run dev` / `next dev`. That was the Schedule-outage root cause.

### 5. Verify new `BUILD_ID` ≠ frozen Dashboard #28

```bash
# on Doc
cat ~/src/Project-Car/apps/project-car/web/.next/BUILD_ID
```

| Check | Expect |
|-------|--------|
| `.next/BUILD_ID` present | Non-empty |
| Value | **Not** `5swmVz-T2CqKEQzTk1ifU` (frozen Dashboard **#28** id) |

If `BUILD_ID` is missing, equals `5swmVz-T2CqKEQzTk1ifU`, or you skipped rebuild, you are still on the frozen build. **Do not** call **#36** / **#69** live. Rebuild again.

Update `STATUS.md` when Lead ships the new id (separate docs pass — not this file’s job to invent a future id).

### 6. Product smoke — #36 + #69 + banner honesty

Walk **`https://ops.projectcar.ca`** (or **`https://app.projectcar.ca`** if `ops.` DNS is flaky). Still the Doc demo. The shop is not open.

| Slice | Expect after this pull |
|-------|------------------------|
| **#36 host allowlist** | `GET /` on `ops.` → `Location: https://ops.projectcar.ca/login` (no `localhost`). Same-host hop on the temporary `app.` alias. Allowlist in `apps/project-car/web/lib/request-origin.ts`: localhost / `127.0.0.1`, `ops.`, `app.`, `projectcar.ca`, `www.` — **never** `api.`. Junk `X-Forwarded-Host` must not mint a random origin. |
| **#69 ops layout** | Owner chrome: primary nav **Dashboard / Schedule / Chat / Members**; secondary **Inventory** (Parts/Tools), **Floor** (Jobs/Cameras/Hoists), **Admin** (Payments/Tiers/Fill/Waitlist); compact dismissible demo banner. Dashboard: **3** primary metrics (booked hours / open to-dos / open POs) + **3×2** bay grid + Parts / To-dos split. |
| **OwnerDemoBanner honesty** | Banner (and login lede if present on that tip) must treat **`ops.projectcar.ca` as LIVE** and **`app.` as the temporary alias**. Fail if copy still says **“naming only, no DNS yet.”** Honesty wording may still be on held **#70** — do **not** amend #70 from this checklist; if the pulled tip still has naming-only copy, record the gap and leave the rewrite to that lane. |

Do **not** claim #36 / #69 live from git SHA alone. `BUILD_ID` + this walk are the proof.

### 7. Public smoke — health + waitlist CORS

Same class as lid-restore smoke, plus CORS. Public probes mean nothing if Doc is asleep — wake first (`doc-lid-restore.md`), then re-run.

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** `{"status":"ok","service":"project-car-api"}` |
| `GET https://ops.projectcar.ca/login` | **200** (or `app.` `/login` if `ops.` DNS is flaky) |
| `GET https://app.projectcar.ca/login` | **200** — alias **still live**; do not cut it |
| Waitlist OPTIONS CORS | `Access-Control-Allow-Origin: https://projectcar.ca` — `cors-origins.md` |

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
curl -sS -o /dev/null -w '%{http_code}\n' https://app.projectcar.ca/login
curl -sS -D - -o /dev/null -X OPTIONS https://api.projectcar.ca/waitlist \
  -H 'Origin: https://projectcar.ca' \
  -H 'Access-Control-Request-Method: POST'
```

Garage may re-run brochure waitlist e2e **after** health is 200. Form only. No process restarts.

---

## After a successful unfreeze

- Doc checkout and `.next/BUILD_ID` match the tip you intended.
- **#36** and **#69** may be called **LIVE on Doc** only after steps 5–7.
- Lid-restore **stays** process-only. A later morning 530 is still wake-only — do **not** pull again unless Ben GOs another unfreeze.
- Shop OS CI remains git-only. Green CI on a *later* SHA is still **not** a new unfreeze GO.
- Soft-530 **CLEAR** / public `GET /health` **200** is still **not** a new unfreeze GO.

---

## Do not

- Treat green `shop-os-ci` as Ben GO
- Treat Soft-530 **CLEAR** / public `GET /health` **200** as Ben GO
- Auto-`git pull` or rebuild from lid-restore / morning 530
- Run this checklist without explicit Ben GO
- Hand Doc pull / alembic / `npm run build` to Garage or Zone
- Serve shop-web with `next dev` on KeepAlive
- Call a `main` pull live while `BUILD_ID` is still `5swmVz-T2CqKEQzTk1ifU`
- Amend held **#70** from this file (optional tip fold is a follow-up on that PR)
- Implement Google Calendar OAuth, Member host cutover, `app.` alias cut, or Mission Control cockpit
- Flip edge / path-split, re-ask Cloudflare ↔ GitHub, or start About P3-2 / P3-3
- Invent a shop opening, Stripe, or Lookout GET-allow nag

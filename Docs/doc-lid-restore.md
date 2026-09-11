# Doc lid-close restore — ordered wake sequence

**Status:** Living ops (Lead checklist)  
**Updated:** 2026-09-11  
**Related:** `doc-unfreeze.md` (Ben GO pull — **not** this file; Soft-530 **CLEAR** Friday ≠ this GO), `api-stay-up.md` (weekend `/health` flip → this file), `shop-web-stay-up.md`, `doc-software-baseline.md`, `cors-origins.md`, `STATUS.md` (weekend Soft-530 coverage), `shop-os-ci.md` (green CI ≠ unfreeze)

Single **ordered** wake/restore after Doc lid-close / sleep (the morning **530 / 1033** pattern). Plan/ops checklist for **Lead**. This file is the sequence. Process essays stay in the Related docs — do not copy them here.

Do **not** invent an edge flip, a Cloudflare ↔ GitHub re-ask, or a Member **GO**. Soft 530 mornings are expected lid-close.

**Doc checkout is frozen** at `4cf8924` / BUILD_ID `5swmVz-T2CqKEQzTk1ifU` (Dashboard **#28**) until **Ben GO**. Lid-restore is process wake only — **not** a license to `git pull` or rebuild to tip. That would flip **#36** / **#69** live on Doc. After Ben GO, the ordered pull is [doc-unfreeze.md](doc-unfreeze.md). Green Shop OS CI is **not** that GO.

---

## Why this exists

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel. Public tunneled hosts then return Cloudflare **502** or **530 / error 1033**.

Amphetamine + plugged-in no-sleep (`doc-software-baseline.md`) plus LaunchAgent KeepAlive once the host is awake are **mitigation, not a guarantee**. If the lid is closed, public API / ops / app are down until Doc is awake.

The public brochure (Worker `projectcar-brochure`) does **not** go down when Doc sleeps. Waitlist still needs the API.

**Vault is OUT of this file.** `vault.projectcar.ca` is McKing-only LIVE (`cloudflared` → `localhost:8222`). Soft-530 lid-restore / LaunchAgent KeepAlive must **not** recreate `vault.` ingress on Doc. Vault watch ≠ this sequence.

---

## Soft 530 mornings vs ping Ben

| Pattern | Action |
|---------|--------|
| Soft morning **530 / 1033** on `api.` / `ops.` / `app.` | **Expected lid-close.** Stay quiet. Restore when Doc is reachable. Do not page Ben. |
| Doc will not wake, **Grok Bot desktop offline**, or a **prolonged** outage after a normal wake window | Ping **Ben**. Lead still owns process restore once the Mac is up. |

Alerts can come from anyone who sees **502**, **530 / error 1033**, or a failed waitlist submit. **Recovery of the processes is Lead only.** Lookout `projectcar-api-health-watch` is **resumed** (`enabled:true`). **#78 lookout-resume** is **LIVE-SUPERSEDED**. Soft-530 companion watches stay **HOLD**.

---

## Weekend Soft-530 coverage (plan-improve off Sat/Sun)

plan-improve is **off Sat/Sun**. Soft-530 companion ops/app watches stay **HOLD / not armed** (do **not** re-ask). Weekend flip coverage = Lookout `api.` `/health` + vault `/alive` **only**.

| Lock | Meaning |
|------|---------|
| **Weekend control plane** | This file: Doc KeepAlive / lid-close (`com.projectcar.cloudflared` + uvicorn `:8000` + `next start` `:3000` LaunchAgents). **Not** `doc-unfreeze.md`. **Not** **#82**. |
| **`api.` `/health` flips non-200** | Chief/Lead run **this** ordered restore — **process wake only**. No pull while freeze `4cf8924` / `5swmVz` is intact. |
| **Vault flips** | Stay on the **separate** McKing vault watch. Vault is **OUT** of this file (below). |
| **No weekend Zone / Worker** | Do **not** schedule weekend Zone Direct Upload / Worker work. First Monday plan-improve resumes Soft-530 smoke. |
| **Anti-goal** | Soft-530 **CLEAR** Friday ≠ unfreeze GO ≠ companion re-ask. |

**#82** Ben GO / Soft-530 companions HOLD / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / waitlist-owner-desk **retired** (Owner desk LIVE; optional CSV Later) / **#79.1** git-only until Doc unfreeze — **unchanged**. Essays: `api-stay-up.md`, `shop-web-stay-up.md`. STATUS Live / Locks is canonical.

---

## Ownership (this run)

| Role | Owns | Does not own |
|------|------|----------------|
| **Lead** | Restore processes on Doc (cloudflared up, shop-api KeepAlive, shop-web `next start` **kickstart only if the process is down**) | Cloudflare tunnel / DNS edits, edge flip, Member GO, **`git pull` / rebuild to tip** while checkout is frozen |
| **Zone** | Only if **local origin is healthy** but public is still **1033** (tunnel / DNS) | Restarting uvicorn or shop-web |
| **Garage** | Brochure waitlist e2e **after** public health is 200 | Restarting processes, tunnel, or DNS |

**Chief / plan-improve** must not treat lid-restore as license to pull tip. Weekend `/health` flip is still this process-wake sequence — plan-improve being **off Sat/Sun** does not invent an unfreeze. Pull/rebuild stays **Ben GO** — checklist: [doc-unfreeze.md](doc-unfreeze.md).

No edge flip. No CF ↔ GitHub re-ask. No Member GO.

---

## Ordered restore

Run these **in order**. Public probes mean nothing until cloudflared is up.

### 1. cloudflared up

Host **cloudflared** must be running on Doc before any public `api.` / `ops.` / `app.` probe means anything. Zone owns the hostname / DNS rules; Lead confirms the process is up on Doc.

If cloudflared is down after wake, start it on Doc. Do not treat a public 1033 as “restart uvicorn” until this step is done.

### 2. shop-api KeepAlive

LaunchAgent **`com.projectcar.shop-api`** → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. **Lead owns.**

1. Local: `GET http://127.0.0.1:8000/health` → **200** `{"status":"ok","service":"project-car-api"}`
2. Public: `GET https://api.projectcar.ca/health` → **200** (same body)

Essay: `api-stay-up.md`. Do not hand the restart to Garage or Zone.

### 3. shop-web

LaunchAgent **`com.projectcar.shop-web`** → **`next start`** `:3000`. **Not** `next dev`. **Lead owns.**

Doc checkout is **frozen** at `4cf8924` / BUILD_ID `5swmVz-T2CqKEQzTk1ifU` (Dashboard **#28**). Lid-restore must **not** auto-`git pull` or rebuild to tip — that would accidentally flip **#36** (host allowlist) and **#69** (ops layout) live on Doc.

**Kickstart only if the process is down** (existing `next start` KeepAlive path). Do **not** `git pull origin main` or `npm run build` on wake.

**Pull/rebuild remains Ben GO.** After that GO, the ordered pull is [doc-unfreeze.md](doc-unfreeze.md) (rebuild essay: `shop-web-stay-up.md`). Until then, do **not** claim **#36** or **#69** is live on Doc.

Must be **`next start`**, not `next dev`.

### 4. Smoke

When steps 1–3 are up:

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** |
| ops/app `/login` | **200** — `https://ops.projectcar.ca/login`, or `https://app.projectcar.ca/login` if `ops.` DNS is flaky |
| Waitlist OPTIONS CORS | Only when health is **200** — `cors-origins.md` |

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
# if ops. DNS is flaky on this client:
curl -sS -o /dev/null -w '%{http_code}\n' https://app.projectcar.ca/login
```

Garage may re-run brochure waitlist e2e **after** health is 200. Form only.

---

## Do not

- Treat a soft morning 530 as a product break or a reason to ping Ben
- Flip edge / path-split (`member-zone-edge.md`)
- Re-ask Cloudflare ↔ GitHub auth (`brochure-pages-cutover.md`)
- Take Member **GO** (`member-host-cutover.md`)
- Cut the `app.` alias
- Instruct Garage or Zone to restart uvicorn / shop-web
- Auto-`git pull` or rebuild shop-web on wake while Doc checkout is frozen (`4cf8924` / `5swmVz-T2CqKEQzTk1ifU`)
- Treat lid-restore as Chief / plan-improve / Lead license to pull tip
- Call a `main` pull live without a new `.next/BUILD_ID`
- Treat green Shop OS CI as unfreeze GO (`doc-unfreeze.md`)
- Treat Soft-530 **CLEAR** Friday as unfreeze GO or a companion re-ask
- Schedule weekend Zone Direct Upload / Worker / **#82** work (first Monday plan-improve resumes Soft-530 smoke)
- Recreate `vault.` ingress on Doc / fold vault into Doc KeepAlive (`vault.projectcar.ca` is McKing-only; vault watch ≠ Soft-530)

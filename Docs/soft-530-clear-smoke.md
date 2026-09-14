# Soft-530 CLEAR recovery smoke (after extended OPEN)

**Status:** Paper — first recovery smoke, **not** a GO  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops while OPEN **~24h+** — this file is the **next** Soft-530 CLEAR card), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — ordered Ben GO menu, **never auto-fire**; **#79.1** acceptance is **later**), [doc-lid-restore.md](doc-lid-restore.md) (process wake + Doc forensics `@55e10d0`), [dual-host-outage.md](dual-host-outage.md) (wake order — Doc first, then McKing), [cors-origins.md](cors-origins.md) (waitlist OPTIONS Origin), [ops-demo-hardening.md](ops-demo-hardening.md) (**#79** / **#79.1** — **after** this smoke), [doc-unfreeze.md](doc-unfreeze.md) (Ben GO pull — **after** this smoke), [vault-stay-up.md](vault-stay-up.md) (vault wake + McKing forensics `@d88cacb`), [vault-clear-smoke.md](vault-clear-smoke.md) (vault CLEAR recovery smoke — **separate** McKing lane; **not** this file)

After Soft-530 **CLEAR** following **extended OPEN** (**>~24h**), run this **first recovery smoke BEFORE** any Owner desk / **#79.1** / unfreeze talk. Quiet-ops named the lock ([soft-530-extended-open.md](soft-530-extended-open.md)). This file names the first public proof that the **route** is back — not only that the tunnel answered.

This fold executes **none** of the curls. Do **not** invent Soft-530 CLEAR, vault CLEAR, **#82**, unfreeze, Zone Direct Upload, Garage strip-changeme, a companion re-ask, or Bitwarden from this paper.

---

## When this card applies

All three — then this smoke, **not** the GO menu.

| Gate | Living stamp / meaning |
|------|------------------------|
| **Prior OPEN was extended** | Soft-530 **OPEN ~24h+** — CF **1033** since 2026-09-13 **~11:57** America/Edmonton (`api.` / `app.` / `ops.` / `cloud.` + waitlist OPTIONS). Quiet-ops: [soft-530-extended-open.md](soft-530-extended-open.md). |
| **A live Soft-530 CLEAR just happened** | Doc lid-restore process wake ran ([doc-lid-restore.md](doc-lid-restore.md)). Wake order stays [dual-host-outage.md](dual-host-outage.md) — **Doc first**. |
| **Before desk / #79.1 / unfreeze talk** | Owner desk existence, Garage **#79.1**, and [doc-unfreeze.md](doc-unfreeze.md) wait. This smoke is **first**. The **#79.1** acceptance card is [post-dual-clear-go.md](post-dual-clear-go.md) — **later**, after Ben GO. |

Living this fold: Soft-530 is still **OPEN** (CF **1033** since 2026-09-13 ~11:57). Vault is independently **OPEN** (**502** since ~19:45 MT Sep 13 — **not** 1033). ListMachines **Mac.lan only**. This paper does **not** invent CLEAR.

**CLEAR path is still** [post-dual-clear-go.md](post-dual-clear-go.md). After a **live** Soft-530 CLEAR **and** a **live** vault CLEAR **and** both forensic papers (`55e10d0` / `d88cacb`), Ben’s GO menu is **ordered** and **never auto-fire**. This smoke does **not** skip KeepAlive, does **not** auto-GO **#82**, and does **not** unfreeze.

---

## First recovery smoke (five — before desk / #79.1 / unfreeze)

Run **in order**. `/health` **200** alone is tunnel-up, not route-alive.

| # | Assert | Expect |
|---|--------|--------|
| **1** | `GET https://api.projectcar.ca/health` | **200** |
| **2** | Waitlist `OPTIONS` | **200** with `Access-Control-Allow-Origin` for Origin `https://projectcar.ca` **and** `https://www.projectcar.ca` ([cors-origins.md](cors-origins.md)) |
| **3** | Waitlist `POST` | Validation **422** **or** success **201** — prove the **route** is alive, not just tunnel-up. Prefer **422** (empty name + bad email) so the smoke does **not** mint a live signup. **201** also counts if a real form already succeeded. |
| **4** | `app.` + `ops.` | May still **307** → `/login` with body print `` `changeme` ``. That is **freeze** (`4cf8924` / BUILD_ID **`5swmVz`**), **not** Soft-530. Do **not** treat `changeme` as “still 1033.” Do **not** treat login-up as unfreeze / **#79.1** talk. |
| **5** | `cloud.` `status.php` | **200** **when Doc public is up**. Five-row shop host. **Not** a McKing `cloud.*` leave. |

```bash
# ONLY after a live Soft-530 CLEAR following extended OPEN — not this paper
# before Owner desk / #79.1 / unfreeze talk
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
# expect 200

curl -sS -D - -o /dev/null -X OPTIONS https://api.projectcar.ca/waitlist \
  -H 'Origin: https://projectcar.ca' \
  -H 'Access-Control-Request-Method: POST'
# expect 200 + Access-Control-Allow-Origin: https://projectcar.ca

curl -sS -D - -o /dev/null -X OPTIONS https://api.projectcar.ca/waitlist \
  -H 'Origin: https://www.projectcar.ca' \
  -H 'Access-Control-Request-Method: POST'
# expect 200 + Access-Control-Allow-Origin: https://www.projectcar.ca

# prefer 422 — prove route; do not mint a live signup
curl -sS -o /dev/null -w '%{http_code}\n' \
  -X POST https://api.projectcar.ca/waitlist \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://projectcar.ca' \
  -d '{"name":"","email":"not-an-email"}'
# expect 422 (validation). 201 also proves the route if a real form already succeeded.

# note only — freeze state, NOT Soft-530
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
curl -sS -o /dev/null -w '%{http_code}\n' https://app.projectcar.ca/login
# 307 → /login then 200 + body may still print `changeme` — freeze 4cf8924 / 5swmVz

# when Doc public NC is up
curl -sS -o /dev/null -w '%{http_code}\n' https://cloud.projectcar.ca/status.php
# expect 200
```

After this smoke passes, stamp Doc forensics on [doc-lid-restore.md](doc-lid-restore.md) (lastExit / KeepAlive / caffeinate·CDM / Tailscale) before walking away. Vault CLEAR first card is [vault-clear-smoke.md](vault-clear-smoke.md); McKing forensics stay [vault-stay-up.md](vault-stay-up.md). Then — and only then — the ordered Ben GO menu is [post-dual-clear-go.md](post-dual-clear-go.md). **Never auto-fire.**

---

## Not the #79.1 acceptance smoke

| Card | When | What |
|------|------|------|
| **This file** | First thing after extended-OPEN Soft-530 **CLEAR** | Route-alive: `/health` + OPTIONS CORS + POST 422/201. `changeme` on `/login` is **expected freeze**. |
| **#79.1 acceptance** | After Ben GO unfreeze + pull + Garage **#79.1** rebuild | Public `/login` **no longer** prints `` `changeme` ``; tip / `BUILD_ID` ≠ `4cf8924` / `5swmVz`. [post-dual-clear-go.md](post-dual-clear-go.md) Shop OS card. |

Soft-530 **CLEAR** alone ≠ the **#79.1** card. This smoke **before** that talk is the point.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **CLEAR smoke ≠ #82 GO** | **#82** is still Ben GO after dual CLEAR ([post-dual-clear-go.md](post-dual-clear-go.md)). This smoke does **not** upload, purge, or reconcile Reality. |
| **CLEAR smoke ≠ companion re-ask** | Soft-530 companions stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. |
| **CLEAR smoke ≠ Bitwarden** | Import/rotate is vault. Vault CLEAR is still the **separate** McKing lane ([vault-stay-up.md](vault-stay-up.md)). Soft-530 green does **not** lift Bitwarden. |
| **Soft-530 CLEAR alone ≠ unfreeze** | Freeze `4cf8924` / **`5swmVz`** until **Ben GO**. `changeme` on `/login` is freeze, not a 1033. |
| **Vault CLEAR still separate** | McKing first card is [vault-clear-smoke.md](vault-clear-smoke.md) (`/alive` **200** + `/api/config` McKing **2026.6.0** class + **502→200**). Forensics stay [vault-stay-up.md](vault-stay-up.md). This file is Doc Soft-530 only. Green `/health` ≠ vault CLEAR. |
| **`/health` 200 ≠ route alive** | Tunnel-up without OPTIONS CORS + POST 422/201 is **not** this card. |
| **Invent CLEAR** | Soft-530 still **OPEN** (CF **1033**). Vault still **OPEN** (**502**). Only `Mac.lan`. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / **#79.1** acceptance (`1cd73c7`) / quiet-ops (`1e6a0b1`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Run this smoke, desk, **#79.1**, or unfreeze from this paper while Soft-530 is still **OPEN**
- Treat `/health` **200** alone as this card (need OPTIONS CORS + POST 422/201)
- Treat `app.`/`ops.` **307**→`/login` + print `` `changeme` `` as Soft-530 still down — that is freeze
- Start Owner desk / **#79.1** / unfreeze talk from this smoke
- Treat this smoke as **#82** GO, companion re-ask, or Bitwarden
- Treat Soft-530 CLEAR alone as unfreeze
- Fold vault CLEAR into this Doc smoke — vault first card is [vault-clear-smoke.md](vault-clear-smoke.md)
- Auto-fire [post-dual-clear-go.md](post-dual-clear-go.md)
- Shell `Mac.lan` as Doc or McKing
- Execute Zone / Garage / Lookout arm from this paper

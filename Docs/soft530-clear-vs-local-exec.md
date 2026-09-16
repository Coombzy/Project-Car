# Soft-530 CLEAR ≠ ListMachines present

**Status:** Paper — class split + half-ops HOLD, **not** a GO  
**Updated:** 2026-09-16 ~07:51 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **CLEAR ~26m** since **~07:25** + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY** + this pointer), [soft-530-blip-recover.md](soft-530-blip-recover.md) (short OPEN blip **~07:06–~07:25** then CLEAR — **no camp GO mid-flap**; this file extends that recover into **steady-state**), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (**`soft530_clear_since` ~07:25** + **`soft530_open_blip` ~07:06–~07:25** + EMPTY **stays EMPTY** — do **not** flip Soft-530=OPEN), [post-dual-clear-go.md](post-dual-clear-go.md) (camp vault-on-Doc GO = Soft-530 **CLEAR ≥30m SAME-CLASS AND** Docs **CONNECTED+Shellable** — CLEAR alone while EMPTY = **half-ops HOLD**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (full smoke **after** Shellable — Lead public `/health` **200** + `app.`/`ops.` **307** is Soft-530 class only), [shared-fleet-cards.md](shared-fleet-cards.md) (Chief Shared amend **queued** until Shellable), [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) (**CONNECTED ≠ Shellable ≠ tunnel healthy**), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (camp still **Ben GO**), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (home-awake half-ops ≠ camp GO), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Soft-530 class and local-exec class are **two stamps**. ListMachines **EMPTY** does **not** make Soft-530 **OPEN**. Soft-530 **CLEAR** while EMPTY does **not** make camp GO / dual CLEAR / **#82** / unfreeze.

This fold executes **none** of the Shells, curls, hops, or GOs. Do **not** invent vault CLEAR, dual CLEAR, **#82**, unfreeze, **#79.1**, camp Zone, Bitwarden, a Shared amend, or a freeze re-verify from this paper.

---

## Split classes

| Class | What it is | What it is not |
|-------|------------|----------------|
| **Soft-530** | Public HTTP only: `api.` `/health`, `app.` / `ops.` (and waitlist OPTIONS/POST when scored). Lookout watches **this** class. | ListMachines presence. Shellable. KeepAlive. lid-restore. Shared amend. Freeze git verify. |
| **Local-exec** | ListMachines + **CONNECTED+Shellable**. Shared amend, freeze re-verify, KeepAlive assert, lid-restore, full [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on-host. | Soft-530 OPEN/CLEAR. Vault class. Option A / **#82**. |

**Lookout** watches public Soft-530 (+ vault `/alive`). **Chief** Shared amend / freeze re-verify stay **queued** until Docs is **CONNECTED+Shellable**. Do **not** ask Lookout to prove local-exec. Do **not** stamp Soft-530 from ListMachines.

---

## Living proof (~07:25–~07:51 America/Edmonton)

| Field | Living |
|-------|--------|
| **Soft-530** | **CLEAR** ~**26m** — Lead `api.` `/health` **200** ok; `app.` + `ops.` **307**. **`soft530_clear_since` ~07:25**. Do **not** stamp **OPEN** because EMPTY. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). Recovered. Essay: [soft-530-blip-recover.md](soft-530-blip-recover.md). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined HTTP** | Soft-530 **CLEAR** + vault **OPEN** = **half-state**. **≠ dual CLEAR.** |
| **ListMachines** | **EMPTY** (Lead confirm). Local-exec **ABSENT**. **CONNECTED ≠ Shellable ≠ tunnel healthy.** |
| **Combined ops** | Soft-530 **CLEAR** + local-exec **EMPTY** = **half-ops HOLD**. |
| **Option A** | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Shared** | **`shared_fleet_card_stale=true`**. CLEAR-since-**~07:25** amend still **Chief** after ≥30m SAME-CLASS dwell **+** Shellable. OPEN-since-**~07:06** queue **cancelled**. |
| **Freeze** | **`last_known`** `` `4cf8924` `` / **`5swmVz`**. Behind **intact**. Re-verify **queued** until Shellable. **Never auto-pull.** |

Receipt: [overnight_2026-09-16_0751_clear_vs_local_exec_verify.md](overnight_2026-09-16_0751_clear_vs_local_exec_verify.md). The ~07:25 recover receipt stays [overnight_2026-09-16_0725_blip_recover_verify.md](overnight_2026-09-16_0725_blip_recover_verify.md) — **same Soft-530 class**, now aged ~26m while EMPTY.

---

## Camp vault-on-Doc Ben GO gate (extends blip-recover into steady-state)

Lead **may re-offer** camp vault-on-Doc **Ben GO** only when **both** are true. This paper does **not** offer it.

| # | Gate | Living this fold (~07:51) |
|---|------|---------------------------|
| **1** | Soft-530 **CLEAR ≥30m SAME-CLASS** (still CLEAR; same **`soft530_clear_since` ~07:25**; vault still **OPEN 1033**; no new OPEN flap) | **~26m** — dwell **not** yet ≥30m |
| **2** | Docs `95a229f5` **CONNECTED+Shellable** + [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on that host | **EMPTY** — fail |

**CLEAR alone while EMPTY = half-ops HOLD.** Extends [soft-530-blip-recover.md](soft-530-blip-recover.md) (`5221d90`) past the recover instant into **steady-state**: the GO window stays **paused** for as long as local-exec is EMPTY, even after the Soft-530 dwell later crosses 30m.

Until both gates, stay quiet on camp. **Ben GO** each later step; **never auto**.

---

## Who watches what

| Actor | Watches | Queued until Shellable |
|-------|---------|------------------------|
| **Lookout** | Public Soft-530 (`api.` `/health`) + vault `/alive` | — |
| **Lead** | Public Soft-530 / vault HTTP class; ListMachines identity | Full clear-smoke, lid-restore, KeepAlive assert |
| **Chief** | Stamp / Shared standing notes | Shared living-host amend **CLEAR since ~07:25** (blip noted); freeze re-verify from `/Users/dochak/src/Project-Car` |

Lookout **CLEAR** while ListMachines **EMPTY** is **expected half-ops**, not a Soft-530 relapse.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **EMPTY ≠ Soft-530 OPEN** | Soft-530 is public HTTP. EMPTY is local-exec **ABSENT**. Living **~07:25–~07:51** is the proof. |
| **CLEAR + EMPTY ≠ dual CLEAR** | Vault still **OPEN 1033**. Local-exec still **ABSENT**. Combined HTTP is **half-state**. Combined ops is **half-ops HOLD**. |
| **CLEAR + EMPTY ≠ camp GO** | Gate is ≥30m SAME-CLASS **AND** **CONNECTED+Shellable**. |
| **CLEAR + EMPTY ≠ #82 / unfreeze / Bitwarden / #79.1** | Each is a **separate Ben GO**. |
| **Never fan-out Garage / Zone on half-ops** | Brochure Home still **STALE** until **#82**. This paper is **not** an upload. |
| **Lead `/health` 200 + 307 ≠ clear-smoke** | Full smoke waits on **CONNECTED+Shellable**. |
| **≠ Shared / freeze write while EMPTY** | Chief stays **queued**. Docs/#70 is SSOT. |

**#82** Ben GO / companions **HOLD** / freeze `4cf8924` / `5swmVz` / vault subclass 502 vs 1033 — **unchanged**. This file executes **none** of those.

---

## Do not

- Stamp Soft-530=**OPEN** because ListMachines is **EMPTY**
- Collapse Soft-530 class into local-exec class (or the reverse)
- Reopen [post-dual-clear-go.md](post-dual-clear-go.md) / camp vault-on-Doc GO from CLEAR+EMPTY
- Score CLEAR+EMPTY as dual CLEAR / camp GO / **#82** / unfreeze / Bitwarden
- Amend Shared or re-verify freeze while EMPTY / **CONNECTED≠Shellable**
- Ask Lookout to prove Shellable / KeepAlive / lid-restore
- Fan-out Garage / Zone from half-ops
- Auto-fire camp / **#82** / **#79.1** / unfreeze / Bitwarden
- Invent vault CLEAR, or treat vault **OPEN 1033** as unexpected
- Auto-pull because freeze is behind
- Re-nag Ben (quiet)
- Treat `Mac.lan` as Doc

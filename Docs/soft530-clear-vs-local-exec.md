# Soft-530 CLEAR ≠ ListMachines present

**Status:** Paper — class split + half-ops HOLD, **not** a GO  
**Updated:** 2026-09-16 ~08:49 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **OPEN** **`soft530_open_since` ~08:41** after CLEAR dwell **~07:25–~08:41** ended + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY** + this pointer), [freeze-build-id-public-probe.md](freeze-build-id-public-probe.md) (public `"b"` scrape is Soft-530 class — **unreachable while OPEN**), [soft-530-blip-recover.md](soft-530-blip-recover.md) (short OPEN blip **~07:06–~07:25** then CLEAR — **no camp GO mid-flap**; this file’s split still holds: **EMPTY ≠ cause of OPEN**), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (**`soft530_open_since` ~08:41**; **`missed_clear_window` omit** — home half-ops), [missed-clear-window-shared-supersede.md](missed-clear-window-shared-supersede.md) (today's **~07:25–~08:41** = **home half-ops** — Shared cancel **correct**; **do not** stamp `missed_clear_window`), [post-dual-clear-go.md](post-dual-clear-go.md) (camp vault-on-Doc GO **HOLD** until next CLEAR + ≥30m + Shellable), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (full smoke **after** Shellable), [shared-fleet-cards.md](shared-fleet-cards.md) (Chief Shared amend **HOLD** until next CLEAR recover + ≥30m + Shellable; **CLEAR since ~07:25** queue **superseded**), [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) (**CONNECTED ≠ Shellable ≠ tunnel healthy**), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (camp still **Ben GO**), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (home-awake OPEN ≠ camp GO), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Soft-530 class and local-exec class are **two stamps**. ListMachines **EMPTY** does **not** make Soft-530 **OPEN**. Soft-530 **CLEAR** while EMPTY does **not** make camp GO / dual CLEAR / **#82** / unfreeze.

This fold executes **none** of the Shells, curls, hops, or GOs. Do **not** invent vault CLEAR, dual CLEAR, **#82**, unfreeze, **#79.1**, camp Zone, Bitwarden, a Shared amend, or a freeze re-verify from this paper.

---

## Split classes

| Class | What it is | What it is not |
|-------|------------|----------------|
| **Soft-530** | Public HTTP only: `api.` `/health`, `app.` / `ops.` (and waitlist OPTIONS/POST when scored — SSOT **`/waitlist`**, not **`/api/waitlist`**). Public `/login` `"b"` scrape = **`freeze_build_id_public`**. Lookout watches **this** class. | ListMachines presence. Shellable. KeepAlive. lid-restore. Shared amend. **`freeze_git_verified`**. |
| **Local-exec** | ListMachines + **CONNECTED+Shellable**. Shared amend, **`freeze_git_verified`**, KeepAlive assert, lid-restore, full [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on-host. | Soft-530 OPEN/CLEAR. Vault class. Option A / **#82**. **`freeze_build_id_public`**. |

**Lookout** watches public Soft-530 (+ vault `/alive`). **Chief** Shared amend / freeze re-verify stay **queued** until Docs is **CONNECTED+Shellable**. Do **not** ask Lookout to prove local-exec. Do **not** stamp Soft-530 from ListMachines.

---

## Living proof (~07:25–~08:41 America/Edmonton — CLEAR dwell ENDED)

Morning **CLEAR while EMPTY** (~07:25–~08:41, ≥51m by ~08:16) is the proof that **EMPTY ≠ Soft-530 OPEN**. The **~08:41** flip is public HTTP — **not** ListMachines.

| Field | Living |
|-------|--------|
| **Soft-530** | **OPEN** — Lookout `api.` **200→530** CF **1033**; Lead `api.` / `app.` / `ops.` all **530 / CF 1033**. **`soft530_open_since` ~08:41**. Prior CLEAR dwell **~07:25–~08:41** (~1h16m) **ENDED**. |
| **Same-day pattern** | blip **~07:06–~07:25**; CLEAR **~07:25–~08:41**; OPEN again **~08:41**. **EMPTY** throughout morning after **~07:25**. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). Essay: [soft-530-blip-recover.md](soft-530-blip-recover.md). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined HTTP** | Soft-530 **OPEN** + vault **OPEN** (both **1033**) — prior half-state **OVER**. **≠ dual CLEAR.** |
| **ListMachines** | **EMPTY** (Lead confirm). Local-exec **ABSENT**. **EMPTY ≠ cause of OPEN.** **CONNECTED ≠ Shellable ≠ tunnel healthy.** |
| **Combined ops** | Soft-530 **OPEN** + local-exec **EMPTY**. Camp / Shared stay **HOLD** until next CLEAR + ≥30m + Shellable. |
| **Option A** | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Shared** | **`shared_fleet_card_stale=true`**. Amend **HOLD** until next CLEAR recover + ≥30m + Shellable. Do **not** write OPEN-since-**~08:41** mid-flap. OPEN-since-**~07:06** queue **cancelled**. **CLEAR since ~07:25** queue **cancelled** — home half-ops (**not** missed camp GO). **`missed_clear_window` omit.** Do **not** backfill. |
| **`freeze_build_id_public`** | **`last_known` true** — public MATCH ~08:16. OPEN → login **530** — scrape **unreachable** (not a DIFF). Essay: [freeze-build-id-public-probe.md](freeze-build-id-public-probe.md). |
| **`freeze_git_verified`** | still **queued** until Shellable. Behind **intact**. **Never auto-pull.** |

Receipt: [overnight_2026-09-16_0841_open_verify.md](overnight_2026-09-16_0841_open_verify.md). Prior CLEAR+EMPTY proof: [overnight_2026-09-16_0816_freeze_build_id_public_probe.md](overnight_2026-09-16_0816_freeze_build_id_public_probe.md) · [overnight_2026-09-16_0751_clear_vs_local_exec_verify.md](overnight_2026-09-16_0751_clear_vs_local_exec_verify.md).

---

## Camp vault-on-Doc Ben GO gate (extends blip-recover into steady-state)

Lead **may re-offer** camp vault-on-Doc **Ben GO** only when **both** are true. This paper does **not** offer it.

| # | Gate | Living this fold (~08:41) |
|---|------|---------------------------|
| **1** | Soft-530 **CLEAR ≥30m SAME-CLASS** (still CLEAR; same **`soft530_clear_since`**; vault still **OPEN 1033**; no new OPEN flap) | Living **OPEN ~08:41** — dwell **reset**. Prior CLEAR dwell **~07:25–~08:41** **ENDED**. |
| **2** | Docs `95a229f5` **CONNECTED+Shellable** + [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on that host | **EMPTY** — fail |

**CLEAR alone while EMPTY = half-ops HOLD.** Extends [soft-530-blip-recover.md](soft-530-blip-recover.md) (`5221d90`) past the recover instant into **steady-state**: the GO window stays **paused** for as long as local-exec is EMPTY, even after the Soft-530 dwell later crosses 30m.

Until both gates, stay quiet on camp. **Ben GO** each later step; **never auto**.

---

## Who watches what

| Actor | Watches | Queued until Shellable |
|-------|---------|------------------------|
| **Lookout** | Public Soft-530 (`api.` `/health`) + vault `/alive` | — |
| **Lead** | Public Soft-530 / vault HTTP class; ListMachines identity | Full clear-smoke, lid-restore, KeepAlive assert |
| **Chief** | Stamp / Shared standing notes | Shared living-host amend **CLEAR since ~07:25** **superseded** (missed window — stamp never wrote). Next Shared write = next CLEAR recover + ≥30m + Shellable. **`freeze_git_verified`** from `/Users/dochak/src/Project-Car` still queued. Public **`freeze_build_id_public`** is Lead Soft-530 class — **not** this queue. |

Lookout **CLEAR** while ListMachines **EMPTY** is **expected half-ops**, not a Soft-530 relapse.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **EMPTY ≠ Soft-530 OPEN** | Soft-530 is public HTTP. EMPTY is local-exec **ABSENT**. Living **~07:25–~08:41** stayed CLEAR while EMPTY. **EMPTY ≠ cause of the ~08:41 OPEN.** |
| **CLEAR + EMPTY ≠ dual CLEAR** | Vault still **OPEN 1033**. Local-exec still **ABSENT**. Combined HTTP is **half-state**. Combined ops is **half-ops HOLD**. |
| **CLEAR + EMPTY ≠ camp GO** | Gate is ≥30m SAME-CLASS **AND** **CONNECTED+Shellable**. Dwell **PASS** at ~08:16; Shellable still **fail**. |
| **CLEAR + EMPTY ≠ #82 / unfreeze / Bitwarden / #79.1** | Each is a **separate Ben GO**. |
| **Never fan-out Garage / Zone on half-ops** | Brochure Home still **STALE** until **#82**. This paper is **not** an upload. |
| **Lead `/health` 200 + 307 ≠ clear-smoke** | Full smoke waits on **CONNECTED+Shellable**. **`freeze_build_id_public`** may record on half-ops. |
| **≠ Shared / `freeze_git_verified` write while EMPTY** | Chief stays **queued**. Public **`freeze_build_id_public`** is allowed. Docs/#70 is SSOT. |
| **Public BUILD_ID MATCH ≠ freeze live-verify PASS** | **`freeze_git_verified`** still queued. Essay: [freeze-build-id-public-probe.md](freeze-build-id-public-probe.md). |

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

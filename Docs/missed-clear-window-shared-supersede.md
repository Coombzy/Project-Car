# Missed CLEAR window — supersede Shared amend

**Status:** Paper — Shared living-host queue lock, **not** a GO  
**Updated:** 2026-09-16 ~08:49 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **OPEN** **`soft530_open_since` ~08:41** + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY** + this pointer), [shared-fleet-cards.md](shared-fleet-cards.md) (Shared **CLEAR since ~07:25** queue **superseded** — do **not** leave that write across the flap), [soft-530-blip-recover.md](soft-530-blip-recover.md) (short-blip recover lock still holds; this file names the **missed** CLEAR that never landed on Shared), [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) (**EMPTY ≠ Soft-530 OPEN** — EMPTY during CLEAR is why the window was missed), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (**`missed_clear_window`** field; **`shared_fleet_card_stale=true`**), [soft-530-extended-open.md](soft-530-extended-open.md) (missed window **≠** extended-open by itself), [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) (**CONNECTED ≠ Shellable ≠ tunnel healthy** — **never** `Mac.lan`), [post-dual-clear-go.md](post-dual-clear-go.md) (camp GO **HOLD**), [deployment-guide.md](deployment-guide.md) (Monday paper map)

A Soft-530 **CLEAR** dwell that meets public **≥30m** (or overnight CLEAR) is **not** a living Shared CLEAR stamp if Fleet Shared `shop-os-mc-plan.md` never got amended because ListMachines stayed **EMPTY** / **not Shellable** the **entire** window. That is a **missed CLEAR window**.

On the Soft-530 **OPEN** that **ends** that window: **cancel / supersede** the queued Shared **CLEAR** amend. Do **not** leave stale “write CLEAR since ~07:25” across the flap. Do **not** backfill the missed CLEAR as current living-host once OPEN.

This fold executes **none** of the Shells, curls, hops, or Shared writes. Do **not** invent vault CLEAR, dual CLEAR, **#82**, unfreeze, **#79.1**, camp Zone, Bitwarden, or an auto Shared write without Shellable.

---

## Lock — missed CLEAR window ≠ living Shared CLEAR

| This is | This is not |
|---------|-------------|
| Public Soft-530 **CLEAR** dwell that met **≥30m** (or overnight CLEAR) | A living Shared `shop-os-mc-plan.md` CLEAR stamp |
| Shared living-host amend **queued** for that CLEAR | Shared amend **DONE** |
| ListMachines **EMPTY** / **CONNECTED≠Shellable** the **entire** dwell | Docs **CONNECTED+Shellable** (the only host that may write Shared) |
| On later **OPEN**: **supersede** the queued CLEAR write | Leave “write CLEAR since \<start\>” queued across the flap |
| Optional stamp **`missed_clear_window`** | Treat the missed CLEAR as current living-host **after** OPEN |

**Gate that never opened.** Shared living-host amend needs Docs **CONNECTED+Shellable** (warm companion — [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md)). **Never** `Mac.lan`. If that gate stays closed for the whole CLEAR dwell, the public CLEAR is **honesty on Docs/#70 only**. Shared still carries the **prior** write. Docs/#70 → `main` is SSOT. Shared **never** overrides.

---

## Living proof (~08:49 America/Edmonton)

| Field | Living |
|-------|--------|
| **Soft-530** | **OPEN** — Lookout `api.` **200→530** CF **1033**; Lead `api.` / `app.` / `ops.` all **530 / CF 1033**. **`soft530_open_since` ~08:41**. |
| **Missed CLEAR window** | **`missed_clear_window={start:~07:25,end:~08:41,reason:empty}`**. Public dwell **~07:25–~08:41** (~1h16m) met **≥30m**. ListMachines **EMPTY** the **entire** dwell. Shared **CLEAR since ~07:25** was **queued**, then **OPEN ~08:41** landed **before** Shellable — **stamp never wrote**. |
| **Same-day pattern** | blip **~07:06–~07:25**; **missed** CLEAR **~07:25–~08:41**; OPEN again **~08:41**. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). Essay: [soft-530-blip-recover.md](soft-530-blip-recover.md). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined class** | Soft-530 **OPEN** + vault **OPEN** (both **1033**). **≠ dual CLEAR.** |
| **ListMachines** | **EMPTY** (Lead confirm ~07:25 **and** ~07:51 **and** ~08:16 **and** ~08:41). **EMPTY ≠ cause of OPEN.** **EMPTY during CLEAR ≠ Soft-530 OPEN.** |
| **Shared** | Last **DONE** write still **CLEAR since ~22:00** (~22:08). OPEN-since-**~07:06** queue **cancelled**. **CLEAR since ~07:25** queue **superseded**. Do **not** write OPEN-since-**~08:41** mid-flap. Do **not** backfill **CLEAR since ~07:25**. **`shared_fleet_card_stale=true`**. |
| **Next Shared write** | After the **next** CLEAR recover + **≥30m SAME-CLASS** + Docs **CONNECTED+Shellable**. Not this missed window. |
| **Option A** | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Camp / post-dual-clear-go** | **HOLD.** Missed window **≠** camp GO. |

Receipt: [overnight_2026-09-16_0849_missed_clear_window_verify.md](overnight_2026-09-16_0849_missed_clear_window_verify.md). Prior OPEN flip: [overnight_2026-09-16_0841_open_verify.md](overnight_2026-09-16_0841_open_verify.md). Prior CLEAR+EMPTY proof: [overnight_2026-09-16_0816_freeze_build_id_public_probe.md](overnight_2026-09-16_0816_freeze_build_id_public_probe.md) · [overnight_2026-09-16_0751_clear_vs_local_exec_verify.md](overnight_2026-09-16_0751_clear_vs_local_exec_verify.md).

---

## On OPEN that ends a missed CLEAR window

When Soft-530 **CLEAR→OPEN** after a CLEAR dwell that never got a Shared write:

1. **Cancel / supersede** the queued Shared **CLEAR** amend (living: **CLEAR since ~07:25**).
2. **Do not** leave that queue for overnight / morning readers, and **do not** land it if Docs later becomes Shellable **while still OPEN**.
3. Stamp **`missed_clear_window={start,end,reason}`** when useful. Living: **`{start:~07:25,end:~08:41,reason:empty}`**.
4. Keep **`shared_fleet_card_stale=true`**. Shared last DONE as-of stays the prior write (**CLEAR ~22:00**).
5. **Next** Shared write waits for the **next** CLEAR recover + **≥30m SAME-CLASS** + Docs **CONNECTED+Shellable**.
6. **Do not** backfill the missed CLEAR as current living-host once OPEN. **Do not** write OPEN-since-**~08:41** mid-flap.

**Chief this fold:** cancelling the Shared **CLEAR ~07:25** amend queue **now**. Paper records the supersede. This file does **not** execute the Shared file.

Essay: [shared-fleet-cards.md](shared-fleet-cards.md).

---

## Stamp field

| Field | Meaning | Living |
|-------|---------|--------|
| **`missed_clear_window`** | Start/end + reason when a public CLEAR dwell met **≥30m** (or overnight CLEAR) but Shared never amended because local-exec stayed **EMPTY** / **≠Shellable** the whole window | **`{start:~07:25,end:~08:41,reason:empty}`** |

Cross [overnight-baseline-stamp.md](overnight-baseline-stamp.md). Reason **`empty`** = ListMachines **EMPTY** (or **CONNECTED≠Shellable**) entire dwell. This field is **optional** — omit when Shared **DID** land the CLEAR (example: **~22:08** amend after **~22:00** CLEAR + Shellable).

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Missed window ≠ Soft-530 extended-open** | Extended-open is quiet-ops after **OPEN ~24h** + vault OPEN + **Mac.lan only** ([soft-530-extended-open.md](soft-530-extended-open.md)). A missed CLEAR is a **Shared-queue** class. |
| **≠ Ben re-nag** | Quiet. Shared amend ≠ Ben ask. Doc-wake already asked. |
| **≠ auto Shared write without Shellable** | EMPTY / **CONNECTED≠Shellable** **never** writes Shared. **Never** `Mac.lan`. |
| **≠ treat EMPTY during CLEAR as Soft-530 OPEN** | Soft-530 is public HTTP. Living **~07:25–~08:41** stayed **CLEAR** while EMPTY. Essay: [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md). |
| **≠ #82 / unfreeze / Bitwarden / camp GO** | Each is a **separate Ben GO**. Missed window **≠** those GOs. Home **STALE** until **#82**. |
| **≠ backfill CLEAR since ~07:25 once OPEN** | The window **ended**. Next write is the **next** CLEAR recover, not this one. |
| **≠ write OPEN-since-~08:41 mid-flap** | Shared amend **HOLD** until next CLEAR + ≥30m + Shellable. |

**#82** Ben GO / companions **HOLD** / freeze `4cf8924` / `5swmVz` / vault subclass 502 vs 1033 — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat a public ≥30m (or overnight) CLEAR as a living Shared CLEAR when ListMachines stayed **EMPTY** / **≠Shellable** the whole window
- Leave the queued Shared **CLEAR since ~07:25** amend across the **~08:41** OPEN flap
- Backfill the missed CLEAR as current living-host once Soft-530 is **OPEN**
- Write Shared **OPEN since ~08:41** mid-flap
- Auto-write Shared without Docs **CONNECTED+Shellable**
- Treat ListMachines **EMPTY** during CLEAR as Soft-530 **OPEN**
- Collapse this into [soft-530-extended-open.md](soft-530-extended-open.md)
- Re-nag Ben
- Auto-fire camp / **#82** / **#79.1** / unfreeze / Bitwarden
- Treat `Mac.lan` as Doc

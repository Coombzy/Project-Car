# Missed CLEAR window — camp dual-CLEAR GO only

**Status:** Paper — Shared living-host + stamp lock, **not** a GO  
**Updated:** 2026-09-16 ~12:29 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **OPEN** **`soft530_open_since` ~08:41** SAME-CLASS ~**3.8h** + vault **OPEN 530 / CF 1033** + ListMachines **Laptop.local only** + this pointer — **do not** carry missed-GO debt), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (**home half-ops CLEAR** = Soft-530 **CLEAR** while Docs **ABSENT** — **not** a missed camp GO), [shared-fleet-cards.md](shared-fleet-cards.md) (Shared **CLEAR since ~07:25** queue **cancelled** — correct; **`shared_fleet_card_stale=true`**), [soft-530-blip-recover.md](soft-530-blip-recover.md) (short-blip recover lock still holds), [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) (**EMPTY ≠ Soft-530 OPEN** — EMPTY during CLEAR is home half-ops, not a Shared-amend failure), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (`missed_clear_window` **only** when camp dual-CLEAR GO was armed; **`shared_fleet_card_stale=true`**), [soft-530-extended-open.md](soft-530-extended-open.md) (OPEN + Laptop-only + Lookout brochure **GONE** = quiet-ops), [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) (**CONNECTED ≠ Shellable ≠ tunnel healthy** — **never** `Mac.lan` / **Laptop.local** as Docs), [post-dual-clear-go.md](post-dual-clear-go.md) (camp GO **HOLD**), [deployment-guide.md](deployment-guide.md) (Monday paper map)

`d582984` stamped today's **~07:25–~08:41** EMPTY CLEAR as **`missed_clear_window`**. That **over-accounted**. Soft-530 **CLEAR** while Docs **ABSENT** is **home half-ops living** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)) — **not** a missed camp GO and **not** a Shared amend failure.

**Shared cancel stays correct.** Do **not** leave a queued “write CLEAR since ~07:25” across the **~08:41** OPEN. Do **not** backfill that CLEAR as current living-host once OPEN. Cancel ≠ missed-GO debt. **Do not** carry `missed_clear_window={start:~07:25,end:~08:41,reason:empty}` into STATUS Reality.

This fold executes **none** of the Shells, curls, hops, or Shared writes. Do **not** invent vault CLEAR, dual CLEAR, **#82**, unfreeze, **#79.1**, camp Zone, Bitwarden, companions re-ask, or an auto Shared write without Shellable.

---

## Lock — when to stamp `missed_clear_window`

| Stamp `missed_clear_window` | Do not stamp |
|-----------------------------|--------------|
| Ben had an **explicit camp dual-CLEAR GO armed** | Soft-530 **CLEAR** while Docs **ABSENT** (home half-ops) |
| Docs **CONNECTED+Shellable** was the **armed** gate for that GO | Shared living-host amend **queued** then **cancelled** because EMPTY / ≠Shellable |
| Shellable **never arrived** before the CLEAR ended | Public ≥30m CLEAR + EMPTY with **no** camp GO armed |
| Paper records start/end + that the armed GO **missed** Shellable | Treat Shared cancel as a Shared-amend **failure** or missed camp GO |

**Home half-ops CLEAR ≠ missed camp GO.** Soft-530 class is public HTTP. Docs **ABSENT** / ListMachines **EMPTY** during a home CLEAR is **expected home half-ops** — not a camp cutover miss and not a Shared SSOT miss. Docs/#70 → `main` is SSOT. Shared **never** overrides.

**Shared hygiene (still true):** if a CLEAR amend was queued and OPEN lands before Shellable, **cancel** that queue. That is standing-notes hygiene. It does **not** mint `missed_clear_window`.

---

## Living proof (~12:29 America/Edmonton)

| Field | Living |
|-------|--------|
| **Soft-530** | **OPEN** — Lookout `api.` **200→530** CF **1033**; Lead `api.` / `app.` / `ops.` all **530 / CF 1033**. **`soft530_open_since` ~08:41**. SAME-CLASS ~**3.8h**. |
| **Today's EMPTY CLEAR** | **~07:25–~08:41** (~1h16m). Docs **ABSENT** / ListMachines **EMPTY** the entire dwell. **Home half-ops living.** **Not** a missed camp GO. **Not** a Shared amend failure. |
| **`missed_clear_window`** | **Omit.** No explicit camp dual-CLEAR GO was armed. Do **not** carry `{start:~07:25,end:~08:41,reason:empty}` in STATUS Reality. |
| **Same-day pattern** | blip **~07:06–~07:25**; home half-ops CLEAR **~07:25–~08:41**; OPEN again **~08:41**. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). Essay: [soft-530-blip-recover.md](soft-530-blip-recover.md). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined class** | Soft-530 **OPEN** + vault **OPEN** (both **1033**). **≠ dual CLEAR.** Quiet-ops. |
| **ListMachines** | **Laptop.local only** (`Mac.lan` ≠ Docs). **EMPTY→Laptop-only is non-progress.** **Never** treat laptop as Docs lid-restore. **EMPTY ≠ cause of OPEN.** |
| **Shared** | Last **DONE** write still **CLEAR since ~22:00** (~22:08). OPEN-since-**~07:06** queue **cancelled**. **CLEAR since ~07:25** queue **cancelled** — **correct**. Do **not** write OPEN-since-**~08:41** mid-flap. Do **not** backfill **CLEAR since ~07:25**. **`shared_fleet_card_stale=true`**. |
| **Next Shared write** | After the **next** CLEAR recover + **≥30m SAME-CLASS** + Docs **CONNECTED+Shellable**. Not this home half-ops window. |
| **Option A** | **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Lookout brochure** | Option A Dynamic watch **GONE**. Quiet-ops. **HOLD** second Ben recreate. |
| **Camp / post-dual-clear-go** | **HOLD.** Home half-ops CLEAR **≠** camp GO. |

Receipt: [overnight_2026-09-16_1229_home_half_ops_clear_verify.md](overnight_2026-09-16_1229_home_half_ops_clear_verify.md). Prior `d582984` receipt ([overnight_2026-09-16_0849_missed_clear_window_verify.md](overnight_2026-09-16_0849_missed_clear_window_verify.md)) keeps the Shared **cancel** — **reclassify** the `missed_clear_window` stamp as **over-accounted**. Prior OPEN flip: [overnight_2026-09-16_0841_open_verify.md](overnight_2026-09-16_0841_open_verify.md).

---

## On OPEN that ends a home half-ops CLEAR

When Soft-530 **CLEAR→OPEN** after a home CLEAR that never had Docs Shellable **and** no camp dual-CLEAR GO was armed:

1. **Cancel** the queued Shared **CLEAR** amend (living: **CLEAR since ~07:25**). Correct hygiene.
2. **Do not** leave that queue for overnight / morning readers, and **do not** land it if Docs later becomes Shellable **while still OPEN**.
3. **Do not** stamp **`missed_clear_window`**. That field is **camp dual-CLEAR GO armed + Shellable never arrived** only.
4. Keep **`shared_fleet_card_stale=true`**. Shared last DONE as-of stays the prior write (**CLEAR ~22:00**).
5. **Next** Shared write waits for the **next** CLEAR recover + **≥30m SAME-CLASS** + Docs **CONNECTED+Shellable**.
6. **Do not** backfill the home half-ops CLEAR as current living-host once OPEN. **Do not** write OPEN-since-**~08:41** mid-flap.
7. **Do not** carry missed-GO debt into STATUS Reality.

**Chief this fold:** Shared **CLEAR ~07:25** cancel **stands**. STATUS Reality **drops** the missed-GO stamp. This file does **not** execute the Shared file.

Essay: [shared-fleet-cards.md](shared-fleet-cards.md) · [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md).

---

## Stamp field

| Field | Meaning | Living |
|-------|---------|--------|
| **`missed_clear_window`** | Start/end + reason **only** when Ben had an **explicit camp dual-CLEAR GO armed** and Docs **CONNECTED+Shellable** never arrived before the CLEAR ended | **Omit.** Today's **~07:25–~08:41** was home half-ops. |

Cross [overnight-baseline-stamp.md](overnight-baseline-stamp.md). Omit when Shared **DID** land the CLEAR (example: **~22:08** after **~22:00** + Shellable). Omit when the CLEAR was **home half-ops** (Docs **ABSENT**, no camp GO armed). Shared cancel of a queued write is **not** this field.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Home half-ops CLEAR ≠ missed camp GO** | Docs **ABSENT** + Soft-530 **CLEAR** is home living. Camp GO was **not** armed. |
| **Shared cancel ≠ Shared amend failure** | Cancel is correct hygiene. Docs/#70 is SSOT. |
| **≠ carry missed-GO debt into STATUS Reality** | `d582984` over-accounted. Drop `{start:~07:25,end:~08:41,reason:empty}` from living Reality. |
| **≠ Soft-530 extended-open** | Extended-open is quiet-ops after **OPEN ~24h** + vault OPEN + laptop-only ([soft-530-extended-open.md](soft-530-extended-open.md)). Living OPEN ~**3.8h** + Lookout brochure **GONE** stays quiet-ops **without** inventing extended-open from this window. |
| **≠ Ben re-nag / #82 re-nag** | Quiet. Shared cancel ≠ Ben ask. Home **STALE** until **#82** — do **not** re-nag. |
| **≠ companions re-ask** | Companions **HOLD**. Brochure recreate **HOLD**. |
| **≠ Garage / Zone / Hatch fan-out** | Paper only. |
| **≠ auto Shared write without Shellable** | EMPTY / **CONNECTED≠Shellable** **never** writes Shared. **Never** `Mac.lan` / **Laptop.local**. |
| **≠ treat EMPTY during CLEAR as Soft-530 OPEN** | Soft-530 is public HTTP. Living **~07:25–~08:41** stayed **CLEAR** while EMPTY. Essay: [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md). |
| **≠ backfill CLEAR since ~07:25 once OPEN** | The window **ended**. Next write is the **next** CLEAR recover, not this one. |
| **≠ write OPEN-since-~08:41 mid-flap** | Shared amend **HOLD** until next CLEAR + ≥30m + Shellable. |

**#82** Ben GO / companions **HOLD** / freeze `4cf8924` / `5swmVz` / vault subclass 502 vs 1033 — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat Soft-530 **CLEAR** while Docs **ABSENT** as a missed camp GO or Shared amend failure
- Stamp **`missed_clear_window`** unless Ben had an **explicit camp dual-CLEAR GO armed** and Shellable never arrived
- Carry `{start:~07:25,end:~08:41,reason:empty}` as missed-GO debt in STATUS Reality
- Leave the queued Shared **CLEAR since ~07:25** amend across the **~08:41** OPEN flap (cancel **stands**)
- Backfill the home half-ops CLEAR as current living-host once Soft-530 is **OPEN**
- Write Shared **OPEN since ~08:41** mid-flap
- Auto-write Shared without Docs **CONNECTED+Shellable**
- Treat ListMachines **EMPTY** during CLEAR as Soft-530 **OPEN**
- Re-nag **#82** / companions / Garage / Zone / Hatch
- Treat `Mac.lan` or **Laptop.local** as Doc

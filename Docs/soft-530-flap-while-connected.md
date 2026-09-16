# Soft-530 flap while CONNECTED — desktop/local-exec dead

**Status:** Paper — presence class + first hop, **not** a GO  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (living half-state Soft-530 **CLEAR ~22:00** + vault **OPEN** + ListMachines **EMPTY** after this flap + this pointer), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**next CONNECTED after ABSENT** — identity `95a229f5-9296-4a18-aa98-70fd300dabdf`; **not** this card’s no-ABSENT-gap warm path), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (CLEAR proof **after** Shellable + cloudflared/KeepAlive — **never** from ListMachines CONNECTED alone), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (**home EXPECTED** = Docs **ABSENT** + Soft-530 **OPEN** — **not** this flap; this flap is home-awake desktop/local-exec dead, then ABSENT), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (must **not** keep Soft-530=CLEAR after a live OPEN flip; **`soft530_open_since`** = wall of that OPEN flip; optional same-day CLEAR dwell; morning ages from last relapse **not** Sep 13; CONNECTED+Shell-unreachable → ABSENT = absorb; next CONNECTED = doc-reappear; same-class quiet), [shared-fleet-cards.md](shared-fleet-cards.md) (Shared living-host lines must carry Soft-530 **class + as-of**; same-day **CLEAR↔OPEN** after Shared rewrite → **queue** Shared living-host amend on next Docs CONNECTED+**Shellable** — this warm companion, **never** `Mac.lan`; Docs/#70→`main` is SSOT; Shared ~15:42 **CLEAR** as-of is stale vs living **CLEAR ~22:00** / ListMachines **EMPTY**), [doc-lid-restore.md](doc-lid-restore.md) (process wake — **only** when CONNECTED+**Shellable**), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops **HOLD** after one Ben ask), [deployment-guide.md](deployment-guide.md) (Monday paper map)

**CONNECTED ≠ Shellable ≠ tunnel healthy.** ListMachines CONNECTED is not Soft-530 CLEAR and is not a lid-restore host.

Evidence **2026-09-15** America/Edmonton: Soft-530 **CLEAR ~13:21–16:36**, then **CLEAR→OPEN ~16:36** with Docs ListMachines **CONNECTED** (`95a229f5`) but Shell **unreachable** (3+ tries); tunnels **530 / CF 1033**. Later ListMachines **emptied** (Lead-verified **EMPTY ~16:51**).

This fold executes **none** of the Shells, curls, hops, or GOs. Do **not** invent Soft-530 CLEAR, vault CLEAR, **#82**, unfreeze, camp Zone, or Bitwarden from this paper.

---

## Three Doc presence classes

Do **not** collapse. Only **CONNECTED+Shellable** can run lid-restore / KeepAlive / [soft-530-clear-smoke.md](soft-530-clear-smoke.md).

| Class | ListMachines | Shell | What you may run | Not this |
|-------|--------------|-------|------------------|----------|
| **ABSENT** | Docs `95a229f5` **not** present | n/a | Stay quiet. Next CONNECTED → [doc-reappear-first-hop.md](doc-reappear-first-hop.md). Home **EXPECTED** is this class + Soft-530 **OPEN** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). | Treat as CONNECTED. Queue lid-restore. Score Soft-530 CLEAR. |
| **CONNECTED+Shell-unreachable** | Docs `95a229f5` **CONNECTED** | Shell **unreachable** (retry sparingly) | Assert identity. Park recovery. Ben ask **once**. Quiet-ops **HOLD** after. | Lid-restore / KeepAlive / clear-smoke. Treat as multi-day cold ABSENT. Treat as home intentional off. |
| **CONNECTED+Shellable** | Docs `95a229f5` **CONNECTED** | Shell **works** on asserted Doc | Lid-restore / KeepAlive / [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on **that** host only. Also the host for a **queued** Shared living-host Soft-530 class+as-of amend ([shared-fleet-cards.md](shared-fleet-cards.md)). | Shell `Mac.lan` as Doc. Skip identity. Treat Shared amend as Ben ask / **#82** / camp. |

Identity lock is unchanged: machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. **Never** `Mac.lan` / Porsche as Doc.

---

## Flap-while-connected (this class)

Soft-530 **CLEAR→OPEN** while **CONNECTED+Shell-unreachable** = **flap-while-connected** (desktop / local-exec **dead**).

| This is | This is not |
|---------|-------------|
| Desktop / Grok Bot / local-exec dead on a still-listed Docs Mac | Multi-day **cold ABSENT** ([doc-reappear-first-hop.md](doc-reappear-first-hop.md) cold-boot) |
| Tunnels **530 / CF 1033** with a CONNECTED name | Soft-530 **CLEAR** because ListMachines says CONNECTED |
| Home-awake exec-dead, then maybe ABSENT | Home **intentional off** — home EXPECTED is Docs **ABSENT** from the start ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)) |

**2026-09-15 receipt:** CLEAR **~13:21–16:36** → OPEN **~16:36** (Docs CONNECTED / Shell unreachable / tunnels 1033) → ListMachines **EMPTY ~16:51**.

---

## First hop (CONNECTED+Shell-unreachable)

Run **in order**. This paper executes **none** of it.

| # | Hop | Lock |
|---|-----|------|
| **1** | **Assert** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`** | **Never** `Mac.lan` as Doc. Name-only ≠ identity. |
| **2** | **Retry Shell sparingly** (do not loop) | 3+ fails = still this class. |
| **3** | **If still unreachable → park recovery** | No lid-restore. No KeepAlive. No clear-smoke. |
| **4** | **Ben ask once** (Doc awake / desktop) | Already asked **2026-09-15** — **no re-nag**. |
| **5** | **Quiet-ops HOLD after** | Duration ≠ second ask. [soft-530-extended-open.md](soft-530-extended-open.md). |

---

## When Shell returns — two forks

| Path | Gate | First cards | Not this |
|------|------|-------------|----------|
| **Warm path (no ABSENT gap)** | Still **CONNECTED**, Shell **returns** without an ABSENT gap | Restart **cloudflared** + shop KeepAlive on asserted Doc → [soft-530-clear-smoke.md](soft-530-clear-smoke.md). **Not** the multi-day cold-boot card. | Walk [doc-reappear-first-hop.md](doc-reappear-first-hop.md) cold-boot C1–C3 as if Docs were ABSENT ≥1 calendar day. |
| **ABSENT absorb (living ~16:51)** | **CONNECTED+Shell-unreachable → ABSENT** | **Absorb** the ListMachines DIFF ([overnight-baseline-stamp.md](overnight-baseline-stamp.md)). Stay quiet. **Next CONNECTED** uses [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (identity, then warm vs cold). | Re-nag Ben. Keep stamping CONNECTED. Keep Soft-530=CLEAR. Queue lid-restore from ABSENT. |

Living **~16:51** took the **ABSENT absorb** fork.

---

## Overnight stamp

After a **live** Soft-530 **OPEN** flip, the last weekday `*/20` / paper stamp must **not** keep Soft-530=**CLEAR**. Stamp **`soft530_open_since`** = wall of that flip (living **~16:36**) plus optional same-day CLEAR dwell (living **~13:21–16:36**). Tonight **~17:20** / **~17:40**: Soft-530 **OPEN 530 / CF 1033** + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY**. Morning ages OPEN from last relapse, **not** the Sep 13 multi-day clock. Same-class morning (still OPEN + same `soft530_open_since`) = stay quiet. Next Docs CONNECTED = [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (absorbed DIFF — **no Ben re-surface** if HTTP class unchanged). Same-day **CLEAR↔OPEN** after the Shared ~15:42 rewrite also **queues** a Shared living-host Soft-530 class+as-of amend on the **next CONNECTED+Shellable** ([shared-fleet-cards.md](shared-fleet-cards.md)) — warm companion, **never** `Mac.lan`; amend ≠ Ben ask. CONNECTED+Shellable **failed** after this flip → overnight stamp **`shared_fleet_card_stale=true`**. Morning first-hop **amends Shared before treating Shared as living**. Shared never overrides Docs/#70 SSOT.

---

## Living now (~16:51 America/Edmonton) — historical flap absorb

Soft-530 then **OPEN 530 / CF 1033** **`soft530_open_since` ~16:36** (same-day CLEAR dwell **~13:21–16:36**). Vault **OPEN 530 / CF 1033**. ListMachines **EMPTY** / Docs **ABSENT** (after flap; prior CONNECTED+Shell-unreachable **~16:36**). That absorb is **historical**.

## Living now (~22:08 America/Edmonton)

Soft-530 **CLEAR** **`soft530_clear_since` ~22:00** (same-day OPEN dwell **~16:36–22:00**). Vault still **OPEN 530 / CF 1033**. Docs `95a229f5` **CONNECTED+Shellable** / KeepAlive **UP** ~22:07–22:08 (EMPTY flap **~16:51–22:00** ended). Option A Redirect+UX **PASS**. Home **STALE** until **#82**. Freeze **`4cf8924` / `5swmVz`**. Lookout api+vault **armed**. Companions **HOLD** forensics. Ben asked once — **no re-nag**. Quiet-ops **HOLD**. **#82** not auto-GO. **`shared_fleet_card_stale=false`**. Half-state ≠ dual CLEAR.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **ListMachines CONNECTED ≠ Soft-530 CLEAR** | CONNECTED is a presence class. CLEAR is `/health` **200** + OPTIONS CORS + POST **422**/**201**. |
| **Never `Mac.lan` as Doc** | Identity is `95a229f5`. |
| **Never lid-restore / KeepAlive / clear-smoke while Shell-unreachable** | Only **CONNECTED+Shellable**. |
| **Never treat this flap as multi-day cold ABSENT** | Cold-boot is ABSENT ≥1 calendar day / OPEN 1033 ≥24h with Docs ABSENT. |
| **Never treat this flap as home intentional off** | Home EXPECTED is Docs **ABSENT** from the start — not CONNECTED-then-dead. |
| **Never auto unfreeze / #82 / camp Zone / Bitwarden** | Paper only. Soft-530 **OPEN ≠ #82 blocked** still holds — this card does **not** GO it. |
| **Never keep Soft-530=CLEAR on the overnight stamp after a live OPEN flip** | Living ~16:36 OPEN; ~16:51 EMPTY. Tonight ~17:20 / ~17:40 must stamp **OPEN**. **`soft530_open_since` ~16:36** — morning ages from last relapse, not Sep 13. |
| **Never re-nag Ben** | Asked once Doc awake/desktop. Quiet-ops **HOLD**. |

**#82** Ben GO / companions **HOLD** / freeze `4cf8924` / `5swmVz` / camp GO / vault subclass 502 vs 1033 — **unchanged**. This file executes **none** of those.

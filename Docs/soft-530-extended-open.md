# Soft-530 extended OPEN — quiet-ops lock

**Status:** Living ops — paper lock  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (**Mon–Thu nights** after last weekday `*/20` ~17:40 MT until next weekday first fire ~06:00 — Lookout api+vault only; Friday last `*/20` → weekend coverage; this lock is **not** that coverage card), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**first hop** when `Docs-MacBook-Pro` reappears — machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`; **never** `Mac.lan` / Porsche), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** when `lightning` / McKing reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**first** recovery smoke after extended-OPEN Soft-530 CLEAR — **before** desk / **#79.1** / unfreeze), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke after extended-OPEN vault CLEAR — **before** Bitwarden / desk), [dual-host-outage.md](dual-host-outage.md) (wake order — **not** this lock), [vault-stay-up.md](vault-stay-up.md) (McKing half + forensics `@d88cacb`), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A Lookout **spec** — living watch **GONE**), [lookout-rearm-sop.md](lookout-rearm-sop.md) (never delete to fix cron; **HOLD** after one Ben ask; interim Chief `*/20`; **#78 LIVE-SUPERSEDED**), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — **never auto-fire**), [doc-lid-restore.md](doc-lid-restore.md) (Lead process wake on the **asserted** host), [deployment-guide.md](deployment-guide.md) (Monday paper map)

When Soft-530 **OPEN** crosses **~24h** **and** vault is **OPEN** **and** ListMachines is **only `Mac.lan`**, lock **quiet-ops**. This file names that lock. It is **not** wake order ([dual-host-outage.md](dual-host-outage.md)), **not** the CLEAR menu ([post-dual-clear-go.md](post-dual-clear-go.md)), and **not** a Ben re-nag.

Do **not** invent CLEAR, **#82**, unfreeze, Zone Direct Upload, Bitwarden, or a companion re-ask from duration alone. This fold executes **none** of those.

---

## Gate (all three)

Quiet-ops is **in force** when every row is true. Living this fold: they are.

| Gate | Living stamp |
|------|----------------|
| **Soft-530 OPEN ~24h+** | CF **1033** since 2026-09-13 **~11:57** America/Edmonton (`api.` / `app.` / `ops.` / `cloud.` + waitlist OPTIONS) |
| **Vault OPEN** | **502** since 2026-09-13 **~19:45** MT (**not** 1033) on `/alive` + `/api/config` |
| **Only `Mac.lan`** | `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`. Lid-restore + vault wake **blocked** until the right host appears |

Weekend coverage (`84107e7`) was Sat/Sun plan-improve-off. Weekday overnight ([soft-530-weekday-overnight.md](soft-530-weekday-overnight.md)) is the **Mon–Thu** twin after last `*/20` (~17:40 MT) until next weekday first fire (~06:00) — Lookout api+vault only; Friday last `*/20` still hands into weekend coverage. This lock is **not** weekend-only and **not** that overnight coverage card. It holds through the week until a host reappears **or** Ben reopens a named ask.

---

## Quiet-ops lock (five)

| # | Lock | Meaning |
|---|------|---------|
| **1** | **No Ben re-nag** | Doc-wake + McKing wake **already asked**. Do **not** page Ben again because the clock crossed ~24h. |
| **2** | **Lead + Chief stay armed** | **Lead** stays armed for ListMachines **`Docs-MacBook-Pro`** reappear → [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (assert machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**, **never** `Mac.lan` / Porsche) **then** [doc-lid-restore.md](doc-lid-restore.md) **process wake only**. **Chief** stays armed for **`lightning`** reappear → [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (assert machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**, **never** `Mac.lan`) **then** [vault-stay-up.md](vault-stay-up.md) vault wake. Identity lock unchanged — no `Mac.lan` Shell. |
| **3** | **Lookout continues; companions HOLD until Ben reopens** | Lookout `api.` `/health` + vault `/alive` stay **armed** — **never delete** them to fix stalled cron ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Brochure-redirect **paper** **continues** ([brochure-redirect-watch.md](brochure-redirect-watch.md)). Living Option A continuous watch is **GONE** (deleted to fix stalled cron; Auto-review blocked recreate) — **HOLD** after one Ben ask; interim = Chief `*/20` redirect smoke. Soft-530 companions stay **HOLD / not armed** until **Ben reopens** — **not** weekend-only. Do **not** re-ask. **#78 lookout-resume** is **LIVE-SUPERSEDED** (api-health already `enabled:true`). |
| **4** | **Option A is public SSOT** | Brochure Option A is the public live SSOT during extended OPEN (Zone Redirect **FULL 10/10**; `waitlist.js?v=3`; `styles.css?v=36`; Soft-530 Discord honesty). Home still bare `href="/"` + canonical/og apex until **#82**. **#70** Reality tip / Option A stays SSOT until **#82**. |
| **5** | **Duration alone ≠ GO** | Crossing ~24h is **not** **#82** GO, **not** unfreeze, **not** Zone Direct Upload, **not** Bitwarden import/rotate, **not** companion re-ask. |

Wake order when a host **does** reappear stays [dual-host-outage.md](dual-host-outage.md) — **Doc first, then McKing**; parallel only if both names are on ListMachines. Doc’s **first hop** on reappear is [doc-reappear-first-hop.md](doc-reappear-first-hop.md) — identity, then smoke, then (only if CLEAR) forensics, then the sequencer (**never auto-fire**). McKing’s **first hop** on reappear is [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) — identity, then vault-clear-smoke, then (only if CLEAR) forensics, then Soft-530 independence (**never auto Bitwarden**; vault CLEAR ≠ Soft-530 CLEAR ≠ unfreeze / **#82** GO).

---

## CLEAR path (unchanged)

**CLEAR path is still** [post-dual-clear-go.md](post-dual-clear-go.md). Quiet-ops does **not** rewrite the menu.

After a **live** Soft-530 CLEAR **and** a **live** vault CLEAR **and** both forensic papers (`55e10d0` / `d88cacb`), Ben’s GO menu is **ordered** and **never auto-fire**. Duration of this OPEN does **not** skip KeepAlive, does **not** auto-GO **#82**, and does **not** unfreeze. Soft-530 **OPEN ≠ #82 blocked** — Ben may GO **#82** Worker-live while Soft-530/vault still **OPEN** (brochure is CF Worker/Zone, not Doc tunnel). KeepAlive→**#82** stays the *default ordered menu after dual CLEAR*.

---

## Next Soft-530 CLEAR after this lock

After an **extended** Soft-530 OPEN, the **next** Soft-530 **CLEAR** runs [soft-530-clear-smoke.md](soft-530-clear-smoke.md) **first** — **before** Owner desk / **#79.1** / unfreeze talk: `api.` `/health` **200** + waitlist OPTIONS CORS (apex **and** www) + waitlist POST **422** or **201** (route alive, not just tunnel-up) + note `app.`/`ops.` may still **307**→`/login` with print `` `changeme` `` (freeze, **not** Soft-530) + `cloud.` `status.php` **200** when Doc public is up. CLEAR path still [post-dual-clear-go.md](post-dual-clear-go.md) (**never auto-fire**). This paper does **not** execute that smoke and does **not** invent CLEAR.

---

## Next vault CLEAR after this lock

When `lightning` **first reappears**, the hop is [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**). After an **extended** vault OPEN (**502** since ~19:45 MT Sep 13), the **next** vault **CLEAR** runs [vault-clear-smoke.md](vault-clear-smoke.md) **first** — **before** Bitwarden / desk: `/alive` **200** + `/api/config` **200** / McKing **2026.6.0** class (not Doc **2025.12.0**) + classify **502→200** (not CF **1033→200**). Soft-530 may still be **OPEN**. Bitwarden stays **Ben GO**, **never auto-fire**. Forensics still [vault-stay-up.md](vault-stay-up.md) (`d88cacb`). CLEAR path still [post-dual-clear-go.md](post-dual-clear-go.md) (**never auto-fire**). This paper does **not** execute that smoke and does **not** invent CLEAR.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Ben re-nag** | Doc-wake + McKing wake already asked. Clock ≠ new Ben ask. |
| **Duration = #82 GO** | Quiet-ops duration still ≠ auto-GO. Soft-530 **OPEN ≠ #82 blocked** — Ben may GO **#82** Worker-live while Soft-530/vault still **OPEN** (brochure is CF Worker/Zone). Dual CLEAR ≠ auto-GO. KeepAlive→**#82** stays the default menu *after* dual CLEAR ([post-dual-clear-go.md](post-dual-clear-go.md)). |
| **Duration = unfreeze** | Freeze `4cf8924` / **`5swmVz`** until **Ben GO**. |
| **Duration = Zone Direct Upload** | No Worker upload / purge from extended OPEN. |
| **Duration = Bitwarden** | Import/rotate **blocked** until vault **CLEAR**. |
| **Duration = companion re-ask** | Companions **HOLD** until **Ben reopens** — not weekend-only, not clock-only. |
| **Drop Lookout** | `api.` + vault stay armed. Brochure-redirect **paper** continues. Continuous Option A watch is **GONE** — interim Chief `*/20` ([lookout-rearm-sop.md](lookout-rearm-sop.md)). |
| **Delete a watch to fix cron** | Forbidden. Prefer in-place update / pause-resume / re-save. Living Option A delete already happened — **HOLD** recreate. |
| **Invent CLEAR** | Soft-530 still **OPEN** (CF **1033**). Vault still **OPEN** (**502**). Only `Mac.lan`. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / brochure-redirect watch paper (`f336fcb`) / **#78 LIVE-SUPERSEDED** — **unchanged**. Option A continuous watch is **GONE** — SOP [lookout-rearm-sop.md](lookout-rearm-sop.md). This file executes **none** of those.

---

## Do not

- Re-nag Ben for Doc-wake or McKing wake (already asked)
- Treat ~24h OPEN as **#82**, unfreeze, Zone Direct Upload, Bitwarden, or companion re-ask
- Drop Lookout `api.` / vault / brochure-redirect **paper** because quiet-ops is on
- Delete an armed Lookout watch to fix stalled cron (living Option A watch is already **GONE** — **HOLD** recreate; [lookout-rearm-sop.md](lookout-rearm-sop.md))
- Arm Soft-530 companions from this paper, or treat HOLD as weekend-only
- Collapse this lock into [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (overnight is coverage; this file is quiet-ops)
- Re-open **#78** (api-health already `enabled:true` — **LIVE-SUPERSEDED**)
- Shell `Mac.lan` or Porsche as Doc or McKing
- Skip [doc-reappear-first-hop.md](doc-reappear-first-hop.md) identity (machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`) when `Docs-MacBook-Pro` first reappears
- Skip [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) identity (machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`) when `lightning` first reappears
- Invent a CLEAR while Soft-530 is still **OPEN** (CF **1033**) or vault is still **OPEN** (**502**)
- Execute the [soft-530-clear-smoke.md](soft-530-clear-smoke.md) curls, desk, **#79.1**, or unfreeze from this bounce
- Execute the [vault-clear-smoke.md](vault-clear-smoke.md) curls or Bitwarden from this bounce
- Execute Zone / Garage / Lookout arm from this paper

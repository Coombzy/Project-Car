# Overnight baseline stamp — last weekday `*/20` one-liner

**Status:** Living ops — paper lock  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (**Mon–Thu nights** after last weekday `*/20` ~17:40 MT until next weekday first fire ~06:00 — Lookout api+vault only; this file is the **pre-gap stamp**, **not** that coverage card), weekend Soft-530 coverage (`84107e7` — Friday last `*/20` stamps **then** hands here; Sat/Sun plan-improve-off), [lookout-rearm-sop.md](lookout-rearm-sop.md) (weekday Chief `*/20` **+ Soft-530 UX**; overnight/weekend Option A Dynamic redirect **UNCOVERED** — `c200d71`; **HOLD** second Ben recreate ask), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A **paper** continues; continuous watch **GONE**), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**first hop** if Doc reappears — machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`; **never** `Mac.lan` / Porsche), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** if McKing / `lightning` reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**first** recovery smoke if Soft-530 CLEARs overnight — **before** desk / **#79.1** / unfreeze), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke if vault CLEARs overnight — **before** Bitwarden / desk), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — stamp does **not** lift it), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Complement of **weekday overnight coverage** ([soft-530-weekday-overnight.md](soft-530-weekday-overnight.md)) and **overnight/weekend Option A uncovered** (`c200d71` / [lookout-rearm-sop.md](lookout-rearm-sop.md)). This file names the **one-line overnight baseline**: last weekday Chief plan-improve `*/20` writes it **before** the Lookout-only window. First weekday `*/20` after ~06:00 **diffs** that line instead of rediscovering. **Same-class = stay quiet.** Surface **Lead/Ben only on stamp class DIFF** (Soft-530 / vault / ListMachines / Option A / freeze / Lookout). A true last ~17:40 fire **refreshes the stamp only if any field diffs**; else the prior stamp **stands**.

This fold is **paper only**. Stamp alone ≠ Ben re-nag ≠ Zone / Garage execute ≠ overnight Option A smoke. Overnight **CLEAR** still follows [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [vault-clear-smoke.md](vault-clear-smoke.md) + first-hop cards. This file executes **none** of Zone Direct Upload, Garage, **#82**, unfreeze, companions, Bitwarden, a Ben Doc-wake re-nag, or a second Ben recreate ask. The living ~17:25 one-liner below is a **STATUS pointer / example**, not a live ops action.

---

## When to stamp / when to diff

| Edge | Meaning |
|------|---------|
| **Stamp** | Last weekday plan-improve `*/20` — **~17:40** America/Edmonton (MT). **Refresh only if any field diffs.** Same-class last fire → prior stamp **stands**. |
| **Paper stamp** | Chief may record a living one-liner **before** a true last fire (this fold: **2026-09-14 ~17:25** America/Edmonton). That line is the baseline for tomorrow’s first `*/20` ~06:00. A later true ~17:40 fire overwrites it **only on field DIFF**. Paper stamp ≠ live ops action. |
| **Nights** | **Mon–Thu:** stamp, then [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) Lookout-only gap. **Friday:** stamp, then hand **into weekend coverage** (`84107e7`) — **not** the Mon–Thu overnight card. |
| **Diff** | First weekday `*/20` after **~06:00** America/Edmonton. Compare **stamp class**: Soft-530 / vault / ListMachines / Option A / freeze / Lookout. **Same-class = stay quiet** — do **not** surface Lead or Ben. Surface **Lead/Ben only on class DIFF**. Unchanged class+since → do **not** rediscover. Do **not** Ben-nag from an unchanged OPEN stamp. |
| **Weekend** | Friday stamp is the Monday-morning baseline. Saturday/Sunday plan-improve stays **off**. Do **not** invent weekend `*/20`. |

Quiet-ops may **already** be in force ([soft-530-extended-open.md](soft-530-extended-open.md)). The stamp does **not** lift quiet-ops and does **not** invent a new Ben ask from the clock.

---

## One-line fields

Write **one** line. Do **not** expand into a second essay. Missing known-unknowns stay `unknown` — do **not** invent.

| Field | Stamp |
|-------|-------|
| **Soft-530 class+since** | `OPEN` / `CLEAR` + public class (`530` CF **1033**, or `/health` **200`) + since (America/Edmonton). Include waitlist OPTIONS class if it differs. |
| **vault class+since** | `OPEN` / `CLEAR` + `/alive` **and** `/api/config` class (`502` origin-down, **not** 1033) + since. Vault ≠ Soft-530. |
| **Option A Redirect+UX** | Last weekday `*/20` Redirect **and** Soft-530 UX: `PASS` / `FAIL` + timestamp. **Redirect-only PASS ≠ Soft-530 UX PASS.** Overnight/weekend Dynamic is **UNCOVERED** while `brochure-option-a-redirect-watch` is **GONE** (`c200d71`) — stamp `UNCOVERED` when no last weekday smoke exists. Do **not** invent overnight redirect smoke to fill the field. |
| **ListMachines IDs** | Names **and** machineIds present. **`Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`.** Never treat `Mac.lan` as Doc (`95a229f5-9296-4a18-aa98-70fd300dabdf`) or McKing (`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`). |
| **freeze tip / BUILD_ID** | Git tip + Doc `BUILD_ID` **if known**. Living freeze is **`4cf8924`** / **`5swmVz`**. `unknown` is honest. Stamp ≠ unfreeze. |
| **Lookout watch state** | `projectcar-api-health-watch` + vault `/alive`: **armed** / not. `brochure-option-a-redirect-watch`: **GONE** / **armed**. Api+vault **stay armed**. Do **not** delete them to fix cron ([lookout-rearm-sop.md](lookout-rearm-sop.md)). |

**Template (one line):**

```
STAMP <date> ~17:40 MT | Soft-530 <OPEN|CLEAR> <class> since <when> | vault <OPEN|CLEAR> <class> since <when> | Option A Redirect+UX <PASS|FAIL|UNCOVERED> <ts> | ListMachines <ids> | freeze <tip>/<BUILD_ID|unknown> | Lookout api+vault <armed|…>; brochure-option-a-redirect-watch <GONE|armed>
```

Overwrite the previous stamp **only if any field diffs**. Same-class last `*/20` → prior stamp **stands**. Keep the prior line if a morning diff is still open. This paper is SSOT for the living one-liner until the next last-`*/20` overwrite.

---

## Morning diff (first weekday `*/20` after ~06:00)

Diff **against the stamp**. Do **not** re-walk STATUS as if the night never happened.

**Surfacing lock:** first `*/20` ~06:00 surfaces **Lead/Ben only on stamp class DIFF**. Stamp classes = Soft-530 / vault / ListMachines / Option A / freeze / Lookout. **Same-class = stay quiet** — no Lead page, no Ben page, no rediscover.

| Diff | Do | Do not |
|------|----|--------|
| **Same-class (all six)** | **Stay quiet.** Continue weekday `*/20`. Prior stamp **stands**. | Surface Lead. Surface Ben. Rediscover dual-OPEN. Treat duration as GO. |
| **Same Soft-530 class+since** | Note unchanged. **Stay quiet** on this class. | Re-nag Ben. Rediscover the outage. Treat duration as GO. |
| **Same vault class+since** | Note unchanged. **Stay quiet** on this class. | Re-nag Ben. Bitwarden. Treat 502 duration as rotate. |
| **Soft-530 class changed toward CLEAR** | Surface Lead. [soft-530-clear-smoke.md](soft-530-clear-smoke.md) **first**. If a host reappeared, [doc-reappear-first-hop.md](doc-reappear-first-hop.md) **before** smoke. | Desk / **#79.1** / unfreeze / **#82** from the stamp. Honesty-off. |
| **vault class changed toward CLEAR** | Surface Lead. [vault-clear-smoke.md](vault-clear-smoke.md) **first**. If `lightning` reappeared, [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) **before** smoke. | Bitwarden auto-fire. Treat vault CLEAR as Soft-530 CLEAR / unfreeze / **#82**. |
| **New ListMachines IDs** | Surface Lead. First-hop cards. Assert machineIds. **Never** `Mac.lan` as Doc or McKing. **Never auto-fire.** | Shell `Mac.lan` as evidence. Skip identity. |
| **Freeze tip / BUILD_ID changed** | Surface Lead. Record. Unfreeze is still **Ben GO**. | Pull / rebuild from the stamp. |
| **Lookout Option A still GONE** | Same-class on this field. Weekday `*/20` Redirect+UX resumes. Overnight uncovered **accepted**. | Second Ben recreate ask. Invent overnight smoke retroactively. Surface Ben. |
| **Lookout Option A now armed** | Class DIFF — surface Lead. [lookout-rearm-sop.md](lookout-rearm-sop.md) row 5 — enabled + first fire ≤ **10m** + baseline **LIVE 10/10**. This paper does **not** run that assert. | Companion re-ask. Claim `enabled:true` without Lookout stamp. |
| **Option A Redirect+UX class changed** | Surface Lead on that class. Last-weekday PASS/FAIL is the stamp field — overnight Dynamic stays **UNCOVERED** while watch **GONE**. | Invent overnight redirect smoke. Treat last-weekday PASS as overnight coverage. |

Overnight **CLEAR** still follows the smoke + first-hop cards. The stamp is the **before** line, not the CLEAR receipt.

---

## Living snapshot (this fold)

STATUS pointers stay canonical. Honesty this fold — **Chief paper stamp** America/Edmonton **2026-09-14 ~17:25** (example / STATUS pointer, **not** a live ops action). Tomorrow’s first `*/20` ~06:00 diffs **this** line. A true last ~17:40 fire tonight refreshes it **only if any field diffs**; else this stamp **stands**.

```
STAMP 2026-09-14 ~17:25 MT (paper / Chief) | Soft-530 OPEN api/app/ops/cloud 530/1033 waitlist_OPTIONS 530 since 2026-09-13T11:57 (~29.5h) | vault OPEN /alive 502 /api/config 502 since 2026-09-13T19:45 (~21.7h) | ListMachines Mac.lan only; docs=ABSENT lightning=ABSENT (lid-restore+vault wake blocked) | freeze last_known 4cf8924 / BUILD_ID 5swmVz (Doc absent → unverifiable live) | Option A Redirect PASS 10/10 apex+www; Soft-530 UX LIVE styles.css?v=36 + waitlist.js?v=3 + Discord honesty | Lookout api+vault armed; companions HOLD; brochure-option-a-redirect-watch GONE (overnight Dynamic UNCOVERED = accept) | locks=quiet-ops HOLD; #82 not auto-GO; no Ben re-nag
```

| Surface | Living (~17:25 MT paper) |
|---------|--------------------------|
| **Soft-530** | **OPEN** — `api.` / `app.` / `ops.` / `cloud.` **530** CF **1033** since 2026-09-13T11:57 America/Edmonton (**~29.5h**) |
| **Waitlist OPTIONS** | **530** |
| **Vault** | `/alive` **502** + `/api/config` **502** since 2026-09-13T19:45 America/Edmonton (**~21.7h**; **not** 1033) |
| **ListMachines** | **`Mac.lan` only** — `docs=ABSENT` · `lightning=ABSENT` (lid-restore + vault wake **blocked**). `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning` |
| **Freeze** | **last_known** **`4cf8924`** / BUILD_ID **`5swmVz`** — Doc absent → **unverifiable live** |
| **#82** | Still **Ben GO**. Soft-530 **OPEN ≠ #82 blocked** — this stamp still ≠ auto-GO. Quiet-ops **HOLD**. No Ben re-nag. |
| **Option A Redirect** | Last weekday smoke **PASS 10/10** apex+www. Overnight Dynamic still **UNCOVERED** while watch **GONE** — accept (`c200d71`). Last-weekday PASS ≠ overnight coverage. **Next smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. Do **not** invent overnight redirect smoke. |
| **Soft-530 UX assets** | **Root-relative LIVE** — `/styles.css?v=36` + `/waitlist.js?v=3` + Membership/Contact Discord honesty. UX **LIVE** ≠ overnight redirect smoke. |
| **Lookout** | api+vault **armed**; companions **HOLD**; `brochure-option-a-redirect-watch` **GONE** |

This paper does **not** invent CLEAR, a host reappear, a morning fire, overnight redirect smoke, or a second Ben ask. Last-weekday Redirect **PASS 10/10** is the recorded weekday field — **not** invented overnight smoke.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** Lookout execute, **not** Zone apply, **not** Garage upload. The ~17:25 one-liner is a **STATUS pointer / example**, not a live ops action. |
| **Same-class = stay quiet** | Morning first `*/20` ~06:00 surfaces **Lead/Ben only on stamp class DIFF** (Soft-530 / vault / ListMachines / Option A / freeze / Lookout). Same-class → **no Lead page, no Ben page**. |
| **17:40 refresh only on field DIFF** | A true last weekday `*/20` ~17:40 **overwrites only if any field diffs**. Else the prior stamp **stands**. |
| **No Ben re-nag from stamp alone** | Unchanged OPEN class+since after overnight ≠ a new Ben page. Doc-wake + McKing wake **already asked**. |
| **No Zone / Garage execute** | Stamp ≠ Worker-live ≠ **#79.1** ≠ purge. |
| **CLEAR overnight still smoke + first-hop** | Soft-530 CLEAR → [soft-530-clear-smoke.md](soft-530-clear-smoke.md). Vault CLEAR → [vault-clear-smoke.md](vault-clear-smoke.md). Host reappear → first-hop **then** smoke. Stamp is **not** the CLEAR card. |
| **Never `Mac.lan` as Doc / McKing** | Identity lock unchanged. |
| **Overnight Option A still UNCOVERED** | Last-weekday Redirect **PASS 10/10** ≠ overnight coverage. Do **not** invent overnight redirect smoke so the stamp can say overnight `PASS`. |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **#82 upload** | Stamp ≠ Worker-live. Soft-530 **OPEN ≠ #82 blocked**, but this card is **not** a GO. Quiet-ops **HOLD**. |
| **Companion re-ask** | ops/app companions **HOLD until Ben reopens**. An unchanged overnight stamp ≠ re-ask. |
| **Invent overnight redirect smoke** | Option A Dynamic redirect is **uncovered — accept that risk** (`c200d71`). Last-weekday Redirect **PASS 10/10** is the weekday field, **not** overnight smoke. **Next Option A smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. |
| **Second Ben recreate ask** | [lookout-rearm-sop.md](lookout-rearm-sop.md) already one-ask. A `GONE` stamp ≠ a new Ben page. |
| **Surface Lead/Ben on same-class morning fire** | Same-class = **stay quiet**. Lead/Ben only on Soft-530 / vault / ListMachines / Option A / freeze / Lookout **DIFF**. |
| **Rewrite an unchanged ~17:40 stamp** | True last fire refreshes **only on field DIFF**. Else the prior stamp **stands**. |
| **Ben Doc-wake re-nag** | OPEN duration + stamp persistence ≠ a new Ben page. |
| **Treat Friday night as Mon–Thu overnight** | Friday last `*/20` **stamps**, then **weekend coverage**. |
| **Treat `Mac.lan` as Doc or McKing** | Identity lock unchanged. |
| **Auto-fire on reappear or CLEAR** | First hops, then smoke, then (only if CLEAR) forensics, then the sequencer. **Never auto-fire.** |
| **Drop Lookout api+vault** | Those two watches **are** overnight coverage. **Never delete** them to fix stalled cron. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / quiet-ops (`1e6a0b1`) / weekday overnight (`618e30a`) / Option A overnight uncovered (`c200d71`) / overnight baseline stamp (`56d5d99`) — **unchanged**. This file extends `56d5d99` and executes **none** of those.

---

## Do not

- Re-nag Ben because the stamp still says OPEN after overnight
- Surface Lead or Ben on a **same-class** morning first `*/20` (~06:00)
- Rewrite the stamp at a true last ~17:40 fire when every field matches — prior stamp **stands**
- Schedule overnight Zone Direct Upload / Worker / purge, or overnight Garage execute
- Invent overnight plan-improve / Zone / Garage Option A redirect smoke so the stamp can say overnight `PASS` (last-weekday **PASS 10/10** ≠ overnight coverage)
- Re-ask Ben to recreate Lookout Option A from a `GONE` stamp (`lookout-rearm-sop` already one-ask)
- Arm Soft-530 companions from this paper
- Treat Friday last `*/20` as another Mon–Thu overnight — stamp, then **weekend coverage**
- Shell `Mac.lan` or Porsche as Doc or McKing
- Skip [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [vault-clear-smoke.md](vault-clear-smoke.md) + first-hop cards if a plane CLEARs overnight
- Auto-fire **#82** / unfreeze / **#79.1** / companions / Zone upload / Bitwarden from a stamp diff
- Invent CLEAR while Soft-530 is still **OPEN** (CF **1033**) or vault is still **OPEN** (**502**)
- Drop Lookout `api.` `/health` or vault `/alive` because plan-improve `*/20` is paused
- Rediscover the whole living dual-OPEN on the first weekday `*/20` when the stamp is unchanged

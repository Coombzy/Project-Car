# Overnight baseline stamp — last weekday `*/20` one-liner

**Status:** Living ops — paper lock  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (living Soft-530 CLEAR + vault OPEN **half-state** + this pointer), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (**Mon–Thu nights** after last weekday `*/20` ~17:40 MT until next weekday first fire ~06:00 — Lookout api+vault only; this file is the **pre-gap stamp**, **not** that coverage card), weekend Soft-530 coverage (`84107e7` — Friday last `*/20` stamps **then** hands here; Sat/Sun plan-improve-off), [lookout-rearm-sop.md](lookout-rearm-sop.md) (weekday Chief `*/20` **+ Soft-530 UX**; overnight/weekend Option A Dynamic redirect **UNCOVERED** — `c200d71`; **HOLD** second Ben recreate ask; chronic ≤1 pause/resume per calendar-day, clock resets **America/Edmonton midnight**), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A **paper** continues; continuous watch **GONE**), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**first hop** if Doc reappears — machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`; **never** `Mac.lan` / Porsche; overnight first-hop **absorbs** a ListMachines DIFF so morning `*/20` does **not** re-ask Ben), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** if McKing / `lightning` reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`; living: hop already ran ~19:10 MT Mon 2026-09-14 — still blocked on Ben sudo), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**first** recovery smoke if Soft-530 CLEARs overnight — **before** desk / **#79.1** / unfreeze), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke if vault CLEARs overnight — **before** Bitwarden / desk), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — stamp does **not** lift it; **chronic-HOLD exception:** when both api + vault are calendar-day chronic HOLD, “Lookout continues” is **false for flip detection**; Chronic Lookout ≠ quiet-ops failure ≠ Ben ping), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (**home-off:** Docs **ABSENT** + Soft-530 **OPEN** is **EXPECTED** / **SAME-CLASS** — **not** a morning Ben DIFF; complement to `fb86f90` camp cutover, **not** a re-cutover), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Complement of **weekday overnight coverage** ([soft-530-weekday-overnight.md](soft-530-weekday-overnight.md)) and **overnight/weekend Option A uncovered** (`c200d71` / [lookout-rearm-sop.md](lookout-rearm-sop.md)). This file names the **one-line overnight baseline**: last weekday Chief plan-improve `*/20` writes it **before** the Lookout-only window. First weekday `*/20` after ~06:00 **diffs** that line instead of rediscovering. **Same-class = stay quiet** (`611c267`). Surface **Lead/Ben only on stamp class DIFF** (Soft-530 / vault / ListMachines / Option A / freeze / Lookout). **Home-off expected:** intentional Docs **ABSENT** + Soft-530 **OPEN** at home is **SAME-CLASS expected** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)) — duration of home-off is **not** a Soft-530 class DIFF and does **not** page Ben. **Exception — first-hop absorbed DIFF:** if a ListMachines (or other) class DIFF was **already handled by first-hop** between last weekday `*/20` and morning first `*/20`, morning `*/20` must **not** re-surface that DIFF to Ben when first-hop completed **and** Ben already asked once **and** Soft-530 / vault HTTP class is unchanged — **refresh** the living stamp to current state so later same-day `*/20` stays same-class quiet; optional short **Lead-only** ack (stamp refresh + first-hop pointer). **Freeze / `BUILD_ID` / `changeme` in this stamp are `last_known` from the last Soft-530 CLEAR only.** While Soft-530 is **OPEN** (**530** / CF **1033**), `app.` + `ops.` `/login` **cannot be live-probed** — morning first `*/20` must **NOT** treat “couldn’t verify freeze tip / `changeme` / `BUILD_ID`” as a freeze class DIFF. Freeze live-verify is deferred to [soft-530-clear-smoke.md](soft-530-clear-smoke.md). Stamp still records last_known tip hashes for continuity. A true last ~17:40 fire **refreshes the stamp only if any field diffs**; else the prior stamp **stands**. True-last `*/20` **~17:42** MT Mon 2026-09-14 was **SAME-CLASS** vs the ~17:25 stamp — **do NOT refresh that last-weekday line**. Overnight `lightning` DIFF ~19:06 / ~19:10 **was** a ListMachines DIFF — first-hop absorbed it; morning refreshes the **living** stamp (below).

This fold is **paper only**. Stamp alone ≠ Ben re-nag ≠ Zone / Garage execute ≠ overnight Option A smoke. Overnight **CLEAR** still follows [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [vault-clear-smoke.md](vault-clear-smoke.md) + first-hop cards. This file executes **none** of Zone Direct Upload, Garage, **#82**, unfreeze, companions, Bitwarden, a Ben Doc-wake / docker / recreate re-nag, or a second Ben ask. The ~17:25 last-weekday one-liner is historical (SAME-CLASS at ~17:42). The **living** stamp below is the **morning refresh** after first-hop absorb — a **STATUS pointer / example**, not a live ops action.

---

## When to stamp / when to diff

| Edge | Meaning |
|------|---------|
| **Stamp** | Last weekday plan-improve `*/20` — **~17:40** America/Edmonton (MT). **Refresh only if any field diffs.** Same-class last fire → prior stamp **stands**. |
| **Paper stamp** | Chief may record a living one-liner **before** a true last fire (this fold: **2026-09-14 ~17:25** America/Edmonton). That line is the baseline for tomorrow’s first `*/20` ~06:00. A later true ~17:40 fire overwrites it **only on field DIFF**. True-last `*/20` **~17:42** MT Mon 2026-09-14 was **SAME-CLASS** vs this stamp — **do NOT refresh**. Paper stamp ≠ live ops action. |
| **Nights** | **Mon–Thu:** stamp, then [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) Lookout-only gap. **Friday:** stamp, then hand **into weekend coverage** (`84107e7`) — **not** the Mon–Thu overnight card. |
| **Diff** | First weekday `*/20` after **~06:00** America/Edmonton. Compare **stamp class**: Soft-530 / vault / ListMachines / Option A / freeze / Lookout. **Same-class = stay quiet** (`611c267`) — do **not** surface Lead or Ben. Surface **Lead/Ben only on class DIFF**. **Couldn’t verify freeze tip / `changeme` / `BUILD_ID` while Soft-530 is OPEN (530/1033) is NOT a freeze class DIFF** — those fields stay `last_known` from the last Soft-530 CLEAR; live-verify waits on [soft-530-clear-smoke.md](soft-530-clear-smoke.md). Unchanged class+since → do **not** rediscover. Do **not** Ben-nag from an unchanged OPEN stamp. |
| **First-hop absorbed DIFF** | A ListMachines (or other) class DIFF **handled by first-hop** between last weekday `*/20` and morning first `*/20`. Morning `*/20` must: (1) **not** re-surface that DIFF to Ben if first-hop completed **and** Ben already asked once **and** Soft-530 / vault HTTP class is unchanged; (2) **refresh** the living stamp to current state so later same-day `*/20` is same-class quiet; (3) optional short **Lead-only** ack (stamp refresh + [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) / [doc-reappear-first-hop.md](doc-reappear-first-hop.md) pointer). **Not** a Ben page. Living: `lightning` DIFF ~19:06 / ~19:10 MT Mon 2026-09-14 — hop ran; vault still **OPEN 502** (docker dead); Soft-530 still **OPEN 1033**; Docs **ABSENT**; still blocked on Ben sudo — **no morning re-ask**. |
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
| **freeze tip / BUILD_ID / changeme** | **`last_known` from the last Soft-530 CLEAR only.** Living last_known is **`4cf8924`** / BUILD_ID **`5swmVz`** + public `/login` still prints `` `changeme` `` (last CLEAR evidence). While Soft-530 is **OPEN** (**530** / CF **1033**), `app.` + `ops.` `/login` **cannot be live-probed** — do **not** curl those pages to “refresh” this field. Stamp still **records** last_known hashes for continuity. Live-verify is deferred to [soft-530-clear-smoke.md](soft-530-clear-smoke.md). `unknown` is honest if no last-CLEAR hashes exist. Stamp ≠ unfreeze. |
| **Lookout watch state** | `projectcar-api-health-watch` + vault `/alive`: **armed** / **chronic HOLD** (`enabled:true` but cron-dead after the day's **1×** re-arm) / not. `brochure-option-a-redirect-watch`: **GONE** / **armed**. Api+vault **stay armed** even on chronic HOLD. Do **not** delete them to fix cron ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Chronic HOLD ≠ Ben ping ([soft-530-extended-open.md](soft-530-extended-open.md) exception). |

**Template (one line):**

```
STAMP <date> ~17:40 MT | Soft-530 <OPEN|CLEAR> <class> since <when> | vault <OPEN|CLEAR> <class> since <when> | Option A Redirect+UX <PASS|FAIL|UNCOVERED> <ts> | ListMachines <ids> | freeze last_known <tip>/<BUILD_ID|unknown> | Lookout api+vault <armed|…>; brochure-option-a-redirect-watch <GONE|armed>
```

Overwrite the previous stamp **only if any field diffs**. Same-class last `*/20` → prior stamp **stands**. Keep the prior line if a morning diff is still open. This paper is SSOT for the living one-liner until the next last-`*/20` overwrite.

---

## Morning diff (first weekday `*/20` after ~06:00)

Diff **against the stamp**. Do **not** re-walk STATUS as if the night never happened.

**Surfacing lock:** first `*/20` ~06:00 surfaces **Lead/Ben only on stamp class DIFF**. Stamp classes = Soft-530 / vault / ListMachines / Option A / freeze / Lookout. **Same-class = stay quiet** (`611c267`) — no Lead page, no Ben page, no rediscover. **First-hop absorbed DIFF** (overnight first-hop already completed + Ben already asked once + Soft-530 / vault HTTP class unchanged) is **not** a morning Ben page — **refresh the stamp**, optional Lead-only ack. Freeze class DIFF applies **only** after Soft-530 **CLEAR** + [soft-530-clear-smoke.md](soft-530-clear-smoke.md) live-verify. **Couldn’t verify freeze tip / `changeme` / `BUILD_ID` while Soft-530 is OPEN (530/1033) is NOT a freeze class DIFF.**

| Diff | Do | Do not |
|------|----|--------|
| **Same-class (all six)** | **Stay quiet.** Continue weekday `*/20`. Prior stamp **stands**. | Surface Lead. Surface Ben. Rediscover dual-OPEN. Treat duration as GO. |
| **Same Soft-530 class+since** | Note unchanged. **Stay quiet** on this class. | Re-nag Ben. Rediscover the outage. Treat duration as GO. |
| **Home-off Soft-530 OPEN + Docs ABSENT** (intentional) | **SAME-CLASS expected** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). Prior stamp **stands**. Quiet-ops **HOLD**. Lookout Soft-530 `ok=false` while Docs **ABSENT** is **expected baseline**, not a Lookout DIFF. | Surface Ben. Treat multi-day home-off as Soft-530 DIFF. Queue lid-restore / KeepAlive. Treat home 1033 as camp cutover failure. Re-arm Soft-530 companions. |
| **Same vault class+since** | Note unchanged. **Stay quiet** on this class. | Re-nag Ben. Bitwarden. Treat 502 duration as rotate. Treat docker-dead 502 as a new Ben sudo page. |
| **Soft-530 class changed toward CLEAR** | Surface Lead. [soft-530-clear-smoke.md](soft-530-clear-smoke.md) **first**. If a host reappeared, [doc-reappear-first-hop.md](doc-reappear-first-hop.md) **before** smoke. | Desk / **#79.1** / unfreeze / **#82** from the stamp. Honesty-off. |
| **vault class changed toward CLEAR** | Surface Lead. [vault-clear-smoke.md](vault-clear-smoke.md) **first**. If `lightning` reappeared, [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) **before** smoke. | Bitwarden auto-fire. Treat vault CLEAR as Soft-530 CLEAR / unfreeze / **#82**. |
| **New ListMachines IDs** (first-hop **not** yet run) | Surface Lead. First-hop cards. Assert machineIds. **Never** `Mac.lan` as Doc or McKing. **Never auto-fire.** | Shell `Mac.lan` as evidence. Skip identity. |
| **New ListMachines IDs — first-hop already completed overnight** | **Do not re-surface to Ben.** Refresh living stamp to current IDs. Optional short **Lead-only** ack (stamp refresh + first-hop pointer). Later same-day `*/20` = same-class quiet (`611c267`). | Re-ask Ben sudo / docker / Doc-wake. Rediscover the overnight DIFF. Leave the stale last-weekday stamp so morning keeps paging. |
| **`Mac.lan` flap (Ben laptop) + HTTP unchanged** | Living vs ~12:45: `Mac.lan` flap **reappeared** (after the ~12:24 drop); **`Mac.lan` + `lightning`**; Docs still **ABSENT**. Soft-530 still **1033**; vault still **502**. **Refresh** the living stamp. **No Ben surface.** | Treat laptop flap as Doc-wake or McKing wake. Page Ben. Fold it into Soft-530 / vault HTTP class. |
| **Couldn't verify freeze tip / changeme / BUILD_ID** (Soft-530 still **OPEN** 530/1033) | **Not a class DIFF.** last_known stands. Stay quiet. Live-verify waits on [soft-530-clear-smoke.md](soft-530-clear-smoke.md). | Surface Lead/Ben. Treat unverifiable as freeze change. Curl `app.`/`ops.` `/login` while OPEN. Refresh last_known. |
| **Soft-530 CLEAR + vault still OPEN** (half-state) | **Soft-530 class DIFF toward CLEAR** — stamp Soft-530 **CLEAR**. Vault class **unchanged OPEN 502**. **Do not** enter [post-dual-clear-go.md](post-dual-clear-go.md). Freeze live-verify **now allowed**; last_known **`4cf8924` / `5swmVz` still unverified**. Lookout api `ok=true` / vault `ok=false` **expected**. | Treat as dual CLEAR. Camp GO. **#82** / unfreeze / Bitwarden. Page Ben. |
| **Freeze tip / BUILD_ID / changeme changed** (only after Soft-530 **CLEAR** + [soft-530-clear-smoke.md](soft-530-clear-smoke.md) live-verify) | Surface Lead. Record. Unfreeze is still **Ben GO**. | Pull / rebuild from the stamp. Treat OPEN unverifiable as this DIFF. |
| **Lookout Option A still GONE** | Same-class on this field. Weekday `*/20` Redirect+UX resumes. Overnight uncovered **accepted**. | Second Ben recreate ask. Invent overnight smoke retroactively. Surface Ben. |
| **Lookout Option A now armed** | Class DIFF — surface Lead. [lookout-rearm-sop.md](lookout-rearm-sop.md) row 5 — enabled + first fire ≤ **10m** + baseline **LIVE 10/10**. This paper does **not** run that assert. | Companion re-ask. Claim `enabled:true` without Lookout stamp. |
| **Lookout api+vault still chronic HOLD** | Same-class on this field. Quiet-ops “Lookout continues” stays **false for flip detection**. Interim = Chief `*/20` + Lead probes (accept **≤~20m**). **Stay quiet** on Ben. | Ben recreate / docker / Doc-wake. Treat as quiet-ops failure. Loop pause/resume. |
| **Lookout api+vault flipped to/from chronic HOLD** | Lookout class DIFF — **Lead only** (not Ben). Stamp the new state. Next local day after **America/Edmonton midnight** Lead **may** try **one** in-place re-arm, then stickiness ≥3 `*/5` ([lookout-rearm-sop.md](lookout-rearm-sop.md) row 8). | Ben recreate. Companion / brochure re-ask. Zone / Garage execute. |
| **Option A Redirect+UX class changed** | Surface Lead on that class. Last-weekday PASS/FAIL is the stamp field — overnight Dynamic stays **UNCOVERED** while watch **GONE**. | Invent overnight redirect smoke. Treat last-weekday PASS as overnight coverage. |

Overnight **CLEAR** still follows the smoke + first-hop cards. The stamp is the **before** line, not the CLEAR receipt.

---

## Living snapshot (this fold)

STATUS pointers stay canonical. Honesty this fold — **two lines**:

1. **Last-weekday paper stamp** America/Edmonton **2026-09-14 ~17:25** (historical). True-last `*/20` **~17:42** MT Mon 2026-09-14 was **SAME-CLASS** vs that line — **do NOT rewrite the last-weekday stamp**.
2. **Living morning-refresh stamp** after first-hop absorb (STATUS pointer / example, **not** a live ops action). Overnight `lightning` DIFF ~19:06 / ~19:10 MT Mon 2026-09-14 was handled by [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md). That absorb + ~12:24 / ~12:45 `Mac.lan` flap lines stay **historical**. **This fold living stamp** (below) supersedes those HTTP / ListMachines classes: Soft-530 **CLEAR** + vault **OPEN 502** + **Docs + lightning + Mac.lan CONNECTED** (home-awake pre-camp **half-state**). Morning first `*/20` **must not** re-surface an already-absorbed DIFF to Ben. Vault still **OPEN 502** (docker dead) — **not** CLEAR. Soft-530 **CLEAR ≠** dual CLEAR ≠ camp GO. Quiet-ops **HOLD** for vault / Ben re-nag. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md) until vault CLEAR.

**Last-weekday (historical — SAME-CLASS at ~17:42 — do not rewrite):**

```
STAMP 2026-09-14 ~17:25 MT (paper / Chief) | Soft-530 OPEN api/app/ops/cloud 530/1033 waitlist_OPTIONS 530 since 2026-09-13T11:57 | vault OPEN /alive 502 /api/config 502 since 2026-09-13T19:45 | ListMachines Mac.lan only; docs=ABSENT lightning=ABSENT (lid-restore+vault wake blocked) | freeze last_known 4cf8924 / BUILD_ID 5swmVz / changeme (last Soft-530 CLEAR only; Soft-530 OPEN 530/1033 → unverifiable live — not a DIFF) | Option A Redirect PASS 10/10 apex+www; Soft-530 UX LIVE styles.css?v=36 + waitlist.js?v=3 + Discord honesty | Lookout api+vault armed; companions HOLD; brochure-option-a-redirect-watch GONE (overnight Dynamic UNCOVERED = accept) | locks=quiet-ops HOLD; #82 not auto-GO; no Ben re-nag
```

**Living (morning refresh after first-hop absorb — later `*/20` same-class quiet):**

```
STAMP 2026-09-15 ~12:24 refresh (paper / Mac.lan drop — historical) | Soft-530 OPEN api/app/ops/cloud 530/1033 waitlist_OPTIONS 530 since 2026-09-13T11:57 | vault OPEN /alive 502 /api/config 502 since 2026-09-13T19:45 (docker dead — not CLEAR) | ListMachines lightning CONNECTED only; Mac.lan dropped vs ~12:24; docs=ABSENT (McKing first-hop ran ~19:10 MT Mon 2026-09-14; still blocked on Ben sudo; HTTP class unchanged — no Ben surface) | freeze last_known 4cf8924 / BUILD_ID 5swmVz / changeme (last Soft-530 CLEAR only; Soft-530 OPEN 530/1033 → unverifiable live — not a DIFF) | Option A Redirect PASS 10/10 apex+www; Soft-530 UX LIVE styles.css?v=36 + waitlist.js?v=3 + Discord honesty | Lookout api+vault chronic HOLD today (enabled:true + cron-dead after 1×; flip detection false); companions HOLD; brochure-option-a-redirect-watch GONE (overnight Dynamic UNCOVERED = accept) | locks=quiet-ops HOLD; Chronic Lookout ≠ quiet-ops failure ≠ Ben ping; #82 still Ben GO; no Ben re-nag
```

**Living (this fold — Soft-530 CLEAR + vault OPEN half-state; Docs + lightning + Mac.lan CONNECTED):**

```
STAMP 2026-09-15 half-state refresh (paper / Soft-530 CLEAR + vault OPEN) | Soft-530 CLEAR api/health 200; waitlist_OPTIONS = Origin CORS preflight (bare 405 ≠ OPEN) | vault OPEN /alive 502 /api/config 502 since 2026-09-13T19:45 (docker dead — not CLEAR) | ListMachines Docs + lightning + Mac.lan CONNECTED (Mac.lan ≠ Docs ≠ lightning; home-awake pre-camp half-state — not camp GO) | freeze last_known 4cf8924 / BUILD_ID 5swmVz / changeme (live-verify NOW ALLOWED after Soft-530 CLEAR; still unverified — not a DIFF) | Option A Redirect PASS 10/10 apex+www; Soft-530 UX LIVE styles.css?v=36 + waitlist.js?v=3 + Discord honesty (rungs 1–2 — ≠ Worker body freshness / #82; Home still STALE bare / canonical+og+nav+sitemap lastmod 2026-09-08) | Lookout api ok=true expected; vault ok=false expected (half-state); companions HOLD; brochure-option-a-redirect-watch GONE | locks=half-state ≠ dual CLEAR; do not enter post-dual-clear-go until vault CLEAR; Soft-530 CLEAR ≠ #82 ≠ unfreeze ≠ Bitwarden ≠ camp GO; Redirect+UX PASS ≠ #82; no Ben re-nag; Zone vault. checklist paper only — no live execute
```

| Surface | Living (Soft-530 CLEAR + vault OPEN half-state) |
|---------|--------------------------|
| **Soft-530** | **CLEAR** — `api.` `/health` **200** |
| **Waitlist OPTIONS** | **Origin CORS preflight** (apex + www). **Bare 405 ≠ Soft-530 OPEN.** |
| **Vault** | `/alive` **502** + `/api/config` **502** since 2026-09-13 ~19:45 America/Edmonton (**not** 1033; docker dead — **not** CLEAR) |
| **ListMachines** | **Docs + lightning + Mac.lan CONNECTED**. `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`. Home-awake pre-camp **half-state** — **not** camp GO, **not** a Ben surface. |
| **Freeze** | **last_known** **`4cf8924`** / BUILD_ID **`5swmVz`** / `` `changeme` `` — live-verify **now allowed** after Soft-530 CLEAR; still **unverified** — **not** a morning DIFF |
| **True-last weekday `*/20`** | **~17:42** MT Mon 2026-09-14 **SAME-CLASS** vs ~17:25 — **do NOT rewrite that last-weekday line**. Overnight `lightning` DIFF is a **separate** absorb → living refresh. |
| **Overnight first-hop** | `lightning` DIFF ~19:06 / ~19:10 absorbed by [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md). Vault HTTP class **unchanged** (still **502**). Soft-530 later flipped to **CLEAR** — that is the living half-state stamp, **not** a morning Ben re-page of the overnight hop. |
| **#82** | Still **Ben GO**. Soft-530 **CLEAR ≠ #82**. Soft-530 **OPEN ≠ #82 blocked**. Half-state ≠ auto-GO. No Ben re-nag. |
| **Option A Redirect** | Last weekday smoke **PASS 10/10** apex+www. Overnight Dynamic still **UNCOVERED** while watch **GONE** — accept (`c200d71`). Last-weekday PASS ≠ overnight coverage. **Next smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. Do **not** invent overnight redirect smoke. |
| **Soft-530 UX assets** | **Root-relative LIVE** — `/styles.css?v=36` + `/waitlist.js?v=3` + Membership/Contact Discord honesty. UX **LIVE** ≠ overnight redirect smoke. |
| **Lookout** | api+vault **chronic HOLD today** (`enabled:true` + cron-dead after the day's 1×); companions **HOLD**; `brochure-option-a-redirect-watch` **GONE**. Quiet-ops “Lookout continues” is **false for flip detection** ([soft-530-extended-open.md](soft-530-extended-open.md)). **Chronic Lookout ≠ quiet-ops failure ≠ Ben ping.** |

This paper does **not** invent vault CLEAR / dual CLEAR, overnight redirect smoke, a second Ben sudo / docker / Doc-wake / recreate ask, or a morning Ben re-page of an already-hopped ListMachines DIFF. Last-weekday Redirect **PASS 10/10** is the recorded weekday field — **not** invented overnight smoke.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** Lookout execute, **not** Zone apply, **not** Garage upload. The ~17:25 last-weekday line is historical. The living morning-refresh stamp is a **STATUS pointer / example**, not a live ops action. ~17:42 same-class honesty is paper — **not** a last-weekday stamp rewrite. |
| **Same-class = stay quiet** | Morning first `*/20` ~06:00 surfaces **Lead/Ben only on stamp class DIFF** (Soft-530 / vault / ListMachines / Option A / freeze / Lookout). Same-class → **no Lead page, no Ben page** (`611c267`). **Couldn’t verify freeze tip / `changeme` / `BUILD_ID` while Soft-530 is OPEN is NOT a freeze DIFF.** |
| **Home-off Soft-530 = SAME-CLASS expected** | Intentional Docs **ABSENT** + Soft-530 **OPEN** at home is **not** a stamp class DIFF ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). Duration / another overnight / another weekday `*/20` does **not** page Ben. Vault may stay McKing **OPEN** or **CLEAR** independently. Lookout Soft-530 `ok=false` while Docs **ABSENT** is **expected baseline**, not stickiness panic. |
| **First-hop absorbed DIFF** | Overnight first-hop completed + Ben already asked once + Soft-530 / vault HTTP class unchanged → morning `*/20` **must not** re-surface that DIFF to Ben. **Refresh** the living stamp. Optional **Lead-only** ack (stamp refresh + first-hop pointer). Cross-link [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) / [doc-reappear-first-hop.md](doc-reappear-first-hop.md). Historical absorb: `lightning` ~19:06 / ~19:10 — hop ran; still blocked on Ben sudo; vault still **502** (docker dead). **This fold living:** Soft-530 **CLEAR** + vault **OPEN 502** + **Docs + lightning + Mac.lan CONNECTED** — half-state, **not** a morning Ben re-page of that hop. **`Mac.lan` flap vs ~12:45** (after the ~12:24 drop; Ben laptop) with HTTP unchanged was the same lock — refresh stamp, **not a Ben surface**. |
| **Freeze last_known while Soft-530 OPEN** | Freeze / `BUILD_ID` / `changeme` are **`last_known` from the last Soft-530 CLEAR only**. While OPEN (**530** / CF **1033**), `app.`+`ops.` `/login` cannot be live-probed. Morning first `*/20` **must not** treat “couldn’t verify freeze tip / changeme / BUILD_ID” as a stamp class DIFF. Live-verify waits on [soft-530-clear-smoke.md](soft-530-clear-smoke.md). Stamp still records last_known hashes. |
| **~17:42 SAME-CLASS** | True-last `*/20` ~17:42 MT Mon 2026-09-14 matched the ~17:25 stamp. That **last-weekday** line **stands**. Do **not** rewrite it. Overnight first-hop absorb refreshes the **living** stamp only — different lock. |
| **17:40 refresh only on field DIFF** | A true last weekday `*/20` ~17:40 **overwrites only if any field diffs**. Else the prior last-weekday stamp **stands**. ~17:42 was SAME-CLASS — last-weekday stamp **stands**. |
| **No Ben re-nag from stamp alone** | Unchanged OPEN class+since after overnight ≠ a new Ben page. Doc-wake + McKing wake **already asked**. First-hop absorbed ListMachines DIFF ≠ a morning Ben sudo / docker / Doc-wake re-ask. |
| **No Zone / Garage execute** | Stamp ≠ Worker-live ≠ **#79.1** ≠ purge. |
| **CLEAR overnight still smoke + first-hop** | Soft-530 CLEAR → [soft-530-clear-smoke.md](soft-530-clear-smoke.md). Vault CLEAR → [vault-clear-smoke.md](vault-clear-smoke.md). Host reappear → first-hop **then** smoke. Stamp is **not** the CLEAR card. |
| **Never `Mac.lan` as Doc / McKing** | Identity lock unchanged. |
| **Overnight Option A still UNCOVERED** | Last-weekday Redirect **PASS 10/10** ≠ overnight coverage. Do **not** invent overnight redirect smoke so the stamp can say overnight `PASS`. |
| **Chronic HOLD ≠ Ben ping** | Lookout api+vault **chronic HOLD** (`enabled:true` + cron-dead after the day's 1×) is **not** a Ben recreate / docker / Doc-wake page. Quiet-ops “Lookout continues” is **false for flip detection** — interim Chief `*/20` + Lead probes (accept **≤~20m**). **Chronic Lookout ≠ quiet-ops failure.** Clock resets **America/Edmonton midnight**. Cross-link [soft-530-extended-open.md](soft-530-extended-open.md) · [lookout-rearm-sop.md](lookout-rearm-sop.md). |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **#82 upload** | Stamp ≠ Worker-live. Soft-530 **OPEN ≠ #82 blocked**, but this card is **not** a GO. Quiet-ops **HOLD**. |
| **Companion re-ask** | ops/app companions **HOLD until Ben reopens**. An unchanged overnight stamp ≠ re-ask. |
| **Invent overnight redirect smoke** | Option A Dynamic redirect is **uncovered — accept that risk** (`c200d71`). Last-weekday Redirect **PASS 10/10** is the weekday field, **not** overnight smoke. **Next Option A smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. |
| **Second Ben recreate ask** | [lookout-rearm-sop.md](lookout-rearm-sop.md) already one-ask. A `GONE` stamp ≠ a new Ben page. |
| **Surface Lead/Ben on same-class morning fire** | Same-class = **stay quiet** (`611c267`). Lead/Ben only on Soft-530 / vault / ListMachines / Option A / freeze / Lookout **DIFF**. |
| **Re-surface a first-hop-absorbed DIFF to Ben** | Overnight first-hop completed + Ben already asked once + Soft-530 / vault HTTP class unchanged → **no morning Ben page**. Refresh the living stamp. Optional Lead-only ack. |
| **Second Ben recreate / docker / Doc-wake re-nag** | McKing first-hop already ran ~19:10; still blocked on Ben sudo. Vault still **502** (docker dead) ≠ a new Ben docker page. Docs **ABSENT** ≠ a new Doc-wake page. Recreate already one-ask. |
| **Treat unverifiable freeze as DIFF** | Soft-530 **OPEN** 530/1033 → `app.`/`ops.` `/login` cannot be live-probed. “Couldn’t verify freeze tip / changeme / BUILD_ID” is **not** a freeze class DIFF. Live-verify waits on [soft-530-clear-smoke.md](soft-530-clear-smoke.md). |
| **Refresh the ~17:25 last-weekday stamp after ~17:42** | True-last `*/20` ~17:42 MT Mon 2026-09-14 was **SAME-CLASS**. That last-weekday line **stands**. Living refresh after first-hop absorb is a **different** line. |
| **Rewrite an unchanged ~17:40 stamp** | True last fire refreshes **only on field DIFF**. Else the prior stamp **stands**. |
| **Ben Doc-wake re-nag** | OPEN duration + stamp persistence ≠ a new Ben page. |
| **Home-off Soft-530 as stamp DIFF / camp failure** | Intentional Docs **ABSENT** + Soft-530 **OPEN** at home is **SAME-CLASS expected** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). Not a morning Ben page. Not camp cutover failure. Not companion re-arm. |
| **Treat Friday night as Mon–Thu overnight** | Friday last `*/20` **stamps**, then **weekend coverage**. |
| **Treat `Mac.lan` as Doc or McKing** | Identity lock unchanged. |
| **Auto-fire on reappear or CLEAR** | First hops, then smoke, then (only if CLEAR) forensics, then the sequencer. **Never auto-fire.** |
| **Drop Lookout api+vault** | Those two watches **are** overnight coverage. **Never delete** them to fix stalled cron. |
| **Treat chronic HOLD as quiet-ops failure / Ben ping** | Living: both watches **chronic HOLD today**. Interim = Chief `*/20` + Lead probes. Does **not** reopen Ben recreate. Clock resets America/Edmonton midnight. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / quiet-ops (`1e6a0b1`) / weekday overnight (`618e30a`) / Option A overnight uncovered (`c200d71`) / overnight baseline stamp (`56d5d99`) / same-class quiet (`611c267`) / freeze last_known (`c1e548e`) — **unchanged**. This file extends `611c267` / `c1e548e` and executes **none** of those.

---

## Do not

- Re-nag Ben because the stamp still says OPEN after overnight
- Treat intentional home Soft-530 **OPEN** + Docs **ABSENT** as a stamp class DIFF or camp cutover failure ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md))
- Surface Ben from `Mac.lan` flap vs ~12:45 (or the earlier ~12:24 drop) when Docs stay **ABSENT** and Soft-530 / vault HTTP class is unchanged
- Surface Ben from Lookout Soft-530 `ok=false` while Docs **ABSENT** at home (expected baseline)
- Re-arm Soft-530 companions from home-off `ok=false`
- Re-surface a first-hop-absorbed ListMachines (or other) DIFF to Ben on morning first `*/20`
- Re-ask Ben sudo / docker / Doc-wake / Lookout recreate because `lightning` is back and vault is still **502**
- Leave the living stamp stale after overnight first-hop so later same-day `*/20` re-pages the same DIFF
- Surface Lead or Ben on a **same-class** morning first `*/20` (~06:00)
- Treat “couldn’t verify freeze tip / changeme / BUILD_ID” while Soft-530 is **OPEN** (530/1033) as a stamp class DIFF
- Curl `app.` / `ops.` `/login` while Soft-530 is OPEN to “refresh” last_known freeze hashes
- Rewrite the ~17:25 stamp after the **SAME-CLASS** true-last `*/20` ~17:42 MT Mon 2026-09-14
- Rewrite the stamp at a true last ~17:40 fire when every field matches — prior stamp **stands**
- Schedule overnight Zone Direct Upload / Worker / purge, or overnight Garage execute
- Invent overnight plan-improve / Zone / Garage Option A redirect smoke so the stamp can say overnight `PASS` (last-weekday **PASS 10/10** ≠ overnight coverage)
- Re-ask Ben to recreate Lookout Option A from a `GONE` stamp (`lookout-rearm-sop` already one-ask)
- Re-ask Ben to recreate api or vault watches because the stamp says **chronic HOLD**
- Treat calendar-day chronic HOLD as quiet-ops failure, or as a Ben ping
- Arm Soft-530 companions from this paper
- Treat Friday last `*/20` as another Mon–Thu overnight — stamp, then **weekend coverage**
- Shell `Mac.lan` or Porsche as Doc or McKing
- Skip [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [vault-clear-smoke.md](vault-clear-smoke.md) + first-hop cards if a plane CLEARs overnight
- Auto-fire **#82** / unfreeze / **#79.1** / companions / Zone upload / Bitwarden from a stamp diff
- Invent vault CLEAR, or treat Soft-530 **CLEAR** + vault **OPEN** as dual CLEAR / camp GO / **#82** / unfreeze / Bitwarden
- Enter [post-dual-clear-go.md](post-dual-clear-go.md) before vault CLEAR
- Treat a bare waitlist OPTIONS **405** as Soft-530 **OPEN**
- Drop Lookout `api.` `/health` or vault `/alive` because plan-improve `*/20` is paused
- Rediscover dual-OPEN or invent dual CLEAR on the first weekday `*/20` when the living stamp is the half-state

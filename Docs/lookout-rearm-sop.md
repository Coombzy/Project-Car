# Lookout rearm SOP — never delete to fix cron

**Status:** Paper SOP — living incident **HOLD**  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (this pointer + Lookout rows + **#78 LIVE-SUPERSEDED** honesty), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A watch **spec** — living watch is **GONE**; weekday `*/20` **+ Soft-530 UX**; overnight/weekend Dynamic redirect **UNCOVERED**; **Redirect-only PASS ≠ Soft-530 UX PASS**), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — Lookout api+vault **continue** = stay **armed and sticky**, not just `enabled:true`; **chronic-HOLD exception:** when **both** are calendar-day chronic HOLD, “Lookout continues” is **false for flip detection**; Chronic Lookout ≠ quiet-ops failure ≠ Ben ping; brochure continuous watch **does not**), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (Mon–Thu after last `*/20` ~17:40 MT — Option A Dynamic redirect **UNCOVERED**; Lookout api+vault stay armed; Friday last `*/20` → weekend coverage), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (last weekday `*/20` one-liner before Lookout-only — **refresh only on field DIFF**; first weekday `*/20` after ~06:00 diffs — **same-class = stay quiet** (`611c267`); surface **Lead/Ben only on stamp class DIFF**; **first-hop absorbed DIFF** → no Ben re-surface + refresh living stamp; freeze/`BUILD_ID`/`changeme` = **`last_known` from last Soft-530 CLEAR only** — OPEN unverifiable ≠ freeze DIFF; ~17:42 SAME-CLASS vs ~17:25 — last-weekday stands; living = Mac.lan+lightning / Docs ABSENT; Lookout field may be **armed** **or** **chronic HOLD**; no rediscover / no Ben re-nag from stamp alone), weekend Soft-530 coverage (`84107e7` — Sat/Sun plan-improve-off; STATUS Live / Locks + [api-stay-up.md](api-stay-up.md) / [doc-lid-restore.md](doc-lid-restore.md) / [vault-stay-up.md](vault-stay-up.md) / [shop-web-stay-up.md](shop-web-stay-up.md) — same Option A **UNCOVERED**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**CLEAR ≠ honesty-off** `0705b37`), [brochure-worker-ci.md](brochure-worker-ci.md) (frozen Redirect inventory SSOT), `api-stay-up.md` (**#78 lookout-resume** is **LIVE-SUPERSEDED** — api-health already `enabled:true`; **can still cron-stall** — same class as vault; remaining **OK-ish** is **not** living contrast this fold), `vault-stay-up.md` (vault `/alive` **LIVE/armed** — **Lookout stall ≠ vault HTTP flip**; **re-arm success ≠ first fire**; docker permanence already `367172d` — **not** this fold), `shop-web-stay-up.md` (Soft-530 companions **HOLD / not armed**)

**Never delete** an armed Project Car Lookout watch to fix a stalled cron. This file names that lock and the living Option A gap.

This fold is **paper only**. It does **not** arm, recreate, pause, or mutate Lookout. It does **not** execute Zone or Garage. It does **not** re-ask companions. It is **not** **#78** lookout-resume.

---

## Living incident (2026-09-14)

`brochure-option-a-redirect-watch` was **deleted** to fix a stalled cron. Recreate then needed **Auto-review**. Auto-review **blocked** recreate. The watch is **GONE**.

Soft-530 companion watches stay **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask). This incident ≠ those companions.

Paper spec name in [brochure-redirect-watch.md](brochure-redirect-watch.md) is `projectcar-brochure-redirect-watch`. The deleted living name is `brochure-option-a-redirect-watch`. Either name: **no** armed Option A flip watch exists now. Do **not** invent `enabled:true`.

**#78 lookout-resume honesty (do not collapse):** **#78** is **LIVE-SUPERSEDED**. `projectcar-api-health-watch` is already **`enabled:true`** (resume 2026-09-11 ~06:52 America/Edmonton) while Doc stays frozen at `4cf8924` / `5swmVz`. Vault `/alive` is a **separate LIVE/armed** watch. This SOP is **not** a re-run of **#78**. Deleting api-health or vault to “fix cron” is the same anti-goal as deleting the brochure watch. Recreating Option A is **not** “resume Lookout.” `enabled:true` on vault **does not** prove the `*/5` is firing — stall class below.

---

## Living class (2026-09-15) — Lookout stall ≠ vault HTTP flip

`projectcar-vault-health-watch` can be **`enabled:true` but cron-stalled**. Example: ~**104m** since last fire; `lastRun` / baseline stuck ~**07:05** on a `*/5`. That is a **separate coverage class** from vault **OPEN 502**.

| Class | What it is | What it is not |
|-------|------------|----------------|
| **Vault OPEN 502** | McKing origin / HTTP class — [vault-stay-up.md](vault-stay-up.md) triage. Living: **502** since ~19:45 MT Sep 13. Docker permanence on CLEAR already landed `@367172d` — **do not redo** that tip here. | A stalled Lookout schedule. A missing watch. |
| **Lookout stall** | Flip watch exists and stays `enabled:true`, but cron is not firing (`lastRun` / baseline stuck). Coverage hole until **stickiness** (row 8) — not first fire. | Vault HTTP flip. Option A **GONE**. |
| **Soft-530 api remaining OK-ish** | **Was** contrast when api was armed **and** firing. Soft-530 itself is still **OPEN** 530/1033. Living ~09:14 MT 2026-09-15: api is **same stall class** (`enabled:true` + cron-dead ~**56m** since ~08:21). | Proof that vault watch is firing. Living api health. |
| **Re-arm first-fire only** | In-place re-arm produced **one** `lastRun` advance, then cron died again. Necessary, **not** healthy. | Stickiness. Vault OPEN 502. |
| **Chronic stall** | Stall again within **24h** of a re-arm that reached first fire or stickiness. **≤1** pause/resume per calendar-day. Clock resets **America/Edmonton midnight**. Lead **paper only** after today's 1×. | Looping pause/resume. Ben recreate. Quiet-ops failure. Zone / Garage / docker / Doc-wake. |
| **Calendar-day chronic HOLD** | Both api + vault `enabled:true` but cron-dead after today's **1×** re-arm budget. Quiet-ops “Lookout continues” is **false for flip detection**. Interim = Chief `*/20` + Lead probes (accept **≤~20m**). Next local day Lead **may** try **one** in-place re-arm, then stickiness ≥3 `*/5`. | Quiet-ops failure. Ben recreate. Companion / brochure re-ask. |
| **Option A GONE** | Watch was **deleted** to fix stalled cron; Auto-review blocked recreate. | This vault / api stall. Do **not** delete vault or api to “match” that lesson. |

**Apply this SOP in-place.** Lead **may GO** in-place re-arm of **both** `projectcar-vault-health-watch` **and** `projectcar-api-health-watch` when stalled (pause/resume or re-save). **Never delete** to fix. **HOLD** any Ben recreate ask (quiet-ops + brochure-watch Auto-review lesson — delete already made Option A **GONE**). Then **verify stickiness** (row 8) **before** calling healthy.

Until stickiness (row 8), interim coverage = Chief weekday `*/20` smoke **+** Lead coding-progress probes — **not** a Ben ping. Do **not** invent Zone / Garage execute, docker re-ask, or Doc-wake re-ask from a stalled `lastRun`.

Living honesty this fold: Soft-530 **OPEN** 530/1033; vault **OPEN** 502; ListMachines **Mac.lan + lightning** / Docs **ABSENT**; Option A Redirect **PASS**; Soft-530 UX **LIVE**; Lookout **both chronic HOLD today**; **#82** Ben GO only.

This paper does **not** pause, resume, or mutate Lookout. Lead’s GO is **named** here; this fold does **not** execute it.

---

## Living class (2026-09-15 ~09:14 MT) — re-arm success ≠ first fire; require stickiness

**Lookout re-arm success ≠ first fire.** After in-place re-arm, success = `lastRun` advances across **≥3 consecutive schedule windows**. On a `*/5`: **≥3 fires spanning ≥10–15m**. One fire is necessary-not-sufficient. Do **not** call the watch healthy on first fire.

**Living example ~09:14 MT 2026-09-15:** vault re-arm ~**08:50** → first fire ~**08:55** OK → stall again (~**22m** no `lastRun` advance). `projectcar-api-health-watch` stalled ~**56m** since ~**08:21**. Same class: **`enabled:true` while cron-dead**. Soft-530 api remaining **OK-ish** is **not** living contrast this fold.

**Chronic stall class:** if a watch stalls again **within 24h** of a re-arm that reached first fire **or** stickiness, do **not** loop pause/resume more than **1×/calendar-day**. Clock resets **America/Edmonton midnight**. Classify **chronic**. Lead **paper only** after today's 1×. Interim = Chief `*/20` + Lead coding-progress probes (accept **≤~20m** flip latency). **HOLD** Ben recreate. Do **not** invent Zone / Garage / docker / Doc-wake from a chronic stall. **Chronic HOLD does not reopen a Ben recreate ask.** Soft-530 companions + brochure recreate stay **HOLD**.

**Quiet-ops exception ([soft-530-extended-open.md](soft-530-extended-open.md)):** when **both** api + vault are calendar-day chronic HOLD, “Lookout continues” is **false for flip detection**. **Chronic Lookout ≠ quiet-ops failure ≠ Ben ping.** Next local day Lead **may** try **one** in-place re-arm again, then stickiness **≥3** `*/5` before healthy. This paper does **not** execute that GO.

Living honesty this fold: Soft-530 **OPEN** 530/1033; vault **OPEN** 502; ListMachines **Mac.lan + lightning** / Docs **ABSENT**; Option A Redirect **PASS**; Soft-530 UX **LIVE**; Lookout **both chronic HOLD today**; **#82** Ben GO only.

**Lead may GO** in-place re-arm of both `projectcar-vault-health-watch` **and** `projectcar-api-health-watch` when stalled **if** the calendar-day 1× is unused, then **verify stickiness** before calling healthy. Living today: 1× spent → Lead **paper only** until **America/Edmonton midnight**. This paper does **not** execute that GO.

Quiet-ops ([soft-530-extended-open.md](soft-530-extended-open.md) lock 3) still holds: Lookout **continues** means api+vault **stay armed** **and** stay firing with **stickiness** — not just `enabled:true`. Soft-530 **OPEN** CF **1033** since 2026-09-13 ~11:57 America/Edmonton (**~24h+**); vault independently **OPEN** **502** since ~19:45 MT Sep 13; ListMachines **Mac.lan + lightning** / Docs **ABSENT**. The brochure **paper** continues. The continuous brochure watch is **GONE**.

**Overnight / weekend Option A Dynamic redirect is UNCOVERED — accept that risk.** Weekday Chief `*/20` is **weekday-hours coverage only**. After last weekday `*/20` (~17:40 MT) until the next weekday first fire (~06:00) — [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) — and Sat/Sun while plan-improve is **off** (`84107e7` weekend stay-up rows), there is **no** Option A redirect smoke. Last weekday `*/20` writes [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (Lookout watch state **GONE/armed/chronic HOLD** is a stamp field) — **refresh only on field DIFF**; else prior stamp **stands**. First weekday `*/20` after ~06:00 **diffs** that stamp — **same-class = stay quiet**; surface **Lead/Ben only on class DIFF**; do **not** rediscover; do **not** Ben-nag from an unchanged `GONE`. Do **not** invent overnight/weekend plan-improve, Zone, or Garage coverage to fill that gap. **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate. This paper **HOLDs** a second Ben recreate ask (row 3 already one-ask). **Redirect-only PASS ≠ Soft-530 UX PASS.** Duration ≠ recreate GO ≠ **#82** ≠ unfreeze ≠ companion re-ask ≠ honesty-off.

---

## SOP (eight)

| # | Lock | Meaning |
|---|------|---------|
| **1** | **Never delete** an armed Project Car Lookout watch to fix stalled cron | Delete is not a cron repair. A stalled schedule is **not** a missing watch. Deleting an armed watch (Option A, `api.` `/health`, or vault `/alive`) to “unstick” cron is forbidden. |
| **2** | Prefer **in-place update / pause-resume / re-save schedule** | Keep the routine. Edit the existing watch. Pause then resume. Re-save the schedule. Do **not** delete-and-recreate as first aid. |
| **3** | If delete **already happened** and recreate needs Auto-review: **HOLD** after **one** Ben ask | Living this fold: delete happened; Auto-review blocked recreate; watch **GONE**. **One** Ben ask to enable recreate. Then **HOLD**. Do **not** re-ask from this paper. Do **not** open a second Ben channel. Do **not** treat Auto-review as a companion re-ask. |
| **4** | Weekday Option A coverage = Chief plan-improve **`*/20` redirect smoke + Soft-530 UX**; overnight/weekend **UNCOVERED** | Continuous watch is **GONE**. Until Ben enables recreate, Chief keeps the existing **weekday** `*/20` Option A redirect smoke **and** Soft-530 UX acceptance ([brochure-redirect-watch.md](brochure-redirect-watch.md)). Last weekday `*/20` (~17:40 MT) writes [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (Redirect+UX PASS/FAIL/UNCOVERED + Lookout watch state) — **refresh only on field DIFF**. First weekday `*/20` after ~06:00 **diffs** that stamp — **same-class = stay quiet**; Lead/Ben only on class DIFF. **Mon–Thu overnight** after last `*/20` (~17:40 MT) until next weekday first fire (~06:00) **and** Sat/Sun plan-improve-off (`84107e7`): Option A Dynamic redirect is **explicitly uncovered — accept that risk**. Do **not** invent overnight/weekend plan-improve, Zone, or Garage coverage. **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate. Cross-link: this SOP · [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · weekend stay-up rows. Redirect **301**s + **root** `?v=` **200**s are **Redirect-only**. **Redirect-only PASS ≠ Soft-530 UX PASS.** UX rows: `membership.html` + `contact.html` still show Soft-530 Discord honesty; **root** `/waitlist.js?v=3` still fail-softs **502 / 530 / 1033** → Discord+mailto (`0705b37`); **root** `/styles.css?v=36` **200**. Probe those **root** paths — **not** `/assets/`. `/assets/styles.css?v=36` or `/assets/waitlist.js?v=3` **404** is **NOT** a regression. Homepage-only **200** is still insufficient. Not honesty-off. Not companions rearm. |
| **5** | After Ben approves recreate: assert **routine enabled** + **first fire within 10m** + baseline still **LIVE 10/10** | Lookout-owned. Flip **Chief + Lead only**; **never Ben** on pass↔fail. Stamp `enabled:true`. First fire ≤ **10 minutes**. Refresh / keep [brochure-redirect-watch.md](brochure-redirect-watch.md) baseline **LIVE 10/10** (Sep 9 `brochure-routing-baseline.json` still says extensionless **IN FLIGHT** — living pack is **LIVE 10/10**). This paper does **not** run that assert. |
| **6** | Soft-530 companions stay **HOLD** | `ops.` / `app.` `/login` (optional `cloud.`) stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. Option A recreate ≠ companion GO. |
| **7** | **`enabled:true` + cron-stalled ≠ missing watch ≠ HTTP flip** | A vault **or** api watch can stay `enabled:true` while `lastRun` / baseline stall (vault example ~**104m**, stuck ~**07:05** on a `*/5`; living api ~**56m** since ~08:21). That is **not** vault OPEN 502 and **not** Option A **GONE**. Soft-530 api remaining **OK-ish** is **not** living contrast this fold. Lead **may GO** in-place re-arm of **both** watches (pause/resume or re-save). **Never delete.** **HOLD** Ben recreate. First fire is necessary-not-sufficient — row 8. Docker permanence `@367172d` is a **different** tip — do **not** redo it here. |
| **8** | **Re-arm success ≠ first fire; require stickiness. Chronic ≤1 pause/resume per calendar-day (America/Edmonton midnight reset)** | After in-place re-arm, success = `lastRun` advances across **≥3 consecutive** schedule windows (`*/5`: ≥3 fires spanning **≥10–15m**). Living ~09:14 MT 2026-09-15: vault re-arm ~08:50 → first fire ~08:55 OK → stall again (~**22m**). If a watch stalls again **within 24h** of a re-arm that reached first fire or stickiness: classify **chronic**; do **not** loop pause/resume more than **1×/calendar-day**; clock resets **America/Edmonton midnight**; next local day Lead **may** try **one** in-place re-arm again, then stickiness before healthy; Lead **paper only** after today's 1×; interim = Chief `*/20` + Lead coding-progress probes (accept **≤~20m**); **HOLD** Ben recreate. When **both** api + vault are chronic HOLD, quiet-ops “Lookout continues” is **false for flip detection** ([soft-530-extended-open.md](soft-530-extended-open.md)). Do **not** call healthy on first fire. |

---

## Not #78 lookout-resume

| Card | Living | This SOP |
|------|--------|----------|
| **#78 lookout-resume** | **LIVE-SUPERSEDED** — `projectcar-api-health-watch` already `enabled:true` — **can still cron-stall** (living ~**56m** since ~08:21) | Do **not** re-open **#78**. Do **not** delete api-health. Lead **may GO** in-place re-arm when stalled; then stickiness (row 8) before healthy. |
| **Vault `/alive`** | **LIVE/armed** (`enabled:true`) — **can still cron-stall** (living: re-arm ~08:50 → first fire ~08:55 → stall ~22m) | Do **not** delete to fix cron. In-place pause/resume or re-save. Stall ≠ OPEN 502. First fire ≠ healthy. Separate McKing plane. |
| **Option A brochure watch** | **GONE** (deleted; Auto-review blocked recreate) | This SOP. HOLD after one Ben ask. Weekday Chief `*/20` only. Overnight/weekend **UNCOVERED**. |
| **Soft-530 companions** | **HOLD / not armed** | Stay HOLD. Not this recreate. Do **not** re-ask. |

`main` `doc-lid-restore.md` Soft-530 table still says api-health **paused**. Living is **`enabled:true`**. **#70** is SSOT until **#82**. Same class as STATUS Reality quarantine. Do **not** execute from `main`’s paused row. Do **not** open a tip-only PR.

---

## Quiet-ops (unchanged lock, honest coverage)

[soft-530-extended-open.md](soft-530-extended-open.md) lock 3: Lookout **continues**; companions **HOLD until Ben reopens**. **Chronic-HOLD exception:** when **both** api + vault are calendar-day chronic HOLD, “Lookout continues” is **false for flip detection**. **Chronic Lookout ≠ quiet-ops failure ≠ Ben ping.**

| Surface | Quiet-ops meaning now |
|---------|------------------------|
| Soft-530 `api.` `/health` | **Stay armed.** Never delete. **`enabled:true` ≠ firing.** Living 2026-09-15: **chronic HOLD today** (day's 1× spent; stalled ~**56m** since ~08:21 — same class as vault). Lead **may GO** in-place re-arm only if the calendar-day 1× is unused; next local day after **America/Edmonton midnight** Lead **may** try one again; stickiness before healthy. Remaining **OK-ish** is **not** living contrast. |
| Vault `/alive` | **Stay armed.** Never delete. **`enabled:true` + cron-stalled ≠ HTTP 502.** First fire ≠ healthy. Living 2026-09-15: **chronic HOLD today**. Lead **may GO** in-place re-arm (pause/resume / re-save) only if the day's 1× is unused; verify stickiness (row 8). Chronic ≤1 pause/resume per calendar-day (midnight reset). Interim = Chief `*/20` + Lead coding-progress probes (accept **≤~20m**) — **not** a Ben ping. |
| Both chronic HOLD | “Lookout continues” is **false for flip detection**. Interim Soft-530+vault SSOT smoke = Chief `*/20` + Lead probes. Does **not** reopen Ben recreate. Companions + brochure recreate stay **HOLD**. Stamp: [overnight-baseline-stamp.md](overnight-baseline-stamp.md). |
| Brochure Option A continuous watch | **GONE.** Paper continues. Weekday interim = Chief `*/20` redirect **+ Soft-530 UX**. Overnight/weekend Dynamic redirect is **UNCOVERED — accept that risk.** **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate. **HOLD** a second Ben recreate ask. **Redirect-only PASS ≠ Soft-530 UX PASS.** |
| Soft-530 companions | **HOLD.** Do **not** re-ask. |

Quiet-ops duration ≠ recreate enablement. This SOP does **not** lift quiet-ops and does **not** invent CLEAR.

---

## After Ben enables recreate (Lookout — not this paper)

Paper asserts only. Do **not** run them from a docs PR.

1. Routine **exists** (prefer the [brochure-redirect-watch.md](brochure-redirect-watch.md) name `projectcar-brochure-redirect-watch` unless Lookout already owns `brochure-option-a-redirect-watch` as the recreate).
2. Routine **`enabled:true`**.
3. **First fire within 10 minutes.**
4. Baseline still **LIVE 10/10** (apex+www `/` **301** → `/index.html`; `/shop` + `/shop.html` **301** → `/the-shop.html`; extensionless pretty pack **301** → matching `*.html`; **root** `/styles.css?v=36` + `/waitlist.js?v=3` **200** — **not** `/assets/`; those **404**s are **not** a regression).
5. Flip alerts **Chief + Lead only**. **Never Ben.** Never restart / mutate / Zone-edit from the watch.
6. Soft-530 companions still **HOLD**.

A Cloudflare **403** HTML challenge is WAF, not a Redirect-pack fail. Zone owns that — **not** from this paper.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** Lookout execute, **not** Auto-review bypass, **not** Zone apply, **not** Garage upload. |
| **Never delete to fix cron** | In-place update / pause-resume / re-save only. |
| **HOLD after one Ben ask** | Recreate is Auto-review-gated. One ask. Then stop. This fold is **not** a second ask. Do **not** open a second Ben recreate channel. |
| **Not #78** | Api-health already `enabled:true`. **LIVE-SUPERSEDED.** |
| **Not companion re-ask / rearm** | Companions stay **HOLD / not armed**. Do **not** re-ask. Do **not** rearm. |
| **Not #82 / not unfreeze / not Zone execute** | Recreate ≠ Worker-live ≠ Doc pull ≠ Redirect-pack edit. |
| **Weekday interim ≠ armed; overnight/weekend UNCOVERED** | Weekday Chief `*/20` is smoke coverage, not `enabled:true`. Overnight + weekend Option A Dynamic redirect is **uncovered — accept that risk**. Do **not** invent overnight plan-improve, Zone, or Garage coverage. |
| **Redirect-only PASS ≠ Soft-530 UX PASS** | `*/20` must also assert Membership/Contact Discord honesty + **root** `/waitlist.js?v=3` 502/530/1033 fail-soft + **root** `/styles.css?v=36` **200**. Pretty-URL **301**s alone are **not** UX PASS. **CLEAR ≠ honesty-off** (`0705b37`). `/assets/` CSS/JS **404** is **not** a fail. |
| **Quiet-ops continue** | [soft-530-extended-open.md](soft-530-extended-open.md). Api+vault stay armed. Brochure paper continues. Watch **GONE**. **Chronic-HOLD exception:** both watches calendar-day chronic HOLD → “Lookout continues” is **false for flip detection**. Chronic Lookout ≠ quiet-ops failure ≠ Ben ping. |
| **Lookout stall ≠ vault HTTP flip** | `enabled:true` + stalled `lastRun` / baseline is a **coverage class**, not OPEN 502 and not a missing watch. Lead **may GO** in-place re-arm of **both** api + vault when stalled. Interim = Chief `*/20` + Lead probes — **not** a Ben ping. Soft-530 api remaining OK-ish ≠ vault firing (and is **not** living contrast this fold). Docker permanence `@367172d` is **not** this fold. |
| **Re-arm success ≠ first fire** | After in-place re-arm, success = `lastRun` advances across **≥3 consecutive** `*/5` windows (≥3 fires spanning **≥10–15m**). Living: vault ~08:50 re-arm → ~08:55 first fire → ~22m stall. Do **not** call healthy on first fire. |
| **Chronic stall ≤1 pause/resume per calendar-day** | Stall again within **24h** of a re-arm that reached first fire or stickiness → classify **chronic**; clock resets **America/Edmonton midnight**; next local day Lead **may** try **one** in-place re-arm again, then stickiness ≥3 `*/5`; Lead **paper only** after today's 1×; interim Chief `*/20` + Lead probes (accept **≤~20m**); **HOLD** Ben recreate. Do **not** loop pause/resume. Chronic HOLD does **not** reopen a Ben recreate ask. |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Not #82 merge nag** | Worker-live / Direct Upload is still Ben GO. Soft-530 **OPEN ≠ #82 blocked**. Dual CLEAR ≠ auto-GO. Recreate ≠ upload. This paper does **not** nag **#82**. |
| **Not Dynamic wipe** | **#82 Worker-live ≠ retire Dynamic** (`49ccf90`). Interim smoke does **not** authorize deleting the **10/10** pack. |
| **Not honesty-off** | **#80** Membership/Contact Discord honesty + `waitlist.js?v=3` fail-soft stay (`0705b37`). **CLEAR ≠ honesty-off.** |
| **Not unfreeze** | Freeze `4cf8924` / **`5swmVz`** until **Ben GO**. Watch recreate ≠ Doc pull. |
| **Not Zone execute** | No Redirect-pack edit, no Direct Upload, no purge from this paper. |
| **Not companion re-ask / rearm** | Soft-530 companions stay **HOLD**. Do **not** re-ask. Do **not** rearm from this paper. |
| **Not #78 re-open** | Api-health already armed. **LIVE-SUPERSEDED.** |
| **Not delete api / vault** | Same SOP. Stalled cron ≠ missing watch. |
| **Not invent `enabled:true`** | Option A watch is **GONE** until Ben enables recreate **and** Lookout stamps row 5. |
| **Not a second Ben ask** | One ask for Auto-review recreate. This paper **HOLDs**. Overnight/weekend uncovered ≠ a new Ben recreate page. |
| **Not invent overnight/weekend redirect smoke** | Do **not** invent overnight plan-improve, Zone, or Garage Option A coverage. **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate. |
| **Not collapse stall into 502** | Cron stall ≠ vault origin-down. Do **not** start a vault-stay-up wake from a stalled `lastRun`. |
| **Not call healthy on first fire** | Re-arm success = stickiness (≥3 consecutive `*/5` windows). Living: ~08:55 first fire then ~22m stall. |
| **Not loop pause/resume on chronic** | Stall again within 24h → **≤1** pause/resume per calendar-day. Clock resets America/Edmonton midnight. Lead paper only after today's 1×. |
| **Not treat chronic HOLD as quiet-ops failure** | Chronic Lookout ≠ quiet-ops failure ≠ Ben ping. Interim = Chief `*/20` + Lead probes. Does **not** reopen Ben recreate. |
| **Not Ben recreate / docker / Doc-wake for stall** | Quiet-ops + Auto-review lesson. In-place re-arm (Lead GO both watches when stalled). Interim = Chief `*/20` + Lead coding-progress probes. |
| **Not redo docker permanence** | Vault CLEAR `docker.service` already `@367172d`. This fold is stall / stickiness / chronic only. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / living dual-OPEN honesty (`5f2fd1c`) / quiet-ops (`1e6a0b1`) / brochure-redirect watch paper (`f336fcb`) / **#78 LIVE-SUPERSEDED** — **unchanged**. This file executes **none** of those.

---

## Do not

- Delete an armed Lookout watch to fix stalled cron
- Re-ask Ben from this paper (one ask, then **HOLD**)
- Invent a second Ben recreate ask because overnight/weekend Option A is uncovered
- Re-ask Soft-530 companions
- Re-open **#78** or treat this as lookout-resume
- Claim Option A continuous watch `enabled:true` while it is **GONE**
- Invent overnight/weekend plan-improve, Zone, or Garage Option A coverage
- Treat weekday Chief `*/20` smoke as an armed flip watch, or as overnight/weekend coverage
- Treat Redirect-only `*/20` PASS as Soft-530 UX PASS
- Treat `/assets/styles.css?v=36` or `/assets/waitlist.js?v=3` **404** as a regression (live HTML is **root** `/styles.css?v=36` + `/waitlist.js?v=3`)
- Strip Soft-530 Discord honesty / `waitlist.js` fail-soft (honesty-off)
- Rearm Soft-530 companions
- Wipe Option A Dynamic **10/10** or nag **#82**
- Execute Zone / Garage / Lookout recreate from this paper
- Invent **#82**, unfreeze, CLEAR, or Bitwarden from a missing watch
- Treat vault `enabled:true` + stalled `lastRun` as vault OPEN 502, or as a missing watch
- Delete `projectcar-vault-health-watch` or `projectcar-api-health-watch` because cron stalled (~104m / ~07:05 vault; ~56m / ~08:21 api)
- Call a re-armed watch healthy on first fire (require stickiness — ≥3 consecutive `*/5` windows)
- Loop pause/resume more than **1×/calendar-day** on a chronic stall (stall again within 24h; clock resets America/Edmonton midnight)
- Treat calendar-day chronic HOLD as quiet-ops failure, or as a Ben ping
- Reopen a Ben recreate ask because both api + vault are chronic HOLD
- Ping Ben to recreate the vault or api watch, or re-ask docker / Doc-wake from a stall
- Treat Soft-530 api remaining OK-ish as living contrast, or as proof the vault `*/5` is firing
- Redo vault CLEAR docker.service permanence (`367172d`) — different tip

# Lookout rearm SOP — never delete to fix cron

**Status:** Paper SOP — living incident **HOLD**  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (this pointer + Lookout rows + **#78 LIVE-SUPERSEDED** honesty), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A watch **spec** — living watch is **GONE**; interim Chief `*/20` **+ Soft-530 UX**; **Redirect-only PASS ≠ Soft-530 UX PASS**), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — Lookout api+vault **continue**; brochure continuous watch **does not**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**CLEAR ≠ honesty-off** `0705b37`), [brochure-worker-ci.md](brochure-worker-ci.md) (frozen Redirect inventory SSOT), `api-stay-up.md` (**#78 lookout-resume** is **LIVE-SUPERSEDED** — api-health already `enabled:true`), `vault-stay-up.md` (vault `/alive` **LIVE/armed** — **not** this recreate), `shop-web-stay-up.md` (Soft-530 companions **HOLD / not armed**)

**Never delete** an armed Project Car Lookout watch to fix a stalled cron. This file names that lock and the living Option A gap.

This fold is **paper only**. It does **not** arm, recreate, pause, or mutate Lookout. It does **not** execute Zone or Garage. It does **not** re-ask companions. It is **not** **#78** lookout-resume.

---

## Living incident (2026-09-14)

`brochure-option-a-redirect-watch` was **deleted** to fix a stalled cron. Recreate then needed **Auto-review**. Auto-review **blocked** recreate. The watch is **GONE**.

Soft-530 companion watches stay **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask). This incident ≠ those companions.

Paper spec name in [brochure-redirect-watch.md](brochure-redirect-watch.md) is `projectcar-brochure-redirect-watch`. The deleted living name is `brochure-option-a-redirect-watch`. Either name: **no** armed Option A flip watch exists now. Do **not** invent `enabled:true`.

**#78 lookout-resume honesty (do not collapse):** **#78** is **LIVE-SUPERSEDED**. `projectcar-api-health-watch` is already **`enabled:true`** (resume 2026-09-11 ~06:52 America/Edmonton) while Doc stays frozen at `4cf8924` / `5swmVz`. Vault `/alive` is a **separate LIVE/armed** watch. This SOP is **not** a re-run of **#78**. Deleting api-health or vault to “fix cron” is the same anti-goal as deleting the brochure watch. Recreating Option A is **not** “resume Lookout.”

Quiet-ops ([soft-530-extended-open.md](soft-530-extended-open.md)) still holds: Soft-530 **OPEN** CF **1033** since 2026-09-13 ~11:57 America/Edmonton (**~24h+**); vault independently **OPEN** **502** since ~19:45 MT Sep 13; ListMachines **Mac.lan only**. Quiet-ops says Lookout **continues** — that means **api + vault stay armed**, and the brochure **paper** continues. The continuous brochure watch is **GONE**. Interim coverage is Chief `*/20` redirect smoke **+ Soft-530 UX acceptance** (row 4). **Redirect-only PASS ≠ Soft-530 UX PASS.** Duration ≠ recreate GO ≠ **#82** ≠ unfreeze ≠ companion re-ask ≠ honesty-off.

---

## SOP (six)

| # | Lock | Meaning |
|---|------|---------|
| **1** | **Never delete** an armed Project Car Lookout watch to fix stalled cron | Delete is not a cron repair. A stalled schedule is **not** a missing watch. Deleting an armed watch (Option A, `api.` `/health`, or vault `/alive`) to “unstick” cron is forbidden. |
| **2** | Prefer **in-place update / pause-resume / re-save schedule** | Keep the routine. Edit the existing watch. Pause then resume. Re-save the schedule. Do **not** delete-and-recreate as first aid. |
| **3** | If delete **already happened** and recreate needs Auto-review: **HOLD** after **one** Ben ask | Living this fold: delete happened; Auto-review blocked recreate; watch **GONE**. **One** Ben ask to enable recreate. Then **HOLD**. Do **not** re-ask from this paper. Do **not** open a second Ben channel. Do **not** treat Auto-review as a companion re-ask. |
| **4** | Interim Option A coverage = Chief plan-improve **`*/20` redirect smoke + Soft-530 UX** until recreate is enabled | Continuous watch is **GONE**. Until Ben enables recreate, Chief keeps the existing `*/20` Option A redirect smoke **and** Soft-530 UX acceptance ([brochure-redirect-watch.md](brochure-redirect-watch.md)). Redirect **301**s + `?v=` **200**s are **Redirect-only**. **Redirect-only PASS ≠ Soft-530 UX PASS.** UX rows: `membership.html` + `contact.html` still show Soft-530 Discord honesty; `waitlist.js?v=3` still fail-softs **502 / 530 / 1033** → Discord+mailto (`0705b37`). Homepage-only **200** is still insufficient. Not honesty-off. Not companions rearm. |
| **5** | After Ben approves recreate: assert **routine enabled** + **first fire within 10m** + baseline still **LIVE 10/10** | Lookout-owned. Flip **Chief + Lead only**; **never Ben** on pass↔fail. Stamp `enabled:true`. First fire ≤ **10 minutes**. Refresh / keep [brochure-redirect-watch.md](brochure-redirect-watch.md) baseline **LIVE 10/10** (Sep 9 `brochure-routing-baseline.json` still says extensionless **IN FLIGHT** — living pack is **LIVE 10/10**). This paper does **not** run that assert. |
| **6** | Soft-530 companions stay **HOLD** | `ops.` / `app.` `/login` (optional `cloud.`) stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. Option A recreate ≠ companion GO. |

---

## Not #78 lookout-resume

| Card | Living | This SOP |
|------|--------|----------|
| **#78 lookout-resume** | **LIVE-SUPERSEDED** — `projectcar-api-health-watch` already `enabled:true` | Do **not** re-open **#78**. Do **not** pause or delete api-health. |
| **Vault `/alive`** | **LIVE/armed** (`enabled:true`) | Do **not** delete to fix cron. Separate McKing plane. |
| **Option A brochure watch** | **GONE** (deleted; Auto-review blocked recreate) | This SOP. HOLD after one Ben ask. Interim Chief `*/20`. |
| **Soft-530 companions** | **HOLD / not armed** | Stay HOLD. Not this recreate. Do **not** re-ask. |

`main` `doc-lid-restore.md` Soft-530 table still says api-health **paused**. Living is **`enabled:true`**. **#70** is SSOT until **#82**. Same class as STATUS Reality quarantine. Do **not** execute from `main`’s paused row. Do **not** open a tip-only PR.

---

## Quiet-ops (unchanged lock, honest coverage)

[soft-530-extended-open.md](soft-530-extended-open.md) lock 3: Lookout **continues**; companions **HOLD until Ben reopens**.

| Surface | Quiet-ops meaning now |
|---------|------------------------|
| Soft-530 `api.` `/health` | **Stay armed.** Never delete. |
| Vault `/alive` | **Stay armed.** Never delete. |
| Brochure Option A continuous watch | **GONE.** Paper continues. Interim = Chief `*/20` redirect **+ Soft-530 UX** until recreate is enabled. **Redirect-only PASS ≠ Soft-530 UX PASS.** |
| Soft-530 companions | **HOLD.** Do **not** re-ask. |

Quiet-ops duration ≠ recreate enablement. This SOP does **not** lift quiet-ops and does **not** invent CLEAR.

---

## After Ben enables recreate (Lookout — not this paper)

Paper asserts only. Do **not** run them from a docs PR.

1. Routine **exists** (prefer the [brochure-redirect-watch.md](brochure-redirect-watch.md) name `projectcar-brochure-redirect-watch` unless Lookout already owns `brochure-option-a-redirect-watch` as the recreate).
2. Routine **`enabled:true`**.
3. **First fire within 10 minutes.**
4. Baseline still **LIVE 10/10** (apex+www `/` **301** → `/index.html`; `/shop` + `/shop.html` **301** → `/the-shop.html`; extensionless pretty pack **301** → matching `*.html`; `styles.css?v=36` + `waitlist.js?v=3` **200`).
5. Flip alerts **Chief + Lead only**. **Never Ben.** Never restart / mutate / Zone-edit from the watch.
6. Soft-530 companions still **HOLD**.

A Cloudflare **403** HTML challenge is WAF, not a Redirect-pack fail. Zone owns that — **not** from this paper.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** Lookout execute, **not** Auto-review bypass, **not** Zone apply, **not** Garage upload. |
| **Never delete to fix cron** | In-place update / pause-resume / re-save only. |
| **HOLD after one Ben ask** | Recreate is Auto-review-gated. One ask. Then stop. This fold is **not** a second ask. |
| **Not #78** | Api-health already `enabled:true`. **LIVE-SUPERSEDED.** |
| **Not companion re-ask / rearm** | Companions stay **HOLD / not armed**. Do **not** re-ask. Do **not** rearm. |
| **Not #82 / not unfreeze / not Zone execute** | Recreate ≠ Worker-live ≠ Doc pull ≠ Redirect-pack edit. |
| **Interim ≠ armed** | Chief `*/20` is smoke coverage, not `enabled:true`. |
| **Redirect-only PASS ≠ Soft-530 UX PASS** | `*/20` must also assert Membership/Contact Discord honesty + `waitlist.js` 502/530/1033 fail-soft. Pretty-URL **301**s alone are **not** UX PASS. **CLEAR ≠ honesty-off** (`0705b37`). |
| **Quiet-ops continue** | [soft-530-extended-open.md](soft-530-extended-open.md). Api+vault stay armed. Brochure paper continues. Watch **GONE**. |

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
| **Not a second Ben ask** | One ask for Auto-review recreate. This paper **HOLDs**. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / living dual-OPEN honesty (`5f2fd1c`) / quiet-ops (`1e6a0b1`) / brochure-redirect watch paper (`f336fcb`) / **#78 LIVE-SUPERSEDED** — **unchanged**. This file executes **none** of those.

---

## Do not

- Delete an armed Lookout watch to fix stalled cron
- Re-ask Ben from this paper (one ask, then **HOLD**)
- Re-ask Soft-530 companions
- Re-open **#78** or treat this as lookout-resume
- Claim Option A continuous watch `enabled:true` while it is **GONE**
- Treat Chief `*/20` smoke as an armed flip watch
- Treat Redirect-only `*/20` PASS as Soft-530 UX PASS
- Strip Soft-530 Discord honesty / `waitlist.js` fail-soft (honesty-off)
- Rearm Soft-530 companions
- Wipe Option A Dynamic **10/10** or nag **#82**
- Execute Zone / Garage / Lookout recreate from this paper
- Invent **#82**, unfreeze, CLEAR, or Bitwarden from a missing watch

# Soft-530 weekday overnight — Mon–Thu Lookout-only gap

**Status:** Living ops — paper lock  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer + weekend Soft-530), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops lock while OPEN **~24h+** + vault OPEN + **Mac.lan only** — this file is the **weekday overnight coverage** twin, **not** that lock), weekend Soft-530 coverage (`84107e7` — Sat/Sun plan-improve-off; STATUS Live / Locks + [api-stay-up.md](api-stay-up.md) / [doc-lid-restore.md](doc-lid-restore.md) / [vault-stay-up.md](vault-stay-up.md) / [shop-web-stay-up.md](shop-web-stay-up.md)), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**first hop** if Doc reappears mid-overnight — machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`; **never** `Mac.lan` / Porsche), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** if McKing / `lightning` reappears mid-overnight — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (last weekday `*/20` ~17:40 MT **one-liner** before this Lookout-only window; first weekday `*/20` after ~06:00 **diffs** that stamp — no rediscover / no Ben re-nag from stamp alone), [lookout-rearm-sop.md](lookout-rearm-sop.md) (weekday Chief `*/20` **pauses** in this window — Option A Dynamic redirect **UNCOVERED**; Lookout api+vault stay armed; **HOLD** second Ben recreate ask), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Option A **paper** continues; continuous watch **GONE**; overnight/weekend **UNCOVERED**), [dual-host-outage.md](dual-host-outage.md) (wake order — **Doc first, then McKing**), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — **never auto-fire**), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Complement of **weekend Soft-530 coverage** (`84107e7` — plan-improve **off Sat/Sun**) and **quiet-ops** ([soft-530-extended-open.md](soft-530-extended-open.md)). This file names the **weekday overnight gap**: after the last weekday Chief plan-improve `*/20` until the next weekday first fire. Soft-530 + vault coverage in that window is Lookout `api.` `/health` + vault `/alive` **only**.

While `brochure-option-a-redirect-watch` is **GONE**, overnight (this card) **and** weekend (`84107e7` stay-up rows) Option A Dynamic redirect coverage is **explicitly uncovered — accept that risk**. Do **not** invent overnight plan-improve, Zone, or Garage coverage. **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Cross-link: [lookout-rearm-sop.md](lookout-rearm-sop.md) · this file · weekend Soft-530 coverage (`84107e7` / stay-up rows). **HOLD** a second Ben recreate ask (`lookout-rearm-sop` already one-ask).

Last weekday `*/20` (~17:40 MT) writes the [overnight-baseline-stamp.md](overnight-baseline-stamp.md) one-liner **before** this window. First weekday `*/20` after ~06:00 diffs that stamp instead of rediscovering. Friday last `*/20` stamps, then hands **into weekend coverage**. Stamp alone ≠ Ben re-nag ≠ Zone / Garage. Overnight **CLEAR** still [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [vault-clear-smoke.md](vault-clear-smoke.md) + first-hop cards.

This card is **Mon–Thu nights only**. Friday’s last `*/20` hands **into weekend coverage**, not back into this file. This fold executes **none** of Zone Direct Upload, Garage, **#82**, unfreeze, companions, Bitwarden, a Ben Doc-wake re-nag, or a second Ben recreate ask.

---

## Window (Mon–Thu nights only)

| Edge | Stamp / meaning |
|------|-----------------|
| **Starts** | After last weekday plan-improve `*/20` — **~17:40** America/Edmonton (MT). That fire writes [overnight-baseline-stamp.md](overnight-baseline-stamp.md) **first**. |
| **Ends** | Next weekday first fire — **~06:00** America/Edmonton. That fire **diffs** the stamp. |
| **Nights** | **Mon–Thu only.** Not Friday night. Not Sat/Sun. |
| **Friday last `*/20`** | Writes [overnight-baseline-stamp.md](overnight-baseline-stamp.md), then hands **into weekend coverage** (`84107e7` / STATUS Live Weekend Soft-530). Do **not** stay on this card overnight Friday→Saturday. |
| **Monday first fire** | Weekday plan-improve `*/20` **resumes** (~06:00 MT) and **diffs** the Friday stamp. This gap is over. |

Quiet-ops may **already** be in force during this window ([soft-530-extended-open.md](soft-530-extended-open.md)). Overnight coverage does **not** lift quiet-ops and does **not** invent a new Ben ask from the clock.

---

## Coverage (Lookout only)

Same flip set as weekend coverage. Companions stay **HOLD**.

| Plane | Overnight coverage | Not this window |
|-------|--------------------|-----------------|
| **Soft-530** | Lookout `projectcar-api-health-watch` — `GET https://api.projectcar.ca/health` | Soft-530 ops/app (`cloud.`) companion watches — **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask) |
| **Vault** | Lookout vault `/alive` (fallback `/api/config` if `/alive` 404s) | Bitwarden import/rotate. Vault flip ≠ Doc lid-restore. |
| **Option A brochure** | **UNCOVERED — accept that risk.** Paper continues ([brochure-redirect-watch.md](brochure-redirect-watch.md)). Continuous watch is **GONE**. Weekday Chief `*/20` **pauses** after last weekday fire until next weekday first fire. Same uncovered class as weekend (`84107e7`). **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Do **not** invent overnight plan-improve / Zone / Garage coverage. **HOLD** a second Ben recreate ask. | Overnight Zone Direct Upload / Worker / purge. Overnight redirect smoke. Soft-530 UX assets stay **root-relative LIVE** (`/styles.css?v=36` + `/waitlist.js?v=3` — not `/assets/`). |
| **Control plane** | Doc KeepAlive / lid-close if Doc is reachable: `com.projectcar.cloudflared` + uvicorn `:8000` + `next start` `:3000`. **Not** unfreeze. **Not** **#82**. | Overnight Garage **#79.1** execute. Overnight `git pull` / rebuild while freeze `4cf8924` / **`5swmVz`** holds. |

`ops.` / `app.` (and `cloud.`) can **530 while `api.` `/health` stays 200**. That blind spot is **accepted** overnight — companions stay **HOLD**. Do **not** invent a companion re-ask because the shop UI is dark.

---

## Mid-overnight reappear (still first hops)

If `Docs-MacBook-Pro` or `lightning` **reappears** on ListMachines during this gap, **do not** treat overnight duration as a GO. Follow the same first hops as quiet-ops. **Never** `Mac.lan` as either host. **Never auto-fire.**

| Host reappears | First hop | Then |
|----------------|-----------|------|
| **`Docs-MacBook-Pro`** | [doc-reappear-first-hop.md](doc-reappear-first-hop.md) — assert machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. **Never** `Mac.lan` / Porsche as Doc. | Lid-restore process wake on the **asserted** host → [soft-530-clear-smoke.md](soft-530-clear-smoke.md) → **only if CLEAR** → forensics → [post-dual-clear-go.md](post-dual-clear-go.md) (**never auto-fire**) |
| **`lightning` / McKing** | [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) — assert machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`** (label **lightning**). **Never** `Mac.lan`. | Vault wake on the **asserted** host → [vault-clear-smoke.md](vault-clear-smoke.md) → **only if CLEAR** → forensics. Bitwarden stays **Ben GO**, **never auto-fire**. |

Wake order stays [dual-host-outage.md](dual-host-outage.md) — **Doc first, then McKing**; parallel only if both names are on ListMachines. `Mac.lan` online is **not** a reappear of either host.

---

## Living snapshot (this fold)

STATUS pointers stay canonical. Honesty this fold:

| Surface | Living |
|---------|--------|
| **Soft-530** | **OPEN** — `api.` / `app.` / `ops.` / `cloud.` **530** CF **1033** since 2026-09-13 ~11:57 America/Edmonton |
| **Waitlist OPTIONS** | **530** |
| **Vault** | `/alive` **502** since ~19:45 MT Sep 13 (**not** 1033) |
| **ListMachines** | **`Mac.lan` only** — `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning` |
| **Freeze** | Intact **`4cf8924`** / BUILD_ID **`5swmVz`** |
| **#82** | Still **Ben GO**. Soft-530 **OPEN ≠ #82 blocked** — this overnight gap still ≠ auto-GO |
| **Option A Dynamic redirect** | **UNCOVERED overnight** while watch **GONE** — accept that risk. **Next smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. |
| **Soft-530 UX assets** | **Root-relative LIVE** — `/styles.css?v=36` + `/waitlist.js?v=3` (not `/assets/`; those 404s are **not** a regression). Membership/Contact Discord honesty stays. UX **LIVE** ≠ overnight redirect smoke. |

This paper does **not** invent CLEAR, a host reappear, or a morning fire.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **#82 upload** | Overnight duration ≠ Worker-live. Soft-530 **OPEN ≠ #82 blocked**, but this card is **not** a GO. |
| **Unfreeze** | Freeze `4cf8924` / **`5swmVz`** until **Ben GO**. Overnight lid-close ≠ pull. |
| **Companion re-ask** | ops/app companions **HOLD until Ben reopens** — not weekend-only, not overnight-only. Do **not** re-ask. |
| **Bitwarden** | Import/rotate **blocked** until vault **CLEAR**, then still **Ben GO**. Overnight **502** ≠ rotate. |
| **Ben Doc-wake re-nag** | Doc-wake + McKing wake **already asked**. OPEN duration alone (weekday overnight or ~24h quiet-ops) ≠ a new Ben page. |
| **Overnight Zone Direct Upload** | No Worker upload / purge from this gap. Friday last `*/20` → weekend coverage, which also forbids weekend Zone. Do **not** invent Zone Option A coverage. |
| **Overnight Garage execute** | No **#79.1** rebuild / `changeme` strip from this paper. Do **not** invent Garage Option A coverage. |
| **Invent overnight redirect smoke** | Option A Dynamic redirect is **uncovered — accept that risk**. Do **not** invent overnight plan-improve. **Next Option A smoke** = first weekday `*/20` after ~06:00, or Ben-approved Lookout recreate. |
| **Second Ben recreate ask** | [lookout-rearm-sop.md](lookout-rearm-sop.md) already one-ask. Overnight uncovered ≠ a new Ben page. |
| **Treat Friday night as this card** | Friday last `*/20` → **weekend coverage**. This file is **Mon–Thu nights** only. |
| **Treat `Mac.lan` as Doc or McKing** | Identity lock unchanged. Mid-overnight reappear still [doc-reappear-first-hop.md](doc-reappear-first-hop.md) / [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md). |
| **Auto-fire on reappear** | First hops, then smoke, then (only if CLEAR) forensics, then the sequencer. **Never auto-fire.** |
| **Drop Lookout api+vault** | Those two watches **are** overnight coverage. **Never delete** them to fix stalled cron ([lookout-rearm-sop.md](lookout-rearm-sop.md)). |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / quiet-ops (`1e6a0b1`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Re-nag Ben for Doc-wake because the weekday clock crossed ~17:40 or the OPEN lasted overnight
- Schedule overnight Zone Direct Upload / Worker / purge, or overnight Garage execute
- Invent overnight plan-improve / Zone / Garage Option A redirect smoke (uncovered — accept that risk)
- Re-ask Ben to recreate Lookout Option A from this paper (`lookout-rearm-sop` already one-ask)
- Arm Soft-530 companions from this paper, or treat HOLD as weekend-only
- Treat Friday last `*/20` as another Mon–Thu overnight — that handoff is **weekend coverage**
- Shell `Mac.lan` or Porsche as Doc or McKing if a host name appears overnight
- Skip [doc-reappear-first-hop.md](doc-reappear-first-hop.md) / [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) on mid-overnight reappear
- Auto-fire **#82** / unfreeze / **#79.1** / companions / Zone upload / Bitwarden from a reappear or from duration
- Invent CLEAR while Soft-530 is still **OPEN** (CF **1033**) or vault is still **OPEN** (**502**)
- Drop Lookout `api.` `/health` or vault `/alive` because plan-improve `*/20` is paused
- Execute Zone / Garage / Lookout companion arm / Bitwarden from this paper

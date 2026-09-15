# Shared fleet cards — Docs SSOT (held #70)

**Status:** Paper — Chief standing-notes hygiene. **Not SSOT.** Rewrite **DONE**. Living-host Soft-530 class+as-of **queued**.  
**Updated:** 2026-09-15 ~17:30 America/Edmonton  
**Related:** `STATUS.md` (Reality one-liner · living-ops / Locks), [deployment-guide.md](deployment-guide.md) (Monday paper map), [home-lab-specification.md](home-lab-specification.md) (host split), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (camp vault-on-doc), [unfreeze-readiness.md](unfreeze-readiness.md) (freeze / draft ≠ GO), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (tonight Soft-530=**OPEN** + **`soft530_open_since` ~16:36** — already tip `7226b98`; Shared must not contradict), [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) (**CONNECTED ≠ Shellable ≠ tunnel healthy**; next CONNECTED+**Shellable** = Shared living-host amend host — **never** `Mac.lan`)

Fleet Shared `shop-os-mc-plan.md` is **rewritten** and remains **non-SSOT**. Prefer this thin card + the STATUS Reality one-liner. Do **not** dual-author living ops on Shared. **Docs/#70 → `main` is SSOT**; Shared is standing notes only.

Chief rewrite **DONE** ~15:42 America/Edmonton on Doc `~/Desktop/Fleet-Nextcloud/Memory/Shared/shop-os-mc-plan.md` — **not** still “rewrite in progress”. That rewrite stamped Soft-530 **CLEAR**. Living is Soft-530 **OPEN** since **~16:36** with ListMachines **EMPTY**. Do **not** leave Shared **CLEAR** language for overnight/morning readers. Chief will amend the Shared living-host line on the **next Docs CONNECTED+Shellable** (warm companion; **never** `Mac.lan`). This paper records the **queue rule** — it does **not** execute that Shared amend. Merging this file is **not** a Shared rewrite execute, **not** a Garage/Zone fan-out, **not** a Ben ask, and **not** unfreeze / **#82** / camp GO.

---

## SSOT lock

| Lock | Meaning |
|------|---------|
| **`Coombzy/Project-Car` `Docs/` is SSOT** | Held **#70** → `main` is the product / living-ops source of truth. Shared fleet cards are **Chief standing notes only**. |
| **Shared must not contradict Docs tip / live** | If Shared language disagrees with Docs tip or live, **discard Shared language**. Do not “reconcile” by rewriting Docs toward Shared. |
| **Shared rewrite is DONE** | Chief rewrote Shared `shop-os-mc-plan.md` ~15:42 America/Edmonton on Doc `~/Desktop/Fleet-Nextcloud/Memory/Shared/shop-os-mc-plan.md`. That rewrite **must match Docs**. This paper notes the receipt; it does **not** land Shared text in this repo. Do **not** keep “in progress”. |
| **Living-host lines carry Soft-530 class + as-of** | Fleet Shared `shop-os-mc-plan.md` living-host lines **must** stamp Soft-530 **CLEAR** or **OPEN** **and** an America/Edmonton as-of wall time. Class-only or undated living-host copy is **stale**. Cross [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (`soft530_open_since`). |
| **Same-day CLEAR↔OPEN flip → queue Shared living-host amend** | After a Shared rewrite, a same-day Soft-530 **CLEAR↔OPEN** flip queues a Shared living-host amend on the **next Docs CONNECTED+Shellable** (warm companion). **Never** `Mac.lan`. Amend ≠ Ben ask ≠ **#82** / unfreeze / camp Zone. Cross [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md). |

---

## Living-host Soft-530 class+as-of (this fold)

Living-host lines on Fleet Shared `shop-os-mc-plan.md` must carry:

| Field | Required |
|-------|----------|
| **Soft-530 class** | **CLEAR** or **OPEN** (public class: `/health` **200**, or **530 / CF 1033**) |
| **as-of wall** | America/Edmonton wall time of that class. After same-day **CLEAR→OPEN**, use the **current** OPEN flip — living **`soft530_open_since` ~16:36**. Do **not** keep the ~15:42 **CLEAR** as-of once live flipped. |

**Same-day flip queue.** If Soft-530 **CLEAR↔OPEN** flips the same America/Edmonton day **after** a Shared rewrite:

1. **Do not** leave the prior Shared class language for overnight / morning readers.
2. **Queue** a Shared living-host amend on the **next Docs CONNECTED+Shellable** (warm companion — [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md)).
3. **Never** Shell `Mac.lan` as that companion.
4. The amend is **Chief paper on Shared standing notes** — **not** a Ben ask, **not** **#82**, **not** unfreeze, **not** camp Zone.
5. Until that Shellable amend lands, **Docs/#70 → `main` is SSOT**. Discard Shared **CLEAR** if live is **OPEN**.

**Evidence 2026-09-15:** Shared rewrite **~15:42** stamped Soft-530 **CLEAR**. Live **OPEN** since **~16:36** with ListMachines **EMPTY** (Lead-verified **~16:51** after flap-while-connected). Overnight stamp tonight already Soft-530=**OPEN** + **`soft530_open_since` ~16:36** ([overnight-baseline-stamp.md](overnight-baseline-stamp.md) tip `7226b98`). Shared living-host line still carries ~15:42 **CLEAR** — **queued** for next Doc Shellable. This fold records the queue; it does **not** execute the Shared file.

**Chief note:** Chief will amend the Shared living-host line on the next Doc Shellable. Until then, overnight/morning readers use this card + the overnight stamp — **not** Shared **CLEAR**.

---

## What the Shared rewrite dropped / aligned

Chief’s Shared `shop-os-mc-plan.md` rewrite (outside this repo) **did**:

| Did | Do not undo |
|-----|-------------|
| **Dropped the false brochure 502 lock** | Restore “brochure stays 502” language. Public `projectcar.ca` is **LIVE** (Option A) since the **2026-09-06** unlock — Shared “stays 502” was **false**. |
| **Dropped Garage-blocked-on-502** | Fan out Garage / Zone / Hatch from Shared or from this Docs fold. |
| **Marked non-SSOT vs Docs / #70** | Treat Shared as living-ops SSOT. Docs held **#70** → `main` stays SSOT; Shared = standing notes only. |
| **Aligned Soft-530 CLEAR half-state** | Collapse Soft-530 **CLEAR** into dual CLEAR, Doc unfreeze, or **#82** Worker-live. Living is **dual OPEN** (half-state **OVER**). Shared ~15:42 **CLEAR** is now **stale** vs live **OPEN ~16:36**. |
| **Aligned camp vault-on-Doc** | Treat parked McKing shop-host / vault-stay-up as camp SSOT. Camp SSOT is [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) — **Ben GO**, never auto. |
| **Aligned freeze `4cf8924` / `5swmVz`** | Treat freeze as lifted. Living pin: `` `changeme` `` / BUILD_ID **`5swmVz`** / tip **`4cf8924`** until **Ben GO**. |
| **Aligned #82 not auto** | Auto-GO **#82** from Soft-530 **CLEAR** or from this fold. |

Vault **OPEN 530 / CF 1033** (was 502 since ~19:45 MT Sep 13) stays living honesty. That is **not** the brochure 502 lock. Do **not** restore brochure-502 language while recording vault 1033.

---

## Living this fold (honesty)

| Plane / pin | Living class |
|-------------|--------------|
| **Soft-530 (Doc)** | **OPEN 530 / CF 1033** since **~16:36** America/Edmonton — `api.` / `app.` / `ops.` (Lookout + Lead; **was CLEAR** ~13:21–16:36). ListMachines **EMPTY**. Half-state **OVER**. |
| **Vault (McKing)** | **OPEN 530 / CF 1033** connector-down (was 502 since ~19:45 MT Sep 13 — **not** CLEAR) |
| **Brochure** | **LIVE** since the **2026-09-06** unlock (Option A). Shared “stays 502” is **false**. |
| **Shared `shop-os-mc-plan.md`** | **Rewritten** ~15:42 America/Edmonton on Doc `~/Desktop/Fleet-Nextcloud/Memory/Shared/shop-os-mc-plan.md`. Still **non-SSOT**. Shared ~15:42 living-host stamped Soft-530 **CLEAR** — **stale**. Living **OPEN** since **~16:36** / ListMachines **EMPTY**. **Queued** Shared living-host amend on next Docs CONNECTED+Shellable. |
| **Overnight stamp** | Tonight stays Soft-530=**OPEN** + **`soft530_open_since` ~16:36** ([overnight-baseline-stamp.md](overnight-baseline-stamp.md) tip `7226b98`). Do **not** rewrite that stamp from Shared **CLEAR**. |
| **Freeze** | `` `changeme` `` / BUILD_ID **`5swmVz`** / tip **`4cf8924`** — **`last_known`** (Soft-530 OPEN → unverifiable live ≠ DIFF) |
| **Option A** | Redirect+UX **PASS** (rungs 1–2). Public brochure is **LIVE**. Home still **STALE** until **#82**. Redirect+UX **PASS** ≠ Worker body freshness **PASS** / **#82** done |
| **Brochure 502 (Shared old lock)** | **False** since **2026-09-06** unlock. Rewrite dropped it. Do **not** restore. |
| **Combined class** | **Dual OPEN both 1033**. Soft-530 CLEAR + vault OPEN half-state is **OVER**. ≠ dual CLEAR ≠ camp GO ≠ unfreeze ≠ **#82** auto |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Not a Ben ask** | Shared living-host **amend ≠ Ben ask**. This fold does **not** page Ben for Shared rewrite, Shared amend, unfreeze, **#82**, camp, or Garage/Zone. Rewrite is already **DONE**; the class+as-of amend is **queued**. |
| **No Garage / Zone fan-out** | Docs paper only. Shared rewrite / queued amend stay Chief’s standing notes. Do not assign or execute Garage / Zone / Hatch from this fold. |
| **No unfreeze / #82 / camp GO** | Shared amend ≠ those GOs. Soft-530 **OPEN ≠** those GOs. Home **STALE** until **#82**. Camp vault-on-doc stays paper + **Ben GO**. |
| **Don’t leave Shared CLEAR overnight** | ~15:42 rewrite stamped **CLEAR**; live **OPEN** since **~16:36** / ListMachines **EMPTY**. Overnight/morning readers use Docs SSOT, not Shared CLEAR. |
| **Don’t restore 502 language** | Shared brochure “stays 502” was stale and is **dropped**. Vault **1033** remains living; do not collapse those two 502s. |
| **Shared ≠ SSOT** | Discard Shared when it contradicts Docs tip / live. Rewrite must match Docs, not the other way. **DONE ≠** Shared is now SSOT. Queued amend still **non-SSOT**. |
| **Don’t keep “in progress”** | The rewrite landed ~15:42 America/Edmonton. “Rewrite in progress” is **false**. The **queued** living-host amend is a later same-day flip, not a rewrite rewind. |
| **Never `Mac.lan` as Doc** | Next Shared living-host amend waits on asserted Docs **CONNECTED+Shellable** (`95a229f5`). Identity lock unchanged. |

---

## Do not

- Treat Fleet Shared `shop-os-mc-plan.md` as living-ops SSOT
- Leave Shared living-host **CLEAR** after a same-day live **OPEN** flip for overnight / morning readers
- Skip Soft-530 **class + as-of wall** on Shared living-host lines
- Execute the queued Shared amend from this Docs fold, from ABSENT, or from CONNECTED+Shell-unreachable
- Shell `Mac.lan` as the Shared living-host amend host
- Treat the queued Shared amend as a Ben ask, **#82**, unfreeze, or camp Zone
- Copy Shared “brochure stays 502” or a Garage-blocked-on-502 lock into Docs
- Fan out Garage / Zone / Hatch from this paper
- Re-ask Ben
- Unfreeze Doc, GO **#82**, or camp-cutover from this fold
- Collapse Soft-530 **CLEAR** into dual CLEAR / unfreeze / **#82** auto
- Restore brochure-502 language
- Keep “Shared rewrite in progress” after the ~15:42 America/Edmonton receipt
- Rewrite tonight’s overnight stamp away from Soft-530=**OPEN** + **`soft530_open_since` ~16:36**

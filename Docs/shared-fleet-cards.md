# Shared fleet cards — Docs SSOT (held #70)

**Status:** Paper — Chief standing-notes hygiene. **Not SSOT.**  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (Reality one-liner · living-ops / Locks), [deployment-guide.md](deployment-guide.md) (Monday paper map), [home-lab-specification.md](home-lab-specification.md) (host split), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (camp vault-on-doc), [unfreeze-readiness.md](unfreeze-readiness.md) (freeze / draft ≠ GO)

Fleet Shared `shop-os-mc-plan.md` is **stale** and **non-SSOT**. Prefer this thin card + the STATUS Reality one-liner. Do **not** dual-author living ops on Shared.

Merging this file is **not** a Shared rewrite execute, **not** a Garage/Zone fan-out, **not** a Ben ask, and **not** unfreeze / **#82** / camp GO.

---

## SSOT lock

| Lock | Meaning |
|------|---------|
| **`Coombzy/Project-Car` `Docs/` is SSOT** | Held **#70** → `main` is the product / living-ops source of truth. Shared fleet cards are **Chief standing notes only**. |
| **Shared must not contradict Docs tip / live** | If Shared language disagrees with Docs tip or live, **discard Shared language**. Do not “reconcile” by rewriting Docs toward Shared. |
| **Shared rewrite is in progress** | Chief is rewriting Shared `shop-os-mc-plan.md`. That rewrite **must match Docs**. This paper notes the rewrite; it does **not** land Shared text in this repo. |

---

## What the Shared rewrite must drop / align

Chief’s Shared `shop-os-mc-plan.md` rewrite (outside this repo) must:

| Do | Do not |
|----|--------|
| **Drop the brochure 502 lock** | Restore “brochure stays 502” language. Public `projectcar.ca` is **LIVE** (Option A) since the **2026-09-06** unlock — Shared “stays 502” is **false**. |
| **Drop the Garage block** | Fan out Garage / Zone / Hatch from Shared or from this Docs fold. |
| **Align host split** | Invent a second host map. Docs SSOT: [home-lab-specification.md](home-lab-specification.md) + STATUS Host split. Home/lab: Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC). |
| **Align freeze** | Treat freeze as lifted. Living pin: `` `changeme` `` / BUILD_ID **`5swmVz`** / tip **`4cf8924`** until **Ben GO**. |
| **Align camp vault-on-doc** | Treat parked McKing shop-host / vault-stay-up as camp SSOT. Camp SSOT is [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) — **Ben GO**, never auto. |
| **Align Soft-530 CLEAR ≠ dual CLEAR ≠ #82 auto** | Collapse Soft-530 **CLEAR** into dual CLEAR, Doc unfreeze, or **#82** Worker-live. Living is **half-state**. |

Vault **OPEN 502** (McKing origin since ~19:45 MT Sep 13) stays living honesty. That is **not** the brochure 502 lock. Do **not** restore brochure-502 language while recording vault 502.

---

## Living this fold (honesty)

| Plane / pin | Living class |
|-------------|--------------|
| **Soft-530 (Doc)** | **CLEAR** — `api.` `/health` **200**; waitlist OPTIONS = Origin CORS preflight (**bare 405 ≠ OPEN**) |
| **Vault (McKing)** | **OPEN 502** since ~19:45 MT Sep 13 (**not** 1033; docker dead — **not** CLEAR) |
| **Freeze** | `` `changeme` `` / BUILD_ID **`5swmVz`** / tip **`4cf8924`** — live-verify **PASS** (confirmed frozen, **not** lifted) |
| **Option A** | Redirect+UX **PASS** (rungs 1–2). Public brochure is **LIVE**. Home still **STALE** until **#82**. Redirect+UX **PASS** ≠ Worker body freshness **PASS** / **#82** done |
| **Brochure 502 (Shared stale)** | **False** since **2026-09-06** unlock. Do **not** copy Shared “stays 502” into Docs. |
| **Half-state** | Soft-530 **CLEAR** + vault **OPEN** ≠ dual CLEAR ≠ camp GO ≠ unfreeze ≠ **#82** auto |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Not a Ben ask** | This fold does **not** page Ben for Shared rewrite, unfreeze, **#82**, camp, or Garage/Zone. |
| **No Garage / Zone fan-out** | Docs paper only. Shared rewrite stays Chief’s standing notes. Do not assign or execute Garage / Zone / Hatch from this fold. |
| **No unfreeze / #82 / camp GO** | Soft-530 **CLEAR ≠** those GOs. Home **STALE** until **#82**. Camp vault-on-doc stays paper + **Ben GO**. |
| **Don’t restore 502 language** | Shared brochure “stays 502” is stale. Vault **502** remains living; do not collapse those two 502s. |
| **Shared ≠ SSOT** | Discard Shared when it contradicts Docs tip / live. Rewrite must match Docs, not the other way. |

---

## Do not

- Treat Fleet Shared `shop-os-mc-plan.md` as living-ops SSOT
- Copy Shared “brochure stays 502” or a Garage block into Docs
- Fan out Garage / Zone / Hatch from this paper
- Re-ask Ben
- Unfreeze Doc, GO **#82**, or camp-cutover from this fold
- Collapse Soft-530 **CLEAR** into dual CLEAR / unfreeze / **#82** auto
- Restore brochure-502 language

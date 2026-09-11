# Lookout resume — `projectcar-api-health-watch` re-arm

**Status:** Living ops (Lead + Lookout checklist) — **plan only**  
**Updated:** 2026-09-08  
**Related:** `STATUS.md` (Live Shop API / Ops), `api-stay-up.md` (Health / Ownership), `website-improvements.md` **P4-5**, `deployment-guide.md`, `doc-unfreeze.md` (Ben GO pull — **not** this flip), `doc-lid-restore.md` (process wake — **not** this flip)

Ordered re-arm of Lookout **`projectcar-api-health-watch`** after a **successful Doc unfreeze** (`doc-unfreeze.md`) **or** an **explicit Ben resume GO**. This file is the sequence. It is **not** a production flip.

Merging this file is **not** `enabled:true`, **not** a Doc pull, and **not** a substitute for Ben’s unfreeze GO or an explicit resume GO.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, Cloudflare ↔ GitHub auth, or About P3-2 / P3-3.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **This file is not the flip** | Do **not** set `enabled:true` from a docs PR. Garage / Zone / Chief do **not** re-arm from merge. |
| **Two valid starts** | (1) Doc unfreeze finished (`doc-unfreeze.md` steps 5–7) **or** (2) Ben said **GO** to resume Lookout — in words. |
| **Baseline while 200** | Do **not** enable on a public **502 / 530 / 1033**. First sample must be a healthy **200**. |
| **Lead interim until then** | While the watch is paused, **Lead** owns the morning/public probe (held **#75** / `STATUS.md` / `api-stay-up.md`). Lookout owns it **after** this checklist. |
| **No GET-allow nag** | Do **not** re-nag Ben to allow GET. The watch already exists. This is `enabled` + ownership, not a new allow. |
| **Tip stays on #70** | Do **not** fold Reality tip onto this file or this PR. Held **#70** owns that lane. |

Green Shop OS CI, a docs merge, lid-restore, or Chief standing GO for **this checklist** is **not** a resume GO and is **not** an unfreeze.

---

## Why this is separate from unfreeze and lid-restore

| File | When | What |
|------|------|------|
| **`doc-lid-restore.md`** | Doc slept / lid-close / public **530 / 1033** | Wake processes. Same frozen checkout. **No** `git pull`. **No** Lookout flip. |
| **`doc-unfreeze.md`** | Ben said **GO** to unfreeze | Pull tip, migrate if needed, rebuild shop-web, new `BUILD_ID`, smoke. **No** Lookout flip. |
| **`lookout-resume.md` (this file)** | Unfreeze done **or** Ben said **GO** to resume Lookout | Baseline on **200** → `enabled:true` → short first-window quiet → hand the probe back from Lead interim. |

Do **not** collapse them. A soft morning 530 is **not** resume GO. Finishing unfreeze is a **valid start** for this file — it is still **not** an automatic flip.

---

## Reality today (do not claim this is done)

| Clock | Pin | Meaning |
|-------|-----|---------|
| **Lookout watch** | **`projectcar-api-health-watch`** **paused** (`enabled:false`) | Live synthetic is off. Do **not** treat STATUS “Lookout owns the live probe” on older tips as “the watch is firing.” |
| **Lead interim** | Held **#75** | Morning/public probe is **Lead** until this checklist finishes. `STATUS.md` Live Shop API / Ops, `api-stay-up.md` Health / Ownership, `website-improvements.md` **P4-5**. |
| **Public health** | **200 when Doc origin is up** | Lid-close / sleep still yields Cloudflare **502** or **530 / error 1033**. Expected — not a product break. |
| **Doc checkout** | Frozen at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** until **Ben GO** | Unfreeze is `doc-unfreeze.md`. This file does **not** pull Doc. |

Do **not** call the watch live until step 2 is actually `enabled:true` **and** step 4 has handed ownership back in the living docs.

---

## Ownership (this run)

| Role | Owns | Does not own |
|------|------|----------------|
| **Ben** | Explicit **GO** to resume Lookout if unfreeze is **not** the start. Unfreeze GO stays `doc-unfreeze.md`. | Flipping `enabled`. Morning probe while paused. |
| **Lead** | Confirm public **200** baseline. Interim morning/public probe **until** step 4. Process restore stays Lead (`api-stay-up.md`). | Cloudflare tunnel / DNS. Setting `enabled` (Lookout). Doc pull. |
| **Lookout** | After GO / unfreeze: set `enabled:true` on **`projectcar-api-health-watch`**. Own the live probe **after** step 4. | Process restore. Interim probe while paused. GET-allow nag. |
| **Garage** | Brochure waitlist e2e **after** public health is 200 | Lookout config. uvicorn. Tunnel. |
| **Zone** | Tunnel / DNS only if local origin is healthy but public is still **1033** | Lookout `enabled`. Doc checkout. |
| **Chief** | Standing GO for this **checklist**. Plan-improve. | Substituting for Ben’s resume GO. Flipping `enabled`. uvicorn / shop-web restarts. |

No edge flip. No CF ↔ GitHub re-ask. No Member GO. No `app.` cut. No OAuth implementation. No tip-only finance stamps. No Reality tip fold (held **#70**).

---

## Ordered re-arm (after unfreeze **or** Ben resume GO only)

Run these **in order**. Stop if neither start is true.

### 1. Establish baseline while public `GET /health` is **200**

Do **not** enable on a down edge. The first Lookout sample must be healthy, or the watch learns a flap as “normal” / pages on the recovery.

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
# expect 200
# optional, on Doc:
curl -sS http://127.0.0.1:8000/health
# expect {"status":"ok","service":"project-car-api"}
```

| Result | Action |
|--------|--------|
| Public **200** | Record who / when. Continue. |
| **502 / 530 / 1033** | **Stop.** Wake first (`doc-lid-restore.md`). Re-check. Do **not** set `enabled:true`. |
| **403** challenge | Zone (WAF), not Lookout. Do **not** treat as lid-close. |

If the start was **Doc unfreeze**, this is the same class as `doc-unfreeze.md` step 7 — re-confirm it is still **200** *now*, not “it was 200 at rebuild.”

If the start is **Ben resume GO** without unfreeze, that is fine **only** while public health is **200**. Resume GO does **not** unfreeze Doc and does **not** make **#36** / **#69** live.

### 2. Set `enabled:true`

Lookout turns **`projectcar-api-health-watch`** back on. **Lookout only.** Not a docs PR. Not Garage. Not Zone. Not Chief.

| Check | Expect |
|-------|--------|
| Watch name | **`projectcar-api-health-watch`** |
| Target | `GET https://api.projectcar.ca/health` |
| Flag | **`enabled:true`** |

Do **not** invent extra monitors (brochure homepage, Discord invite, Apex `/api/apex/health`). **P4-5** stays **partial**: API health flips + optional brochure 200. Apex stays dropped.

Do **not** re-nag Ben to allow GET.

### 3. Short first-window quiet (morning flaps are not noise)

Lid-close **530 / 1033** is **expected**. The first night / morning after re-arm will flap. That is **not** a new incident and **not** a reason to ping Ben.

| Window | Action |
|--------|--------|
| **First quiet window** | Stay quiet through the **next** expected morning lid-close (or the remainder of the current night if unfreeze landed late). Soft **530 / 1033** → Lead restores (`doc-lid-restore.md`). Do **not** page Ben. |
| **After that window** | Lookout alerts on flips as usual. Still: soft morning 530 is expected lid-close — stay quiet unless Doc will not wake / Grok Bot desktop is offline / the outage is **prolonged**. |

Do **not** skip this quiet because CI is green or because unfreeze just smoked **200**. The Mac still sleeps.

### 4. Hand probe ownership back from Lead interim

After `enabled:true` **and** the first quiet window is understood (step 3), the living docs stop saying Lead owns the morning probe.

| Doc | After this step |
|-----|-----------------|
| **`STATUS.md`** | Live Shop API + Ops: Lookout owns the live probe again. Drop “paused / Lead interim.” **Do not** fold Reality tip (held **#70**). |
| **`api-stay-up.md`** | Health + Ownership: Lookout owns `projectcar-api-health-watch` when enabled. Lead keeps process restore. Drop interim-probe ownership. |
| **`website-improvements.md` P4-5** | Watch is the live path again (**partial** still — Apex dropped; brochure / Discord optional). Do **not** reopen P4-5 status. |
| **`deployment-guide.md`** | Index points at this file as **done** (or drop the paused-interim row). |
| **Held #75** | That lane is **satisfied** once the docs above match re-armed reality. Do **not** amend #75 from this checklist if it is already merged; follow-up on `main`. |

Lead **still** owns uvicorn / shop-web KeepAlive restore. Lookout **alerts**; Lookout does **not** restart Doc.

---

## After a successful re-arm

- `projectcar-api-health-watch` is **`enabled:true`**.
- Baseline was a public **200**.
- First-window quiet was observed (or is in force for the next morning).
- Living docs no longer assign the morning probe to Lead interim.
- Lid-restore **stays** process-only. A later morning 530 is still wake-only — **not** a new pause and **not** a new unfreeze.
- Doc checkout freeze / unfreeze is unchanged by this file.

---

## Do not

- Flip `enabled` from a docs PR, from Chief standing GO, or from green `shop-os-ci`
- Re-arm while public `GET /health` is **502 / 530 / 1033**
- Treat lid-restore or a soft morning 530 as resume GO
- Treat Doc unfreeze merge (the checklist file) as this flip — unfreeze **done** is a valid **start**, not an automatic `enabled:true`
- Re-nag Ben to allow GET
- Hand process restore to Lookout, Garage, Zone, or Chief
- Invent extra shipped monitors (Apex, Discord, brochure-required)
- Amend held **#70** (Reality tip), **#75** (Lead interim), **#76**, or **#77** from this file
- Fold Reality tip onto this PR
- Execute Member GO, `app.` cut, Mission Control cockpit, or About P3-2 / P3-3
- `git pull` / rebuild Doc from this file

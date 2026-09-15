# Unfreeze readiness — draft Ben-GO gates (before any pull)

**Status:** Paper — Lead may **draft** only. **draft ≠ GO**  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (living-ops / Locks · freeze **`4cf8924` / `5swmVz` / `changeme`** · Next **#79** · [post-dual-clear-go.md](post-dual-clear-go.md) Shop OS **#79.1** acceptance smoke), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (extended-OPEN Soft-530 **CLEAR** first card + freeze live-verify — **before** this draft), [doc-unfreeze.md](doc-unfreeze.md) (ordered **Ben GO** pull — **after** GO, not this file), [post-dual-clear-go.md](post-dual-clear-go.md) (**#79.1** acceptance smoke is lane-done **after** GO+pull+rebuild — not “next after **#82**”; this file does **not** enter that menu), [ops-demo-hardening.md](ops-demo-hardening.md) (Garage **#79.1** strip — git-only until the pull), [cors-origins.md](cors-origins.md) (Owner seed / waitlist CORS draft), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Soft-530 **CLEAR** + freeze live-verify **PASS** + Doc HEAD **`4cf8924`** **~89** behind `origin/main` means Lead can **draft** the Ben-GO gates **before** any `git pull` / unfreeze. This file is that draft card.

Merging this file is **not** a pull, **not** a rebuild, **not** Ben GO, and **not** a substitute for [doc-unfreeze.md](doc-unfreeze.md). Garage / Zone / Hatch do **not** execute from this paper. **No Ben re-nag.**

Do **not** invent a shop opening, Stripe, Member host migration, `app.` cut, Mission Control cockpit, Cloudflare ↔ GitHub auth, About P3-2 / P3-3, vault CLEAR, dual CLEAR, **#82** Worker-live, or Bitwarden from this fold.

---

## Why this card exists (tip-fold)

| Already true | Still not true |
|--------------|----------------|
| Soft-530 **CLEAR** (`api.` `/health` **200**; waitlist OPTIONS = Origin CORS preflight — **bare 405 ≠ OPEN**) | Dual CLEAR. Vault is still **OPEN 502**. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md). |
| Freeze live-verify **PASS** — public `app.`/`ops.` `/login` still print `` `changeme` `` on BUILD_ID **`5swmVz`** / tip **`4cf8924`** | Unfreeze. Live-verify **PASS** = freeze **confirmed**, not lifted. |
| Doc HEAD **`4cf8924`** is **~89** behind `origin/main` (paper stamp this fold) | License to `git pull`. Behind-count is the reason to **draft**, not to pull. |

[soft-530-clear-smoke.md](soft-530-clear-smoke.md) already ran (or its five-row class is living **CLEAR**). Freeze live-verify is **now allowed** after that CLEAR and is **PASS** this fold. Those two + the behind-count unlock **drafting** only.

Finance / CCJ / SPCX / BTC tip-of-main can inflate a raw `git rev-list 4cf8924..origin/main` count. Product Reality tip stays **`2dd61a2` / #74**. The **~89** figure is the living paper stamp — do **not** treat a later finance-only tip as a new unfreeze delta.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **draft ≠ GO** | Lead may write the five gates below on paper. That is **not** Ben GO to unfreeze. It is **not** [doc-unfreeze.md](doc-unfreeze.md) step 1. Do **not** `git pull`, migrate, rebuild, or strip public `changeme` from this file. |
| **Vault OPEN does not block drafting** | Living vault **OPEN 502** blocks the **post-dual-CLEAR menu** ([post-dual-clear-go.md](post-dual-clear-go.md)). It does **not** block Lead from **drafting** these Shop OS unfreeze gates. Half-state ≠ dual CLEAR still stands. |
| **Soft-530 CLEAR duration ≠ auto-unfreeze ≠ auto #82** | How long Soft-530 has been **CLEAR** does **not** unfreeze Doc and does **not** GO **#82**. Same class as green `shop-os-ci` and lid-restore process-wake. Soft-530 **CLEAR ≠ #82**. Soft-530 **OPEN ≠ #82 blocked** — brochure is CF Worker/Zone, not this card. |
| **This file is not the pull** | Do not execute from a docs PR. Garage / Zone / Hatch do **not** pull Doc. **No Ben re-nag.** |
| **#79.1 acceptance is later** | Lane-done after Ben GO + pull + Garage rebuild is [post-dual-clear-go.md](post-dual-clear-go.md) **Shop OS parallel — unfreeze + #79.1 acceptance smoke**. This draft is **before** that talk. Soft-530 CLEAR alone ≠ that card. |

---

## Draft gates (paper — not execute)

Draft these **five** so a later Ben GO has a written ask. Stop if the draft starts to look like a pull.

### 1. `origin/main` delta skim

Doc is frozen at **`4cf8924`** / Dashboard **#28**. A Ben-GO pull lands **`main`**, not this held **#70** branch.

**Draft (do not pull):** what Shop OS / stay-up paper would land after `4cf8924` — at least host allowlist **#36** (`f952cd3`), OwnerShell **#69** (`b9f9019`), google-calendar-oauth plan **#71**, lid-restore no-auto-pull **#72**, Shop OS CI **#73**, [doc-unfreeze.md](doc-unfreeze.md) checklist **#74**. Brochure Worker **#52–#67** / Soft-530 **#80** are already Worker-live — **not** a Doc rebuild. Garage **#79.1** strip, if on `main`, stays **git-only** until this pull + rebuild.

**Not this skim:** finance / CCJ / SPCX / BTC tips. **Not** held **#70** docs. **Not** a `git fetch` / `git pull` on Doc from this paper.

### 2. Alembic / migrations

Shop data is dedicated Postgres 16 — never Nextcloud MariaDB. Essay after GO: [doc-unfreeze.md](doc-unfreeze.md) step 3.

**Draft:** freeze already shipped `20260906_0007` (todos / parts POs / calendar scaffold). **#36** / **#69** are shop-web only. No later `alembic/versions` revision is known on `origin/main` after **`4cf8924`**. Expect `alembic current` **equals** `heads` after a later GO pull unless a new revision lands first.

**Not this draft:** `alembic upgrade` / `downgrade`. Do **not** re-seed unless Ben asked.

### 3. Owner seed / CORS

**Draft:**

| Keep after a later GO | Do not |
|-----------------------|--------|
| Owner seed `owner@projectcar.ca` + env `OWNER_PASSWORD` / `MEMBER_DEMO_PASSWORD` (localhost / seed note) | Re-seed from this paper. Print `` `changeme` `` in public `/login` HTML is **freeze**, not a seed bug |
| `CORS_ORIGINS` apex **and** www **and** `ops.` **and** temporary `app.` ([cors-origins.md](cors-origins.md)) | Drop `app.` from a docs PR. Treat Soft-530 CLEAR OPTIONS CORS as a pull trigger |

Waitlist OPTIONS CORS (apex + www) is already Soft-530 **CLEAR** proof on [soft-530-clear-smoke.md](soft-530-clear-smoke.md). That is **not** unfreeze GO.

### 4. Rollback to `4cf8924` / `5swmVz`

**Draft** the abort if a later GO pull / rebuild goes bad:

| Pin | Rollback target |
|-----|-----------------|
| Git | Doc checkout **`4cf8924`** |
| shop-web | `.next/BUILD_ID` **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) |
| Public honesty | `app.`/`ops.` `/login` may print `` `changeme` `` again — expected freeze, not Soft-530 |

Do **not** invent a future `BUILD_ID`. Do **not** run rollback from this paper. Lid-restore stays process-only if the public hosts 530 / 1033 during a later attempt.

### 5. Garage **#79.1** — parallel, not next-after

**Draft:** Garage **#79.1** strip-changeme is **Shop OS parallel** — **not** “next after **#82**” in place of Bulk / **#83**. After Ben GO unfreeze + pull + rebuild, lane-done is [post-dual-clear-go.md](post-dual-clear-go.md) **unfreeze + #79.1 acceptance smoke**:

1. Public `app.` + `ops.` `/login` HTML no longer prints Password `` `changeme` ``
2. Tip / `BUILD_ID` ≠ `4cf8924` / `5swmVz`
3. `api.` `/health` **200** + waitlist OPTIONS CORS Origin `https://projectcar.ca` **and** www
4. **#79.1** merge-alone **without** this pull does **not** clear public `changeme`

Soft-530 **CLEAR** alone ≠ that card. This draft does **not** start Garage. Merge of **#79.1** on `main` stays git-only while freeze holds.

---

## Living this fold (honesty)

| Plane / pin | Living class |
|-------------|--------------|
| **Soft-530 (Doc)** | **OPEN 530 / CF 1033** — `api.` / `app.` / `ops.` (Lookout + Lead **~16:36**; **was CLEAR**). Half-state **OVER**. Draft paper stays; **draft ≠ GO**. |
| **Vault (McKing)** | **OPEN 530 / CF 1033** connector-down (was 502 since ~19:45 MT Sep 13 — **not** CLEAR) |
| **Freeze** | **`4cf8924`** / BUILD_ID **`5swmVz`** / public `` `changeme` `` — **`last_known`** (Soft-530 OPEN → unverifiable ≠ DIFF) |
| **Option A** | Redirect+UX **PASS** (rungs 1–2). Home still **STALE** until **#82** (canonical/`og:url` + nav Home bare `/`; sitemap loc bare `/`, lastmod **2026-09-08**). Redirect+UX **PASS** ≠ Worker body freshness **PASS** / **#82** done |
| **Doc vs `main`** | HEAD **`4cf8924`** **~89** behind `origin/main` — draft reason, **not** pull license |
| **Combined class** | **Dual OPEN both 1033**. Soft-530 CLEAR + vault OPEN half-state is **OVER**. Vault OPEN **does not** block **this draft**. Still **do not enter** the post-dual-CLEAR menu |

**No Ben re-nag.** Soft-530 **CLEAR** duration ≠ auto-unfreeze ≠ auto **#82**. This paper executes **none** of the curls, pulls, or rebuilds.

---

## Not the #79.1 acceptance smoke

| Card | When | What |
|------|------|------|
| **[soft-530-clear-smoke.md](soft-530-clear-smoke.md)** | First thing after extended-OPEN Soft-530 **CLEAR** | Route-alive. `changeme` on `/login` is **expected freeze**. Freeze live-verify **PASS** lives here / STATUS. |
| **This file** | After that CLEAR + freeze live-verify **PASS** + behind-count | Lead **drafts** Ben-GO gates. **draft ≠ GO.** Vault OPEN does **not** block drafting. |
| **#79.1 acceptance** | After Ben GO unfreeze + pull + Garage **#79.1** rebuild | Public `/login` **no longer** prints `` `changeme` ``; tip / `BUILD_ID` ≠ `4cf8924` / `5swmVz`. [post-dual-clear-go.md](post-dual-clear-go.md) Shop OS card. |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **draft ≠ GO** | A written gate list is not Ben saying **GO**. Do not pull from a complete draft. |
| **Vault OPEN ≠ draft blocked** | Half-state blocks the **menu**, not this paper. Do not wait on vault CLEAR to *write* the gates. |
| **Soft-530 CLEAR duration ≠ auto-unfreeze ≠ auto #82** | CLEAR clock does not lift freeze and does not upload Worker. |
| **Behind-count ≠ pull** | **~89** (or a later `rev-list`) is skim fuel. Finance tip-of-main is not Shop OS. |
| **Freeze live-verify PASS ≠ unfreeze** | Confirmed `` `changeme` `` / **`5swmVz`** means the pin holds. |
| **This draft ≠ #79.1 acceptance** | Acceptance is after GO+rebuild. Merge-alone still does not clear public `changeme`. |
| **This draft ≠ #82 / Zone / Bitwarden / camp GO** | Brochure and vault stay on their own papers. Soft-530 **CLEAR ≠ #82**. Home **STALE** until **#82**. |
| **No Ben re-nag** | Do not ping Ben because the draft exists, because Soft-530 stayed CLEAR, or because vault stayed 502. |

---

## Do not

- `git pull` / rebuild / alembic / re-seed from this paper
- Treat a finished draft as Ben GO or as [doc-unfreeze.md](doc-unfreeze.md) step 1
- Enter [post-dual-clear-go.md](post-dual-clear-go.md) while vault is **OPEN 502**
- Block this **draft** on vault OPEN
- Treat Soft-530 **CLEAR** duration as auto-unfreeze or auto **#82**
- Call **#36** / **#69** / **#79.1** live on Doc from git SHA or from this draft
- Put unfreeze + **#79.1** “next after **#82**” in place of Bulk / **#83**
- Execute Garage / Zone / Hatch / Lookout arm from this fold
- Re-nag Ben
- Invent vault CLEAR, dual CLEAR, or Home freshness **PASS**

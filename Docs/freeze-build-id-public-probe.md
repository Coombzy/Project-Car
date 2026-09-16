# Freeze BUILD_ID public probe — split from git verify

**Status:** Paper — public BUILD_ID scrape + waitlist path SSOT, **not** a GO  
**Updated:** 2026-09-16 ~08:16 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **CLEAR ≥51m** since **~07:25** + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY** + **`freeze_build_id_public=true`** + this pointer), [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) (Soft-530 = public HTTP; local-exec = ListMachines+Shellable; **EMPTY ≠ Soft-530 OPEN**; this file extends that split onto freeze), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (may record **`freeze_build_id_public=true`** on half-ops; full **`freeze_git_verified`** still waits on Shellable), [unfreeze-readiness.md](unfreeze-readiness.md) (draft still needs full freeze live-verify **PASS** = **`freeze_git_verified`**), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (freeze field now splits public BUILD_ID vs git verify), [cors-origins.md](cors-origins.md) (waitlist smoke SSOT = **`/waitlist`**), [post-dual-clear-go.md](post-dual-clear-go.md) (camp vault-on-Doc still **half-ops HOLD** while EMPTY), [shared-fleet-cards.md](shared-fleet-cards.md) (Shared **CLEAR since ~07:25** amend still **Chief** when Shellable), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Soft-530 **CLEAR** while ListMachines is **EMPTY** does **not** make public `app.`/`ops.` `/login` unverifiable. Scrape `"b":"…"` from the public HTML. That stamp is **`freeze_build_id_public`**. Full freeze live-verify is still **`freeze_git_verified`** — Docs **CONNECTED+Shellable** + Doc checkout HEAD match.

This fold executes **none** of the Shells, curls, hops, or GOs. Do **not** invent vault CLEAR, dual CLEAR, **#82**, unfreeze, **#79.1**, camp Zone, Bitwarden, a Shared amend, or freeze live-verify **PASS** from a public BUILD_ID match.

---

## Split freeze checks

| Stamp | What it is | When it may record | What it is not |
|-------|------------|--------------------|----------------|
| **`freeze_build_id_public`** | Scrape `"b":"…"` from public `https://app.projectcar.ca/login` and/or `https://ops.projectcar.ca/login` while Soft-530 is **CLEAR**. Match last_known **`5swmVz-T2CqKEQzTk1ifU`**. Soft-530 class (public HTTP). | Half-ops **HOLD**. ListMachines **EMPTY**. Lead public scrape — **no** Docs Shell. | Freeze live-verify **PASS**. Unfreeze. **#82**. **#79.1**. Shared amend GO. Soft-530 **OPEN**. |
| **`freeze_git_verified`** | Docs **CONNECTED+Shellable** + Doc checkout `/Users/dochak/src/Project-Car` HEAD **`4cf8924`** + disk `.next/BUILD_ID` + behind-count. Local-exec class. | **Required** for full freeze live-verify. Still **queued** while EMPTY. | Public `"b"` scrape. Shared living-host write. Auto-pull. |

**Both true** = freeze live-verify **PASS** (pin holds, not lifted). **`freeze_build_id_public=true` alone** = public BUILD_ID **MATCH** — **not** that PASS.

While Soft-530 is **OPEN** (530 / CF 1033), public `/login` cannot be live-probed — stay **`last_known`**. That is **not** this card. This card applies **after** Soft-530 **CLEAR**.

`` `changeme` `` print / `/login` **307** alone is still **not** either stamp.

---

## Living proof (~08:16 America/Edmonton)

| Field | Living |
|-------|--------|
| **Soft-530** | **CLEAR ≥51m** — Lead `api.` `/health` **200** ok; `app.` + `ops.` **307**. **`soft530_clear_since` ~07:25**. Do **not** stamp **OPEN** because EMPTY. Do **not** stamp **OPEN** because public BUILD_ID still serves. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined HTTP** | Soft-530 **CLEAR** + vault **OPEN** = **half-state**. **≠ dual CLEAR.** |
| **ListMachines** | **EMPTY**. Local-exec **ABSENT**. **CONNECTED ≠ Shellable ≠ tunnel healthy.** |
| **Combined ops** | Soft-530 **CLEAR** + local-exec **EMPTY** = **half-ops HOLD**. SAME-CLASS dwell now **≥51m** (gate 1 **PASS**). Gate 2 Shellable still **fail**. |
| **Option A** | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Public `/login` BUILD_ID** | **`5swmVz-T2CqKEQzTk1ifU`** — scrape `"b":"…"` on `https://app.projectcar.ca/login` (and/or `ops.`) **MATCH** last_known. **`freeze_build_id_public=true`**. |
| **`freeze_git_verified`** | still **queued** until Docs **CONNECTED+Shellable**. ~06:57 PASS is last_known git evidence. **Never auto-pull.** |
| **Shared** | **`shared_fleet_card_stale=true`**. CLEAR-since-**~07:25** amend still **Chief** after Shellable. Public BUILD_ID match **≠** Shared amend GO. |
| **Camp / post-dual-clear-go** | still **half-ops HOLD**. Public BUILD_ID match **≠** camp GO reopen. |

Receipt: [overnight_2026-09-16_0816_freeze_build_id_public_probe.md](overnight_2026-09-16_0816_freeze_build_id_public_probe.md). Prior half-ops class receipt stays [overnight_2026-09-16_0751_clear_vs_local_exec_verify.md](overnight_2026-09-16_0751_clear_vs_local_exec_verify.md) — **same Soft-530 class**, now aged ≥51m, with public BUILD_ID **MATCH**.

**Do not** leave BUILD_ID as unverified solely because ListMachines is **EMPTY**. Public login still serves the frozen build.

---

## How to scrape (Lead — after Soft-530 CLEAR)

Public HTML, not Doc disk. Soft-530 **CLEAR** is the gate. Shellable is **not**.

```bash
# ONLY after a live Soft-530 CLEAR — not this paper
# public scrape — no Docs Shell required
# curl -sS -L https://app.projectcar.ca/login | grep -oE '"b":"[^"]+"'
# expect "b":"5swmVz-T2CqKEQzTk1ifU"
# optional twin:
# curl -sS -L https://ops.projectcar.ca/login | grep -oE '"b":"[^"]+"'
```

Record **`freeze_build_id_public=true`** on MATCH. `"b"` ≠ `5swmVz*` → freeze **DRIFT** (Lead lane) — still ≠ auto-unfreeze / ≠ Ben nag.

[soft-530-clear-smoke.md](soft-530-clear-smoke.md) **may** record this on half-ops. Row **6** (`freeze_git_verified`) still waits on **CONNECTED+Shellable**.

---

## Extends ddc9b84 — what still needs Shellable

Public BUILD_ID is Soft-530 class. These stay **local-exec** — still **queued** until Docs **CONNECTED+Shellable**:

| Still queued | Why |
|--------------|-----|
| Shared living-host amend **CLEAR since ~07:25** (blip noted) | Chief write on Doc Shared. **≠** public BUILD_ID. |
| Camp vault-on-Doc **Ben GO** re-offer | Gate = ≥30m SAME-CLASS **AND** Shellable. Dwell **PASS** at ~08:16; Shellable still **fail**. |
| Full **`freeze_git_verified`** / freeze live-verify **PASS** | Doc checkout `/Users/dochak/src/Project-Car` only. |
| Full [soft-530-clear-smoke.md](soft-530-clear-smoke.md) on-host + lid-restore / KeepAlive | Local-exec. |

Essay this extends: [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) (`ddc9b84`).

---

## Waitlist smoke SSOT = `/waitlist`

Brochure + Shop API waitlist is **`https://api.projectcar.ca/waitlist`**.

| Path | Class |
|------|-------|
| **`/waitlist`** | **SSOT.** OPTIONS Origin CORS + POST **422**/**201**. Brochure `waitlist.js` POSTs here. |
| **`/api/waitlist`** | **False friend.** OPTIONS **200** CORS there is **not** waitlist route-alive. POST **404**. Do **not** stamp Soft-530 CLEAR / waitlist smoke from that OPTIONS. |

Cross [cors-origins.md](cors-origins.md) · [soft-530-clear-smoke.md](soft-530-clear-smoke.md).

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Public BUILD_ID MATCH ≠ freeze live-verify PASS** | Missing **`freeze_git_verified`**. Pin holds on paper; PASS needs Doc checkout. |
| **Public BUILD_ID MATCH ≠ unfreeze / #82 / #79.1** | Each is a **separate Ben GO**. |
| **Public BUILD_ID MATCH ≠ Shared amend GO** | Shared write is local-exec. Still **Chief** when Shellable. |
| **EMPTY ≠ Soft-530 OPEN when public BUILD_ID still serves** | Serving `"b":"5swmVz…"` **is** Soft-530 **CLEAR** evidence. Do **not** flip OPEN because ListMachines is EMPTY. |
| **EMPTY ≠ leave BUILD_ID unverified** | Public scrape is allowed on half-ops. |
| **`/api/waitlist` OPTIONS 200 ≠ waitlist smoke** | False friend. POST **404**. SSOT is **`/waitlist`**. |
| **CLEAR + EMPTY ≠ dual CLEAR / camp GO** | Vault still **OPEN 1033**. Shellable still **fail**. |

**#82** Ben GO / companions **HOLD** / freeze `4cf8924` / `5swmVz` / vault subclass 502 vs 1033 — **unchanged**. This file executes **none** of those.

---

## Do not

- Leave BUILD_ID **unverified** solely because ListMachines is **EMPTY**
- Stamp Soft-530=**OPEN** because EMPTY while public `/login` still serves `"b":"5swmVz…"`
- Treat **`freeze_build_id_public=true`** as freeze live-verify **PASS** / **`freeze_git_verified`**
- Treat public BUILD_ID MATCH as unfreeze / **#82** / **#79.1** / Shared amend / camp GO
- Amend Shared or re-verify git freeze while EMPTY / **CONNECTED≠Shellable**
- Smoke waitlist at **`/api/waitlist`**
- Auto-pull because freeze is behind
- Re-nag Ben (quiet)
- Treat `Mac.lan` as Doc

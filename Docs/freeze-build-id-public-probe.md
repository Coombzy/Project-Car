# Freeze BUILD_ID public probe — split from git verify

**Status:** Paper — public BUILD_ID scrape + waitlist path SSOT, **not** a GO  
**Updated:** 2026-09-16 ~08:41 America/Edmonton  
**Related:** `STATUS.md` (living Soft-530 **OPEN** **`soft530_open_since` ~08:41** + vault **OPEN 530 / CF 1033** + ListMachines **EMPTY** + **`freeze_build_id_public` last_known** + this pointer), [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) (Soft-530 = public HTTP; **EMPTY ≠ cause of OPEN**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (may record **`freeze_build_id_public=true`** on half-ops; full **`freeze_git_verified`** still waits on Shellable), [unfreeze-readiness.md](unfreeze-readiness.md) (draft still needs full freeze live-verify **PASS** = **`freeze_git_verified`**), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (while OPEN, freeze stays **`last_known`** — login **530** unverifiable ≠ DIFF), [cors-origins.md](cors-origins.md) (waitlist smoke SSOT = **`/waitlist`**), [post-dual-clear-go.md](post-dual-clear-go.md) (camp vault-on-Doc **HOLD** while OPEN / EMPTY), [shared-fleet-cards.md](shared-fleet-cards.md) (Shared amend **HOLD** until next CLEAR + ≥30m + Shellable), [deployment-guide.md](deployment-guide.md) (Monday paper map)

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

## Living proof (~08:16 MATCH; ~08:41 OPEN → unreachable)

| Field | Living |
|-------|--------|
| **Soft-530** | **OPEN** — Lookout `api.` **200→530** CF **1033**; Lead `api.` / `app.` / `ops.` all **530 / CF 1033**. **`soft530_open_since` ~08:41**. Prior CLEAR dwell **~07:25–~08:41** **ENDED**. |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical). |
| **Vault** | still **OPEN 530 / CF 1033** — **EXPECTED**. ≠ vault CLEAR. |
| **Combined HTTP** | Soft-530 **OPEN** + vault **OPEN** (both **1033**). **≠ dual CLEAR.** |
| **ListMachines** | **EMPTY**. Local-exec **ABSENT**. **EMPTY ≠ cause of OPEN.** **CONNECTED ≠ Shellable ≠ tunnel healthy.** |
| **Combined ops** | Camp / Shared **HOLD** until next CLEAR + ≥30m + Shellable. |
| **Option A** | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`). Home **STALE** until **#82**. |
| **Public `/login` BUILD_ID** | **`last_known` `5swmVz-T2CqKEQzTk1ifU` MATCH** (~08:16). Living **OPEN** → login **530** — scrape **unreachable**. That is **not** a freeze DIFF. |
| **`freeze_git_verified`** | still **queued** until Docs **CONNECTED+Shellable**. ~06:57 PASS is last_known git evidence. **Never auto-pull.** |
| **Shared** | **`shared_fleet_card_stale=true`**. Amend **HOLD** until next CLEAR + ≥30m + Shellable. |
| **Camp / post-dual-clear-go** | **must not reopen**. Public MATCH ≠ camp GO. |

Receipt: [overnight_2026-09-16_0841_open_verify.md](overnight_2026-09-16_0841_open_verify.md). Prior public MATCH: [overnight_2026-09-16_0816_freeze_build_id_public_probe.md](overnight_2026-09-16_0816_freeze_build_id_public_probe.md).

While Soft-530 is **OPEN**, do **not** curl `app.`/`ops.` `/login` to “refresh” last_known. After the **next** CLEAR, scrape again — **EMPTY ≠ leave BUILD_ID unverified**.

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

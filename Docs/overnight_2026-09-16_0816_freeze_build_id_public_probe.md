# Overnight verify — 2026-09-16 ~08:16 America/Edmonton

**Status:** Thin paper receipt — not a GO  
**Updated:** 2026-09-16 ~08:16 America/Edmonton  
**Held:** #70 · [freeze-build-id-public-probe.md](freeze-build-id-public-probe.md) · [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) · [soft-530-clear-smoke.md](soft-530-clear-smoke.md) · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · [STATUS.md](STATUS.md) Reality  
**Prior:** [overnight_2026-09-16_0751_clear_vs_local_exec_verify.md](overnight_2026-09-16_0751_clear_vs_local_exec_verify.md) (CLEAR+EMPTY half-ops — **same Soft-530 class**, now aged ≥51m)

Soft-530 **CLEAR** held **≥51m** (~07:25–~08:16) while ListMachines stayed **EMPTY**. Public `https://app.projectcar.ca/login` BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** **MATCH** last_known. Do **not** leave BUILD_ID unverified because EMPTY. Do **not** stamp Soft-530 **OPEN** because EMPTY. Camp vault-on-Doc / [post-dual-clear-go.md](post-dual-clear-go.md) stays **half-ops HOLD**.

| Assert | Result |
|--------|--------|
| Soft-530 class | **CLEAR** · **`soft530_clear_since` ~07:25** · dwell **≥51m** (SAME-CLASS dwell **PASS**) |
| Local-exec class | ListMachines **EMPTY** — **ABSENT**. **CONNECTED ≠ Shellable ≠ tunnel healthy** |
| Combined ops | **half-ops HOLD** — CLEAR + EMPTY. **EMPTY ≠ Soft-530 OPEN** |
| **`soft530_open_blip`** | **~07:06–~07:25** (historical) |
| Lead public | `api.` `/health` **200** ok; `app.` + `ops.` **307** |
| Vault | still **OPEN 530 / CF 1033** — **EXPECTED** |
| Combined HTTP | Soft-530 **CLEAR** + vault **OPEN** — **half-state**. **≠ dual CLEAR** |
| Brochure Option A | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`) |
| Home | still **STALE** until **#82** |
| **`freeze_build_id_public`** | **`true`** — public `/login` `"b":"5swmVz-T2CqKEQzTk1ifU"` **MATCH** |
| **`freeze_git_verified`** | still **queued** until Shellable (~06:57 last_known git evidence; behind **intact**) |
| Freeze live-verify | **not PASS** — public MATCH ≠ git verify |
| `shared_fleet_card_stale` | **`true`** — CLEAR-since-**~07:25** amend still **Chief** when **CONNECTED+Shellable** |
| Camp vault-on-Doc / post-dual-clear-go | **half-ops HOLD** — dwell **PASS**; Shellable **fail** |
| Waitlist SSOT | **`/waitlist`** — **`/api/waitlist`** OPTIONS 200 CORS is a **false friend** (POST **404**) |

**Stamp:** Soft-530=**CLEAR** · **`soft530_clear_since` ~07:25** · dwell **≥51m** · **`soft530_open_blip` ~07:06–~07:25** · vault **OPEN 530/1033 EXPECTED** · ListMachines **EMPTY** · Option A **PASS** · Home **STALE** until **#82** · **`freeze_build_id_public=true`** `` `5swmVz-T2CqKEQzTk1ifU` `` · **`freeze_git_verified` queued** · **`shared_fleet_card_stale=true`** · half-ops **HOLD**.

**Locks:** **EMPTY ≠ Soft-530 OPEN** (public BUILD_ID still serves). Public BUILD_ID MATCH ≠ freeze live-verify PASS / ≠ unfreeze / ≠ **#82** / ≠ **#79.1** / ≠ Shared amend GO. Never treat EMPTY as Soft-530 OPEN when `"b":"5swmVz…"` still prints. Waitlist smoke SSOT = **`/waitlist`**. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md). Quiet Ben.

# Overnight verify — 2026-09-16 ~07:25 America/Edmonton

**Status:** Thin paper receipt — not a GO  
**Updated:** 2026-09-16 ~07:25 America/Edmonton  
**Held:** #70 · [soft-530-blip-recover.md](soft-530-blip-recover.md) · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · [STATUS.md](STATUS.md) Reality  
**Prior:** [overnight_2026-09-16_0706_open_verify.md](overnight_2026-09-16_0706_open_verify.md) (CLEAR→OPEN ~07:06 flap-while-connected — **superseded as living**)

Soft-530 **OPEN** blip **~07:06–~07:25** then **CLEAR** again. ListMachines **EMPTY**. Camp vault-on-Doc / [post-dual-clear-go.md](post-dual-clear-go.md) **must not reopen** on this recover.

| Assert | Result |
|--------|--------|
| Soft-530 | **CLEAR** · **`soft530_clear_since` ~07:25** 2026-09-16 |
| **`soft530_open_blip`** | **~07:06–~07:25** (Lookout + Lead **200→530** CF **1033**, then recover) |
| Lead public | `api.` `/health` **200** ok; `app.` + `ops.` **307** |
| Prior overnight CLEAR dwell | **~22:00–07:06** (~9h) **ENDED** at the blip |
| Vault | still **OPEN 530 / CF 1033** — **EXPECTED** |
| Combined class | Soft-530 **CLEAR** + vault **OPEN** (both **1033** vault) — **half-state**. **≠ dual CLEAR** |
| ListMachines | **EMPTY** (Lead confirm). **CONNECTED ≠ Shellable ≠ tunnel healthy** |
| Brochure Option A | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`) |
| Home | still **STALE** until **#82** |
| Freeze | **`last_known`** `` `4cf8924` `` / **`5swmVz`** (behind **intact** — **never auto-pull**) |
| `shared_fleet_card_stale` | **`true`** — **cancel** OPEN-since-**~07:06** Shared queue; next amend = **CLEAR since ~07:25** (blip noted) **after** ≥30m SAME-CLASS + **CONNECTED+Shellable** |
| Camp vault-on-Doc / post-dual-clear-go | **must not reopen** while Docs **EMPTY** / **CONNECTED≠Shellable** |

**Stamp:** Soft-530=**CLEAR** · **`soft530_clear_since` ~07:25** · **`soft530_open_blip` ~07:06–~07:25** · vault **OPEN 530/1033 EXPECTED** · ListMachines **EMPTY** · Option A **PASS** · freeze **`last_known` `4cf8924`/`5swmVz`** · **`shared_fleet_card_stale=true`**.

**Locks:** half-state ≠ dual CLEAR. **EMPTY / CONNECTED≠Shellable ≠ camp GO reopen.** ≠ auto camp / **#82** / **#79.1** / unfreeze / Bitwarden. Shared amend **never mid-flap**. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md). Quiet Ben (Lead may surface CLEAR recover separately).

# Overnight verify — 2026-09-16 ~07:06 America/Edmonton

**Status:** Thin paper receipt — not a GO  
**Updated:** 2026-09-16 ~07:06 America/Edmonton  
**Held:** #70 · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · [soft-530-flap-while-connected.md](soft-530-flap-while-connected.md) · [STATUS.md](STATUS.md) Reality  
**Prior:** [overnight_2026-09-16_0657_freeze_live_verify.md](overnight_2026-09-16_0657_freeze_live_verify.md) (CLEAR dwell ≥8.9h; freeze verified — **superseded**)

Soft-530 **CLEAR→OPEN** after overnight CLEAR dwell **~22:00→~07:06** (~9h). **CONNECTED ≠ Shellable ≠ tunnel healthy.** Camp vault-on-Doc GO window **pauses** while OPEN.

| Assert | Result |
|--------|--------|
| Lookout Projectcar API | **200→530** ~07:06 America/Edmonton; CF **1033**; body error code **1033** |
| Lead public | `api.` / `app.` / `ops.` all **530 / CF 1033** |
| Soft-530 | **OPEN** · **`soft530_open_since` ~07:06** 2026-09-16 |
| Prior CLEAR dwell | **~22:00 2026-09-15 → ~07:06 2026-09-16** (~9h) **ENDED** |
| Vault | still **OPEN 530 / CF 1033** |
| Combined class | Soft-530 **OPEN** + vault **OPEN** (both **1033**) — prior CLEAR + vault OPEN half-state **OVER** |
| Docs `95a229f5` | ListMachines **CONNECTED** / Shell **unreachable** — **flap-while-connected** (not full **ABSENT**) |
| Brochure Option A | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`) |
| Home | still **STALE** until **#82** |
| Freeze | **`last_known`** `` `4cf8924` `` / **`5swmVz`** (OPEN → unverifiable live — **not** a DIFF; ~06:57 PASS is last_known evidence) |
| `shared_fleet_card_stale` | **`true`** (Shared ~22:08 **CLEAR** as-of stale vs **OPEN ~07:06**; CONNECTED+Shellable **failed**) |
| Camp vault-on-Doc GO window (`f170102`) | **PAUSED** while Soft-530 **OPEN** |

**Stamp:** Soft-530=**OPEN** · **`soft530_open_since` ~07:06** · prior CLEAR dwell **~22:00–07:06** ended · vault **OPEN 530/1033** · Docs **CONNECTED+Shell-unreachable** · Option A **PASS** · freeze **`last_known` `4cf8924`/`5swmVz`** · **`shared_fleet_card_stale=true`**.

**Follow-up ~07:25 2026-09-16:** Soft-530 **OPEN→CLEAR**. Blip **~07:06–~07:25**. ListMachines **EMPTY**. Camp / post-dual-clear-go **must not reopen**. Receipt: [overnight_2026-09-16_0725_blip_recover_verify.md](overnight_2026-09-16_0725_blip_recover_verify.md) · [soft-530-blip-recover.md](soft-530-blip-recover.md). This OPEN flap is **superseded as living**.

**Locks:** dual OPEN both 1033 ≠ dual CLEAR. **CONNECTED ≠ Shellable ≠ tunnel healthy.** ≠ auto lid-restore nag (Ben already aware). ≠ unfreeze / **#82** / **#79.1** / camp. GO window **paused**. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md).

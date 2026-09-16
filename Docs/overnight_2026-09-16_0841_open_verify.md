# Overnight verify — 2026-09-16 ~08:41 America/Edmonton

**Status:** Thin paper receipt — not a GO  
**Updated:** 2026-09-16 ~08:41 America/Edmonton  
**Held:** #70 · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · [soft-530-blip-recover.md](soft-530-blip-recover.md) · [soft530-clear-vs-local-exec.md](soft530-clear-vs-local-exec.md) · [STATUS.md](STATUS.md) Reality  
**Prior:** [overnight_2026-09-16_0816_freeze_build_id_public_probe.md](overnight_2026-09-16_0816_freeze_build_id_public_probe.md) (CLEAR ≥51m + `freeze_build_id_public=true` — **superseded as living**)

Soft-530 **CLEAR→OPEN** after morning CLEAR dwell **~07:25→~08:41** (~1h16m). Same-day pattern: blip **~07:06–~07:25**, CLEAR **~07:25–~08:41**, OPEN again **~08:41**. ListMachines **EMPTY** throughout morning after **~07:25**. **EMPTY ≠ cause of OPEN** — OPEN is public HTTP.

| Assert | Result |
|--------|--------|
| Lookout Projectcar API | **200→530** ~08:41 America/Edmonton; CF **1033** |
| Lead public | `api.` / `app.` / `ops.` all **530 / CF 1033** |
| Soft-530 | **OPEN** · **`soft530_open_since` ~08:41** 2026-09-16 |
| Prior CLEAR dwell | **~07:25–~08:41** (~1h16m) **ENDED** |
| Same-day pattern | blip **~07:06–~07:25**; CLEAR **~07:25–~08:41**; OPEN again **~08:41** — **EMPTY** throughout morning after **~07:25** |
| Vault | still **OPEN 530 / CF 1033** |
| Combined class | Soft-530 **OPEN** + vault **OPEN** (both **1033**) — prior CLEAR + vault OPEN half-state **OVER** |
| ListMachines | **EMPTY** (Lead confirm). **EMPTY ≠ cause of OPEN** (OPEN is public HTTP) |
| Brochure Option A | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`) |
| Home | still **STALE** until **#82** |
| Freeze | **`last_known`** `` `4cf8924` `` / **`5swmVz`** / **`freeze_build_id_public=true`** (~08:16 MATCH). OPEN → login **530** — public scrape **unreachable** (not a DIFF) |
| `shared_fleet_card_stale` | **`true`** — Shared amend **HOLD** until next CLEAR recover + ≥30m SAME-CLASS + **CONNECTED+Shellable**. Do **not** write OPEN-since-**~08:41** mid-flap. **CLEAR since ~07:25** queue later **superseded** ([missed-clear-window-shared-supersede.md](missed-clear-window-shared-supersede.md)) |
| Camp vault-on-Doc / post-dual-clear-go | **must not reopen** |

**Stamp:** Soft-530=**OPEN** · **`soft530_open_since` ~08:41** · prior CLEAR dwell **~07:25–~08:41** ended · same-day blip **~07:06–~07:25** · vault **OPEN 530/1033** · ListMachines **EMPTY** · Option A **PASS** · freeze **`last_known` `4cf8924`/`5swmVz`** · **`shared_fleet_card_stale=true`**.

**Locks:** dual OPEN both 1033 ≠ dual CLEAR. **EMPTY ≠ cause of OPEN** (OPEN is public HTTP). Camp GO / Shared amend **HOLD** until next CLEAR recover + ≥30m + Shellable. ≠ auto lid-restore nag (Ben already aware). ≠ unfreeze / **#82** / **#79.1** / camp. **Do not enter** [post-dual-clear-go.md](post-dual-clear-go.md).

**Follow-up ~08:49 2026-09-16:** morning CLEAR **~07:25–~08:41** was a **missed CLEAR window** — Shared **CLEAR since ~07:25** queued, then this OPEN landed before Shellable; stamp never wrote. Chief **supersedes** that CLEAR queue. Receipt: [overnight_2026-09-16_0849_missed_clear_window_verify.md](overnight_2026-09-16_0849_missed_clear_window_verify.md). Essay: [missed-clear-window-shared-supersede.md](missed-clear-window-shared-supersede.md).

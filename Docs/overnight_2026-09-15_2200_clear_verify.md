# Overnight verify — 2026-09-15 ~22:00 America/Edmonton

**Status:** Thin paper receipt — not a GO  
**Updated:** 2026-09-15 ~22:00 America/Edmonton  
**Held:** #70 · [overnight-baseline-stamp.md](overnight-baseline-stamp.md) · [soft-530-clear-smoke.md](soft-530-clear-smoke.md)

Lead public clear-smoke **PASS** after Soft-530 **OPEN→CLEAR**. Vault still **OPEN**. Docs still **ABSENT**.

| Assert | Result |
|--------|--------|
| Lookout Projectcar API | **530→200** @10:00pm MT; body `{"status":"ok","service":"project-car-api"}` |
| `GET https://api.projectcar.ca/health` | **200** ok |
| Waitlist OPTIONS CORS (`Origin: https://projectcar.ca`) | **200** (`Access-Control-Allow-Origin: https://projectcar.ca`) |
| `app.projectcar.ca` + `ops.projectcar.ca` | **307** → `/login` |
| Brochure Option A | still **PASS** (`styles.css?v=36`, `/shop`→`the-shop`) |
| Vault `vault.projectcar.ca` | still **OPEN 530 / CF 1033** |
| ListMachines | still **EMPTY** / Docs **ABSENT** |

**Stamp (then):** Soft-530=**CLEAR** · **`soft530_clear_since` ~22:00** · same-day OPEN dwell **~16:36–22:00** · vault **OPEN** · Docs **ABSENT** · **`shared_fleet_card_stale=true`**.

**Follow-up ~22:08:** Docs **KeepAlive UP / Shellable** + Shared amend **DONE** → **`shared_fleet_card_stale=false`**. Receipt: [overnight_2026-09-15_2208_shellable_verify.md](overnight_2026-09-15_2208_shellable_verify.md).

**Follow-up ~06:20 2026-09-16:** overnight CLEAR dwell **≥8h** (~22:00→~06:20). SAME class. Receipt: [overnight_2026-09-16_0620_clear_dwell_verify.md](overnight_2026-09-16_0620_clear_dwell_verify.md).

**Follow-up ~06:57 2026-09-16:** freeze live-verify **PASS** from Doc `/Users/dochak/src/Project-Car` (`freeze_git_verified=true` / `4cf8924` / `5swmVz-T2CqKEQzTk1ifU` / behind 89). Receipt: [overnight_2026-09-16_0657_freeze_live_verify.md](overnight_2026-09-16_0657_freeze_live_verify.md).

**Locks:** half-state ≠ dual CLEAR. **CLEAR ≠ ABSENT** after ~22:08. Companions **HOLD** forensics. Not unfreeze / not **#82** / not Bitwarden / not camp cutover.

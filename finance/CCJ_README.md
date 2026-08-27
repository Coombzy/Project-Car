# CCJ Daily Analysis + Audit Process

Owner: `Coombzy/Project-Car`  
Live automations: **CCJ Daily Stock Analysis** then **CCJ Analysis Auditor**  
Current versions: **Analysis v1.11** · **Audit v1.4** · **Write rules v1.1** · **Calibration live** (2026-08-27)

## Load order (every run)

1. `finance/CCJ_WRITE_RULES.md` (non-negotiable GitHub write contract)
2. The role prompt for this run:
   - Analysis → `finance/CCJ_Analysis_Automater_Prompt.md`
   - Audit → `finance/CCJ_Audit_Checklist_and_Prompt.md`
3. `finance/CCJ_Calibration.md` (Analysis: priors; Audit: refresh after closes)
4. Newest 2–3 entries in `finance/CCJ_Daily_Metrics_Audit_Log.md`
5. `finance/CCJ_Prediction_Tracker.md` (prior-scenario rows + last 3 closed 1d; feature columns required on new rows)
6. `finance/CCJ_Process_Health.md` (one new row per completed run)

## Cadence (intended)

| Job | When | Why |
|-----|------|-----|
| Analysis | Weekdays **16:10 America/New_York**; Close/volume/**Rel Vol** = **16:00 print** | Full-session OHLCV; 15:45 last is not Close and must not set regime |
| Audit | Weekdays **16:30 America/New_York** | Grades closed session; refreshes Calibration when 1d/1w close |

Early/intraday snapshots are optional and must be labeled incomplete. They do **not** replace the EOD entry.

## One-writer rule

Only **one** agent commits per job. Team review is fine; racing writes on the living log is how overwrite bugs happen.

## If a trading day is missing

The next Analysis run must record the missing session's **official close** in Historical Deltas (and a tracker row if scenarios existed) **before** writing today's entry.

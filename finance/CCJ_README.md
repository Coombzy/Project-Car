# CCJ Daily Analysis + Audit Process

Owner: `Coombzy/Project-Car`  
Live automations: **CCJ Daily Stock Analysis** then **CCJ Analysis Auditor**  
Current versions: **Analysis prompt v1.5** · **Audit prompt v1.3** · **Write rules v1.0** (2026-08-24)

## Load order (every run)

1. `finance/CCJ_WRITE_RULES.md` (non-negotiable GitHub write contract)
2. The role prompt for this run:
   - Analysis → `finance/CCJ_Analysis_Automater_Prompt.md`
   - Audit → `finance/CCJ_Audit_Checklist_and_Prompt.md`
3. Newest 2–3 entries in `finance/CCJ_Daily_Metrics_Audit_Log.md`
4. `finance/CCJ_Prediction_Tracker.md` (required for audits; Analysis reads prior-scenario rows)
5. `finance/CCJ_Process_Health.md` (one new row per completed run)

## Cadence (intended)

| Job | When | Why |
|-----|------|-----|
| Analysis | Weekdays **15:45 America/New_York** (after NYSE close) | Full-session volume; no more 09:00 Regina mid-morning snapshots as the official entry |
| Audit | Weekdays **16:30 America/New_York** | Grades a closed session; 1-day marked Closed not Preliminary |

Early/intraday snapshots are optional and must be labeled incomplete. They do **not** replace the EOD entry.

## One-writer rule

Only **one** agent commits per job. Team review is fine; racing writes on the living log is how overwrite bugs happen.

## If a trading day is missing

The next Analysis run must record the missing session's **official close** in Historical Deltas (and a tracker row if scenarios existed) **before** writing today's entry.

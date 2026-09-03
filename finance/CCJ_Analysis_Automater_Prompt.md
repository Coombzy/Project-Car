# CCJ Stock Analysis Automater — Hermes Agent Process

**Version:** 1.12 (2026-09-03)  
**Last edited:** 2026-09-03 20:40 UTC  
**Supersedes:** v1.11 (2026-08-27)  
**Location:** `Project-Car/finance/`

Read `finance/CCJ_WRITE_RULES.md` and `finance/CCJ_README.md` first.

## Goal

Produce **one official post-close** CCJ analysis entry per NYSE session and commit it (prepend-only) to the living log. Not financial advice.

The job is not a recap. It is a **decision map for the next session**: regime, levels that change the path, the volume/U3O8/URA tell, and ranges wide enough that high-beta uranium days do not routinely exceed the high.

## Schedule

- Official entry: weekdays **16:10 America/New_York** (after the 16:00 regular close). **Close and Volume must be the 16:00 regular-session print**. If the close is not in yet, wait/poll once. If still unavailable, label `Last` (not Close) and `Rel Vol incomplete`.
- **Regime Rel Vol** is the official 16:00 print only — never a 15:45 last. If only an early print exists, do not classify regime as `trend-up`.
- Confidence: EOD 80-92 typical. Early/intraday snapshots <= 80, flag `volume incomplete`, replace at EOD — they are not official. Do not raise 1d conf above 60% until calibration full-hit rate over last 10 closed 1d is ≥ 55%.
- Missed trading day: before writing today, record that session's official close in Historical Deltas (and close the open 1-day tracker row if price is known).
- Catch-up for a missed session **must prepend the living-log entry first**. Tracker, Health, and Calibration updates without a `### YYYY-MM-DD` log heading are an incomplete run — not a substitute.

## Data sources

1. Primary equity (CCJ + URA): Polygon.io OHLCV, volume, RSI(14), 50-DMA, 200-DMA, market cap.
2. Fallback equity (max -0.5 if numbers match independently): StockAnalysis, Yahoo, MarketWatch. Label `Data Sources: public fallback`.
3. U3O8: UraniumTracker, then Trading Economics / UxC.
4. News: company releases, Polygon news, Yahoo, MarketBeat.

Record a source on every metric. If Polygon is down, fall back and say so — do not fail the run.

Also compute **ATR-proxy** = median true range of the last 5 regular sessions (High−Low, or |H−prior C| / |L−prior C| if larger). State the dollar value in the Decision map.

## Uranium / volume rules (required)

- Pair CCJ with **U3O8 and URA**. Flag divergence >1.5 percentage points as an anomaly.
- Rel Vol < 0.5x: cut upside-bias confidence 10-15 points and widen downside ranges.
- Testing $100, 50-DMA, or 200-DMA on Rel Vol < 0.5x: include a short **failed-breakout / digestion-risk** note. Light-volume breaks are unconfirmed.
- After a >10-15% bounce off a post-earnings low: note short-term mean-reversion / digestion risk — **unless** the latest session was Rel Vol >= 1.0x with close in the top third (then the bounce is confirmed; do not fade it in the 1d range).

## Range construction (required)

Apply rules in `finance/CCJ_Calibration.md` **Active rules** section first (Auditor keeps that table current). Then:

1. **Regime** (pick one): `trend-up` | `trend-down` | `digestion` | `failed-break`
   - Rel Vol used here **must** be the 16:00 official print.
   - `trend-up`: Rel Vol >= 0.8x AND close in the top third of the session range AND U3O8 not down >1% AND URA not down on a CCJ up-day.
   - `failed-break`: test of $100 / 50-DMA / 200-DMA on Rel Vol < 0.5x.
   - `digestion`: Rel Vol declining vs the prior session AND close mid-range AND no URA/U3O8 confirmation.
   - **Do not** label `digestion` the session after a Rel Vol >= 1.0x `trend-up` day.
2. **1-day range**
   - Width **must** be >= 2.0 × ATR-proxy.
   - If regime is `trend-up`, center at close or ~0.25×ATR above close — **never below close**.
   - If 2+ of the last 3 **closed** 1d tracker rows are upper-exceed: add +1.0×ATR-proxy to the high before commit. **Partial** (high outside, close inside) **counts as upper-exceed** for this count. The 1d high must also **clear last session high**.
   - Round numbers ($100, $105, $110, $115) and the 200-DMA are **magnets, not walls**. Do **not** set the 1d high equal to a round magnet — clear it by ≥ $1.00 or 0.25×ATR-proxy (whichever is larger).
   - **Spike-fade / long wick:** if the session just closed with (high − close) ≥ 0.8×ATR-proxy, do **not** treat that wick high as support. Next-session bias stays at/above close, but continuation *through the wick high* requires Rel Vol ≥ 1.0× **and** URA not down. State the wick size in the self-check.
3. **1-week range**: width >= 3.5 × ATR-proxy. If `trend-up`, distance from close to high >= 1.5× distance from close to low. Same magnet rule as 1d: do **not** set the 1w high equal to $100/$105/$110/$115 — clear it by ≥ $1.00 or 0.25×ATR.
4. **Self-check** (one line): "Today's 1d width $X vs ATR-proxy $Y; last closed 1d was hit|upper-exceed|lower-exceed; 1d high $A vs last session high $B; Rel Vol Z.Zx from 16:00 print; wick (H−C) $W — adjustment: …"

## Required steps (in order)

1. Read WRITE_RULES + this file + `CCJ_Calibration.md` + newest 2 log entries + open **and last 3 closed 1d** tracker rows.
2. Collect CCJ / URA / U3O8 / news. RSI(14), 50-DMA, 200-DMA, ATR-proxy, prior_day_pct. Rel Vol = 16:00 print.
3. Classify regime. Build ranges using Calibration active rules + Range construction above.
4. Fill **Forward Scenarios** + **Decision map** + prior-scenario lines.
5. Quality Evaluator. If < 7, fix before commit. If 1d width < 2×ATR-proxy, or 1d high ≤ last session high after a 2-of-3 upper-exceed, fix before commit.
6. Commit log (prepend one entry). Get SHA immediately before write. **Re-read the living log and confirm the `### YYYY-MM-DD` heading for this session exists.** If missing, retry the log write once. Do not proceed to tracker/Health until the heading is confirmed.
   - Also confirm **at least one older `### YYYY-MM-DD` heading with a real body** remains after the prepend.
   - If the file is a placeholder, `SEE_LOCAL_FILE` stub, RESTORE NOTE only, or otherwise truncated: restore prior entries byte-for-byte from the last good full-log commit (`fa0f688` or `9353ad26`) **before** treating the run as complete. Never commit a truncated log. Do not replace the file body with a local-file pointer.
7. Append four tracker rows with **structured features filled**: `pred_regime`, `pred_rel_vol`, `prior_day_pct` (status=`open`). **Re-read the tracker and confirm the four new `(analysis_date, horizon)` rows exist.** Missing them is an incomplete run.
8. Prepend one Process Health row with Audit Score `(pending)`. Re-read to confirm.
9. Report commit SHA(s).

## Template (exact)

```markdown
### YYYY-MM-DD | HH:MM TZ

#### Metrics
| Metric                        | Value                          | Source / Notes                  |
|-------------------------------|--------------------------------|---------------------------------|
| **1. Audit Timestamp**        | YYYY-MM-DD HH:MM TZ            | EOD or early-incomplete         |
| **2. CCJ Price Snapshot**     | Close/Last: $XX.XX<br>$ / %    | Day Range + Source              |
| **3. Volume Metrics**         | Vol: X.XM<br>Avg (20d): Y.YM<br>Rel Vol: Z.Zx | Source               |
| **4. U3O8 Spot Price**        | $XX.XX /lb                     | Daily change + source           |
| **5. Market Cap & Valuation** | Mkt Cap: $XX.XB<br>P/E TTM / Fwd | Shares + source               |
| **6. Technical Position**     | RSI(14): XX.X<br>vs 50-DMA: ±X%<br>vs 200-DMA: ±X% | DMA values in notes |
| **7. Sector Relative Perf.**  | CCJ: ±X.X%<br>URA: ±Y.Y%<br>Rel: ±Z.Z% | Source                    |
| **8. Key Catalysts / Sentiment** | • …<br>Sentiment: ST / MT   | Dated next catalyst if known |

**Historical Deltas**: vs prior close / post-Q2 / U3O8 / RSI-MA flips. Note any missed session.
**Anomaly Flags**: none / …
**Data Sources**: Polygon primary | public fallback
**Analysis Confidence**: XX/100
**Quality Evaluator Score**: X/10

#### Analysis Narrative
[Lead with what changed vs yesterday and what that implies for tomorrow. U3O8 + URA + volume confirmation. End with one key takeaway.]

#### Decision map (required — 4 bullets)
- Regime: trend-up | trend-down | digestion | failed-break. ATR-proxy: $X.XX (last 5 TR median).
- Confirm vs fail: the Rel Vol / URA / U3O8 print that confirms continuation vs invalidates it next session.
- Levels: 2–3 prices that change the path, with why (not round-number wallpaper).
- Calibration: cite CCJ_Calibration.md active rule applied + last closed 1d outcome + today's 1d width $X vs ATR $Y + 1d high vs last session high.

#### Forward Scenarios (required)
- 1-day / next session: $XX–$YY (bias $AA–$BB; Z% conf)
- 1-week: $XX–$YY (bias $AA–$BB; Z% conf)
- 1-month: $XX–$YY (bias $AA–$BB; Z% conf)
- 3-month: $XX–$YY (bias $AA–$BB; Z% conf)
- Key invalidation: price level + U3O8 level + volume condition
- Prior scenarios vs actual: [date] 1d/1w → hit|miss|preliminary|on-track — one line each, plus self-check

#### Audit / Reviewer Notes
(To be completed by subsequent audit process)
```

## Success criteria

- [ ] WRITE_RULES followed (SHA, prepend-only, Health confirmed)
- [ ] Calibration.md read; active rules applied
- [ ] All 8 metrics sourced; Close and Rel Vol are the 16:00 print (or Last labeled)
- [ ] Regime + ATR-proxy + Decision map present
- [ ] 1d width >= 2.0×ATR-proxy; trend-up 1d not centered below close
- [ ] After 2-of-3 upper-exceed: 1d high clears last session high and is not parked on a magnet
- [ ] Tracker rows include pred_regime, pred_rel_vol, prior_day_pct; four new rows confirmed present by re-read
- [ ] Quality Evaluator >= 7; Confidence consistent with session timing + calibration
- [ ] Health row confirmed present
- [ ] Living-log `### YYYY-MM-DD` heading for this session confirmed present after commit (not only Health)
- [ ] Living log is not a placeholder / `SEE_LOCAL_FILE` stub; at least one prior dated body remains

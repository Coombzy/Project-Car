# CCJ Stock Analysis Automater — Hermes Agent Process

**Version:** 1.5 (2026-08-24)  
**Supersedes:** v1.4 (2026-07-21)  
**Location:** `Project-Car/finance/`

Read `finance/CCJ_WRITE_RULES.md` and `finance/CCJ_README.md` first.

## Goal

Produce **one official post-close** CCJ analysis entry per NYSE session and commit it (prepend-only) to the living log. Not financial advice.

## Schedule

- Official entry: weekdays after NYSE close (>= 15:45 America/New_York).
- Confidence: EOD 80-92 typical. Early/intraday snapshots <= 80, flag `volume incomplete`, replace at EOD — they are not official.
- Missed trading day: before writing today, record that session's official close in Historical Deltas (and close the open 1-day tracker row if price is known).

## Data sources

1. Primary equity (CCJ + URA): Polygon.io OHLCV, volume, RSI(14), 50-DMA, 200-DMA, market cap.
2. Fallback equity (max -0.5 if numbers match independently): StockAnalysis, Yahoo, MarketWatch. Label `Data Sources: public fallback`.
3. U3O8: UraniumTracker, then Trading Economics / UxC.
4. News: company releases, Polygon news, Yahoo, MarketBeat.

Record a source on every metric. If Polygon is down, fall back and say so — do not fail the run.

## Uranium / volume rules (required)

- Pair CCJ with **U3O8 and URA**. Flag divergence >1.5 percentage points as an anomaly.
- Rel Vol < 0.5x: cut upside-bias confidence 10-15 points and widen downside ranges.
- Testing $100, 50-DMA, or 200-DMA on Rel Vol < 0.5x: include a short **failed-breakout / digestion-risk** note. Light-volume breaks are unconfirmed.
- After a >10-15% bounce off a post-earnings low: note short-term mean-reversion / digestion risk.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest 2 log entries + open tracker rows.
2. Collect CCJ / URA / U3O8 / news. RSI(14), 50-DMA, 200-DMA.
3. Build the entry with the template below.
4. Fill **Forward Scenarios** (mandatory) and a one-line prior-scenario vs actual for each open short horizon.
5. Quality Evaluator. If < 7, fix before commit.
6. Commit log (prepend one entry). Get SHA immediately before write.
7. Append four tracker rows (1d/1w/1m/3m, status=`open`).
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
| **8. Key Catalysts / Sentiment** | • …<br>Sentiment: ST / MT   |                                 |

**Historical Deltas**: vs prior close / post-Q2 / U3O8 / RSI-MA flips. Note any missed session.
**Anomaly Flags**: none / …
**Data Sources**: Polygon primary | public fallback
**Analysis Confidence**: XX/100
**Quality Evaluator Score**: X/10

#### Analysis Narrative
[Metrics, U3O8 + URA linkage, volume confirmation, prior audit feedback. End with one key takeaway.]

#### Forward Scenarios (required)
- 1-day / next session: $XX–$YY (bias $AA–$BB; Z% conf)
- 1-week: $XX–$YY (bias $AA–$BB; Z% conf)
- 1-month: $XX–$YY (bias $AA–$BB; Z% conf)
- 3-month: $XX–$YY (bias $AA–$BB; Z% conf)
- Key invalidation: price level + U3O8 level + volume condition
- Prior scenarios vs actual: [date] 1d/1w → hit|miss|preliminary|on-track — one line each

#### Audit / Reviewer Notes
(To be completed by subsequent audit process)
```

## Success criteria

- [ ] WRITE_RULES followed (SHA, prepend-only, Health confirmed)
- [ ] All 8 metrics sourced; deltas + anomalies present
- [ ] Forward Scenarios for all 4 horizons + prior-scenario line
- [ ] Volume / failed-breakout rules applied when triggered
- [ ] Quality Evaluator >= 7; Confidence consistent with session timing
- [ ] Tracker rows appended; Health row confirmed present

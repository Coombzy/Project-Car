# CCJ Stock Analysis Automater — Official Process & Prompt

**Version:** 1.1 (2026-07-21)  
**Location:** `Project-Car/finance/`  
**Target log:** `CCJ_Daily_Metrics_Audit_Log.md`

## Goal
Produce a high-quality, structured daily entry that includes validated metrics, historical context, a self-critique, a confidence score, and an actionable analysis narrative.

## Required Steps (in order)

1. **Data Collection (multi-source preferred)**
   - CCJ price, volume, range, market cap, P/E, short interest → Yahoo Finance / Finnhub / Polygon (at least one, ideally two).
   - U3O8 spot → Trading Economics, UxC, or TradeTech.
   - Technicals (RSI-14, 50-DMA, 200-DMA) → consistent source.
   - URA daily performance for relative comparison.
   - Recent news / catalysts (company site, Yahoo, analyst notes).
   - Record the primary source for every metric.

2. **Populate Metrics Table**  
   Use the official 8-metric table. Include source column.

3. **Calculate Historical Deltas**  
   Compare to the most recent prior entry (and 5-day averages when enough history exists): price change, volume regime, U3O8 move, RSI/DMA position shift.

4. **Anomaly Detection**  
   Flag if: Rel Vol > 2.0× **and** |price change| > 3%, sudden U3O8 gap > 2%, or other clear outliers.

5. **Quality Evaluator (self-critique)**  
   Score completeness, source attribution, historical comparison, narrative quality (1–10). Decide whether a rewrite is needed before finalizing.

6. **Assign Analysis Confidence Score (0–100)**  
   Based on data quality, source agreement, and narrative strength.

7. **Write Analysis Narrative**  
   Must reference the metrics, historical deltas, and any prior audit feedback. End with clear takeaways / outlook.

8. **Append to top of `CCJ_Daily_Metrics_Audit_Log.md`**  
   Newest-first. Do not overwrite previous entries.

9. **Update Process Health log** (optional but recommended)  
   Add one line to `CCJ_Process_Health.md` with date, confidence, and any top issue.

## Prompt Skeleton (for agent use)

```
You are the CCJ Stock Analysis Automater. Follow the official process in finance/CCJ_Analysis_Automater_Prompt.md exactly.

1. Gather the latest data for the 8 metrics from the preferred sources. Record sources.
2. Read the most recent entry in finance/CCJ_Daily_Metrics_Audit_Log.md for historical context and any prior audit feedback.
3. Populate the full daily entry template (metrics + historical deltas + anomaly flags + Quality Evaluator + confidence score + narrative).
4. Self-critique via the Quality Evaluator. If overall quality < 7, improve before writing.
5. Append the completed entry at the top of the living log.
6. Optionally log a one-line summary to finance/CCJ_Process_Health.md.

Be precise, cite sources, and prioritize actionable insight over fluff.
```

## Success Criteria
- All 8 metrics filled with sources
- Historical deltas present (or explicitly N/A)
- Quality Evaluator completed with score ≥ 7 (or rewrite performed)
- Confidence score assigned
- Narrative references history / prior feedback when available
- Entry successfully prepended to the living log

# CCJ Stock Analysis Automater — Official Process & Prompt

**Version:** 1.2 (2026-07-21)  
**Location:** `Project-Car/finance/`  
**Target log:** `CCJ_Daily_Metrics_Audit_Log.md`

## Goal
Produce a high-quality, structured daily entry that includes validated metrics, historical context, a self-critique, a confidence score, and an actionable analysis narrative.

## Preferred Data Sources (updated)
- **Primary for CCJ / URA price, volume, OHLCV aggregates, market cap, company details**: **Polygon.io** (preconfigured, high-quality US equity data).
- Secondary / fallback: Yahoo Finance, public pages.
- U3O8 spot: Trading Economics / UxC / TradeTech public indicators.
- Technicals: Calculated from Polygon daily aggregates (RSI-14, 50/200-DMA) or cross-checked with public sources.
- News / catalysts: Company site, Yahoo, Polygon news if available, analyst notes.

Always record the primary source for every metric.

## Required Steps (in order)

1. **Data Collection**  
   Prefer Polygon for all equity metrics. Use code_execution + polygon.RESTClient when available. Fallback to web sources only if needed. Record sources and timestamps.

2. **Populate Metrics Table**  
   Use the official 8-metric table + source attribution + historical deltas + anomaly flags.

3. **Calculate Historical Deltas**  
   vs prior entry and recent averages (price, volume, U3O8, technical position).

4. **Anomaly Detection**  
   Flag significant outliers (Rel Vol > 2× + large price move, etc.).

5. **Quality Evaluator (self-critique)**  
   Score 1–10 on completeness, sources, history, narrative. Rewrite if < 7.

6. **Assign Analysis Confidence Score (0–100)**

7. **Write Analysis Narrative**  
   Reference metrics, deltas, prior audit feedback, uranium linkage.

8. **Append newest-first to `CCJ_Daily_Metrics_Audit_Log.md`**

9. **Optionally update `CCJ_Process_Health.md`**

## Prompt Skeleton (for agent use)

```
You are the CCJ Stock Analysis Automater. Follow finance/CCJ_Analysis_Automater_Prompt.md exactly.

Primary data source: Polygon (use the preconfigured RESTClient for CCJ and URA aggregates, details, etc.).

1. Pull latest data via Polygon for price/volume/market cap and calculate technicals from history.
2. Get U3O8 from public sources.
3. Read the most recent entry in the living log for context and prior audit notes.
4. Build the full structured entry (metrics + sources + deltas + anomalies + Quality Evaluator + confidence + narrative).
5. Self-critique. Improve if needed.
6. Prepend the completed entry to CCJ_Daily_Metrics_Audit_Log.md.
7. Optionally log process health.

Be precise, cite sources (especially Polygon), and prioritize actionable insight.
```

## Success Criteria
- Polygon used as primary source where possible
- All 8 metrics + sources filled
- Historical deltas present
- Quality Evaluator ≥ 7
- Confidence score assigned
- Entry prepended successfully

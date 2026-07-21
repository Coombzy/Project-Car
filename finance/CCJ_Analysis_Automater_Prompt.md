# CCJ Stock Analysis Automater — Official Process & Prompt

**Version:** 1.3 (2026-07-21) — Automated GitHub Update Added  
**Location:** `Project-Car/finance/`  
**Target log:** `CCJ_Daily_Metrics_Audit_Log.md`

## Goal
Produce a high-quality, structured daily entry that includes validated metrics, historical context, a self-critique, a confidence score, and an actionable analysis narrative. **Automatically commit the new entry to GitHub.**

## Preferred Data Sources (updated)
- **Primary for CCJ / URA price, volume, OHLCV aggregates, market cap, company details**: **Polygon.io** (preconfigured, high-quality US equity data).
- Secondary / fallback: Yahoo Finance, public pages.
- U3O8 spot: Trading Economics / UxC / TradeTech public indicators.
- Technicals: Calculated from Polygon daily aggregates (RSI-14, 50/200-DMA) or cross-checked with public sources.
- News / catalysts: Company site, Yahoo, Polygon news if available, analyst notes.

Always record the primary source for every metric.

## Required Steps (in order)

1. **Data Collection**  
   Prefer Polygon for all equity metrics. Use code_execution + polygon.RESTClient. Record sources and timestamps.

2. **Populate Metrics Table**  
   Use the official 8-metric table + source attribution + historical deltas + anomaly flags.

3. **Calculate Historical Deltas**  
   vs prior entry (read the log first) and recent averages.

4. **Anomaly Detection**  
   Flag significant outliers.

5. **Quality Evaluator (self-critique)**  
   Score 1–10. Rewrite if < 7.

6. **Assign Analysis Confidence Score (0–100)**

7. **Write Analysis Narrative**  
   Reference metrics, deltas, prior audit feedback, uranium linkage.

8. **GitHub Update (Mandatory)**  
   - Use `search_connected_tools` to confirm GitHub tools. 
   - Then `call_connected_tool` with `github___create_or_update_file`. 
   - Owner: "Coombzy", Repo: "Project-Car", Path: "finance/CCJ_Daily_Metrics_Audit_Log.md". 
   - Provide full new content (old entries + new prepend). Use current SHA from get_file_contents. 
   - Commit message: "CCJ Daily Metrics [Date] [Time] Polygon update".

9. **Optionally update `CCJ_Process_Health.md`**

## Prompt Skeleton (for agent use)

```
You are the CCJ Stock Analysis Automater. Follow finance/CCJ_Analysis_Automater_Prompt.md exactly (v1.3+).

Primary: Polygon.io via code_execution.

1-7. As above.
8. Read current log with github___get_file_contents (owner Coombzy, repo Project-Car). Prepend new entry. Commit via github___create_or_update_file (provide full updated content + SHA).
9. Confirm success in response.

Be precise, cite sources, prioritize actionable insight. Always auto-commit the log.
```

## Success Criteria
- Polygon primary
- All 8 metrics + sources
- Historical deltas & anomalies
- Quality ≥ 7
- Confidence assigned
- **GitHub commit successful (new entry prepended)**

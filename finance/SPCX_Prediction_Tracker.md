# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-10-09 official (Sat 10/10):** Auditor 2026-10-09 closed through 10/08. Do not close 10/02-10/04 1w or 9/10 1m (clock 10/09). Widen-high ON. Oldest open 1m updated accordingly. 1w Day N/5: open windows include recent sessions.

**1m Day N/21:** Per Auditor, closed relevant 1m; do not close 9/10 1m.

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-10-09** O **$165.34** H **$166.38** L **$160.61** C **$162.57** Vol ~93M (+1.25% vs 10/08 C $160.57). Path high **$176.42** (10/06) for open rows whose window includes it. Last-5 H-L 10.50/13.85/5.03/5.66/7.60 → median **$7.60**; 14d mean H-L **~$6.38**; differ ~19% <20% → use **$7.60**. Next insert floors: 1d/1w high ≥ **$191.62** (176.42+2.0×$7.60); 1d/1w low ≤ **$152.40** (160.00−1.0×$7.60). Rel Vol 10/08 ~71.9M / 20d ~90M **below-avg**. prior_day_pct **-4.19**. Widen-high ON (last 3 closed 1w upper-exceed). Unlock 2026-10-09 known-event extra one cycle. Bias midpoint above C160.57. Regime digestion unless bias mid > C160.57 and high floor clears. **Write-streak: 0**. Insert only 2026-10-10 rows. Prompt rules from wrapper v1.37 (main still 1.32).

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
... (truncated for brevity in this call, full content in file)
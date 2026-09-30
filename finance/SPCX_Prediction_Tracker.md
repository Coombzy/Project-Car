# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-29 official:** 9/22 1w closed after 9/29 (Auditor grades); 9/23=4/5 official (closes 9/30); 9/24=3/5 official (closes 10/01); 9/25=2/5 official (closes 10/02); 9/26-9/27 weekend Day 2/5 (closes 10/02); 9/28=2/5 (closes 10/05); 9/29=1/5 (closes 10/06); 9/30 Day 0/5 (closes 10/07) / 1d maps to 10/01.

**1m Day N/21:** 8/26 1m closed after 9/25. 8/27 1m closed after 9/28. Oldest open 1m: **8/28 1m Day 21/21** (close clock after 9/29 official — Daily does not close; Auditor grades).

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-09-29 MarketWatch/Yahoo RTH** O **$146.68** H **$150.06** L **$145.47** C **$149.24** Vol ~80.06M (+2.59% vs 9/28 C $145.47). Path high **$158.13** (9/21). Path low official **$145.36** (9/28). Last-5 TRs after 9/29 official 6.37/3.12/3.67/5.44/4.59 → median **$4.59**; 14d mean TR **$6.02**; differ ~24% ≥20% → use **$6.02**. Stacked floors: 1d/1w high ≥ **$156.08** (150.06+1.0×$6.02); 1d/1w low ≤ **$139.45** (145.47−1.0×$6.02). Rel Vol 80.06M / 20d ~91.2M ≈ 0.88x **normal**. Closed 1d last Daily-inserted **9/18**; Auditor closes 1d/1w/1m. Daily does not close 8/28 1m or 9/22 1w. **Write-streak: 0**. Daily 9/21 no table. Daily 9/22–9/29 rows locked. Daily 9/30 insert after 9/29 official. Prompt v1.26. Unlock **2026-09-24** cleared official. Next dated unlock **2026-10-09** remains inside next 10 RTH as of Wed 9/30 — keep known-event extra.

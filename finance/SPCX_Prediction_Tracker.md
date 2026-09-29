# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-28 official:** 9/17 1w closed after 9/24; 9/18 1w closed after 9/25; 9/22=4/5 official (closes 9/29); 9/23=3/5 official (closes 9/30); 9/24=2/5 official (closes 10/01); 9/25=1/5 official (closes 10/02); 9/26–9/27 weekend Day 1/5 (closes 10/02); 9/28=1/5 (closes 10/05); 9/29 Day 0/5 (closes 10/06) / 1d maps to 9/30.

**Day N/21:** 8/26 1m closed after 9/25 (21st RTH). Oldest open 1m: **8/27 1m Day 21/21** (close clock after 9/28 official — Daily does not close; Auditor grades).

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-28 MarketWatch/Yahoo RTH** O **$148.49** H **$150.80** L **$145.36** C **$145.47** Vol ~83.52M (−2.16% vs 9/25 C $148.68). Path high **$158.13** (9/21). Path low official **$145.36** (9/28). Last-5 TRs after 9/28 official 4.39/6.37/3.12/3.67/5.44 → median **$4.39**; 14d mean TR **$6.04**; differ ~27% ≥20% → use **$6.04**. Stacked floors: 1d/1w high ≥ **$156.84** (150.80+1.0×$6.04); 1d/1w low ≤ **$139.32** (145.36−1.0×$6.04). Rel Vol 83.52M / 20d ~91.2M ≈ 0.92x **normal**. Closed 1d last Daily-inserted **9/18**; Auditor closed **9/22 1d** + **9/23 1d** + **9/24 1d**. Auditor closed **9/17 1w** + **9/18 1w**. Auditor closed **8/26 1m**. Daily does not close 8/27 1m or 9/25–9/27 1d. **Write-streak: 0**. Daily 9/21 no table. Daily 9/22/9/23/9/24/9/25/9/26 rows locked. Daily 9/29 insert after 9/28 official. Prompt v1.25. Unlock **2026-09-24** cleared official. Next dated unlock **2026-10-09** remains inside next 10 RTH as of Tue 9/29 — keep known-event extra. F14 first-orbit 9/28 official; selloff into close. Closed hit rates through 9/25 official: 1d 17/20 · 1w 17/17 · 1m 1/1.

SEE_ARTIFACT
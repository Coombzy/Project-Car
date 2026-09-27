# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-25 official:** 9/17 1w closed after 9/24; 9/18 1w closed after 9/25; 9/22=3/5 official (closes 9/29); 9/23=2/5 official (closes 9/30); 9/24=1/5 official (closes 10/01); 9/25=0/5 official (closes 10/02); 9/26–9/27 weekend Day 0/5 (closes 10/02) / 1d maps to 9/28.

**Day N/21:** 8/26 1m closed after 9/25 (21st RTH). Oldest open 1m: **8/27 1m Day 20/21** (closes after 9/28).

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-25 Yahoo/MarketWatch RTH** O **$148.38** H **$149.67** L **$146.00** C **$148.68** Vol ~54.60M (+0.44% vs 9/24 C $148.03). Path high **$158.13** (9/21). Path low official **$145.88** (9/24). Last-5 TRs after 9/25 official 3.67/3.12/6.83/4.39/6.53 → median **$4.39**; 14d mean TR **$6.61**; differ ~34% ≥20% → use **$6.61**. Stacked floors: 1d/1w high ≥ **$156.28** (149.67+1.0×$6.61); 1d/1w low ≤ **$139.39** (146.00−1.0×$6.61). Rel Vol 54.6M / 20d ~89M ≈ 0.61x **below-avg**. Closed 1d last Daily-inserted **9/18**; Auditor closed **9/22 1d** + **9/23 1d** + **9/24 1d**. Auditor closed **9/17 1w** + **9/18 1w**. Auditor closed **8/26 1m**. Daily does not close 9/22 1w or 9/25 1d. **Write-streak: 0**. Daily 9/21 no table. Daily 9/22/9/23/9/24/9/25/9/26 rows locked. Daily 9/27 weekend insert. Prompt v1.25. Unlock **2026-09-24** cleared official. Next dated unlock **2026-10-09** remains inside next 10 RTH as of Sat 9/26 — keep known-event extra.

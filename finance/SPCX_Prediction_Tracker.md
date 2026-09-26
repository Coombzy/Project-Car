# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-25 official:** 9/15 1w closed after 9/22; 9/16 1w closed after 9/23; 9/17 1w closed after 9/24; 9/18=5/5 official pending Auditor close; 9/22=4/5 official; 9/23=3/5 official; 9/24=2/5 official; 9/25=1/5 official; 9/26 weekend / 1d maps to 9/28.

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-25 Yahoo/MarketWatch RTH** O **$148.38** H **$149.67** L **$146.00** C **$148.68** Vol ~54.60M (+0.44% vs 9/24 C $148.03). Path high **$158.13** (9/21). Path low official **$145.88** (9/24). Last-5 TRs after 9/25 official 3.67/3.12/6.83/4.39/6.53 → median **$4.39**; 14d mean TR **$6.61**; differ ~34% ≥20% → use **$6.61**. Stacked floors: 1d/1w high ≥ **$156.28** (149.67+1.0×$6.61); 1d/1w low ≤ **$139.39** (146.00−1.0×$6.61). Rel Vol 54.6M / 20d ~89M ≈ 0.61x **below-avg**. Closed 1d last Daily-inserted **9/18**; Auditor closed **9/22 1d** + **9/23 1d**. Auditor closed **9/17 1w**. Daily does not close 9/18 1w or 9/24 1d. **Write-streak: 0**. Daily 9/21 no table. Daily 9/22/9/23/9/24/9/25 rows locked. Daily **9/26** inserted. Prompt v1.24. Unlock **2026-09-24** cleared official. Next dated unlock **2026-10-09** remains inside next 10 RTH as of Sat 9/26 — keep known-event extra.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 9/02 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 158.13 | 148.03 |  |  |  | open | path L135.10 H158.13 Last148.68 |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 158.13 | 148.03 |  |  |  | open | path L135.10 H158.13 Last148.68 |

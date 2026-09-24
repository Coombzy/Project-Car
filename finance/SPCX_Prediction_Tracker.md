# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-23 official:** 9/15 1w closed after 9/22; 9/16 1w closed after 9/23; 9/17=4/5 official / 5/5 in progress on 9/24 (closes after 9/24 RTH); 9/18=3/5 official / 4/5 in progress; 9/22=2/5 official / 3/5 in progress; 9/23=1/5 official / 2/5 in progress; 9/24=0/5 official / 1/5 in progress.

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-23 Yahoo/MarketWatch RTH** O **$153.28** H **$154.26** L **$147.89** C **$148.36** Vol ~60.64M (−4.11% vs 9/22 C $154.72). **Live 2026-09-24 ~11:30 EDT** Last **~$147.19** H **$149.00** L **$145.88** vs 9/23 C $148.36 ≈ −0.79% / −$1.17 — no live-impulse. Path high **$158.13** (9/21). Path low live **$145.88**. Last-5 TRs after 9/23 official 5.99/6.67/6.53/4.39/6.83 → median **$6.53**; 14d mean TR **$7.20**; differ 10% <20% → use **$6.53**. Closed 1d last Daily-inserted **9/18**; Auditor closed **9/22 1d** on 9/23 official and recovered **9/23** Daily block (WRITE FAILED 403). **Write-streak: 0**. Daily 9/21 no table. Daily 9/22 rows locked. Daily 9/23 recovered by Auditor. Daily 9/24 rows locked. Prompt v1.24. Unlock stack **2026-09-24** is today's event (locked 9/24 rows). Next dated unlock **2026-10-09** remains inside next 10 RTH as of 9/25 — keep known-event extra after 9/24 official EOD.

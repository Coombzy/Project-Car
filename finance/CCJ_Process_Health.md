# CCJ Process Health Log

Lightweight tracker for long-term quality of the Analysis Automater and Audit Process.  
One short line per day. Does **not** replace the main living analysis log.

**Current prompt versions (as of 2026-10-08 audit):** Analysis **v1.17** · Audit **v1.4** · Write rules **v1.1** · **Calibration.md live**  
See `finance/CCJ_README.md`. Official cadence: Analysis **16:10 ET** weekdays · Audit 16:30 ET weekdays.

| Date       | Analysis Confidence | Audit Score | Top Issue / Note                          | Data Sources OK? |
|------------|---------------------|-------------|-------------------------------------------|------------------|
| 2026-10-08 | missed              | 10          | Official EOD Oct 2/5/6/7/8 MISSED; log deleted 156cd0a restored from 23a71b45 on branch ccj-audit-2026-10-08 (main PR-protected); audited Oct 1 EOD 10/10; Oct 1/Sep 30/29/28 1w CLOSED hit path H$94.57 C$87.12; Cal 27/31 1d 22/29 1w; prompt v1.17 no bump | Yes (Polygon) |
| 2026-10-01 | 86                  | 10          | Official EOD C$85.69 Rel 1.54x trend-down; 14th under 50-DMA; rule 7 OFF wick 0.60xATR; Sep 30 1d CLOSED hit C$85.69 pct_error 1.5%; Sep 24 1w CLOSED hit path L$83.80 C$85.69 pct_error 3.7%; Cal 26/30 1d 17/24 1w; Analysis missed tracker+Health (auditor backfill); prompt v1.17 no bump | Yes (Polygon) |
| 2026-09-30 | 86                  | 10          | Official EOD C$86.69 Rel 0.97x trend-down; 13th under 50-DMA; rule 7 ON wick 1.22xATR; Sep 29 1d CLOSED hit C$86.69 pct_error 0.4%; Cal 25/29; prompt v1.17 no bump | Yes (Polygon) |
| 2026-09-29 | 86                  | (pending)   | Official EOD catch-up C$86.88 Rel 0.74x trend-down; 12th under 50-DMA; Mon fail gate did not fire; log heading 68df4708; prompt v1.17 | Yes |
| 2026-09-29 | missed              | 10          | Official EOD Analysis heading MISSED then catch-up written 68df4708; audited existing Sep 28 EOD 10/10; Sep 28 1d CLOSED hit C$86.88 Rel 0.74x; fail gate did not fire; Cal refresh 24/28; prompt v1.17 no bump | Yes (Polygon) |
| 2026-09-28 | 86                  | 10          | Official EOD C$87.04 Rel 1.00x trend-down; 11th under 50-DMA; Fri fail gate; low undercut post-Q2 $86.38; Sep 25 1d + Sep 21 1w CLOSED hit; persist-close Sep 24 1d; Cal refresh; tracker grades + Sep 21 1w restore; prompt v1.17 | Yes |
| 2026-09-25 | 86                  | 10          | Official EOD C$88.06 Rel 0.63x trend-down; 10th under 50-DMA; light-vol inside day; Sep 24 1d + Sep 18 1w CLOSED hit; tracker backfill Sep 25 four rows; Cal refresh; prompt v1.16 no bump | Yes |
| 2026-09-24 | 86                  | 10          | Official EOD C$88.16 Rel 1.11x trend-down; 9th under 50-DMA; Sep 23 1d + Sep 17 1w CLOSED hit; persist-close Sep 18/21/22 1d + Sep 14/15/16 1w; Cal 3baf397; log still 2 headings; tracker backfill this run (0acaace); prompt v1.16 | Yes |
| 2026-09-23 | 86                  | 10          | Official EOD C$90.80 Rel 0.81x trend-down; 8th under 50-DMA; Sep 22 1d + Sep 16 1w CLOSED hit; persist-close Sep 18/21 1d + Sep 14/15 1w; Cal refresh; log STILL one-heading (restore 37e81b8d next Analysis); tracker backfill this run; prompt v1.15 | Yes |
| 2026-09-22 | 86                  | 10          | Official EOD C$94.59 Rel 1.05x trend-up; 7th session close under 50-DMA (H tagged through); Sep 18 1d + Sep 21 1d CLOSED hit; Sep 14 1w + Sep 15 1w CLOSED hit; Cal refresh; Analysis missed tracker append (auditor backfill); prompt v1.14 | Yes |
| 2026-09-21 | 86                  | 10          | Official EOD C$93.23 Rel 1.01x trend-down; 6th session under 50-DMA; pair flag vs U3O8 +1.76pp; Sep 18 1d CLOSED hit; audit notes left placeholder (write-rules newest-only); prompt v1.13 | Yes |
| 2026-09-18 | 86                  | 10          | Official EOD C$91.62 Rel 3.04x trend-down; 5th session under 50-DMA; spike-fade H$96.09 rule 7 ON; Sep 17 1d CLOSED hit; Sep 11 1w CLOSED hit; Cal refresh; Analysis missed tracker append (auditor backfill); prompt v1.13 | Yes |
| 2026-09-17 | 86                  | 10          | Official EOD C$92.80 Rel 0.78x trend-down; 4th session under 50-DMA; pair flag vs U3O8 +2.37pp; Sep 16 1d CLOSED hit; Sep 10 1w CLOSED hit; Cal refresh; Analysis missed tracker append (auditor backfill); prompt v1.13 | Yes |
| 2026-09-16 | 86                  | 10          | Official EOD C$90.90 Rel 0.71x; Sep 15 1d CLOSED hit; Sep 9 1w CLOSED hit; Sep 14 1d persist-close hit; Cal refreshed; Analysis missed tracker append + Health + log still truncated; auditor backfill; prompt v1.13 | Yes |
| 2026-09-15 | 86                  | 10          | Official EOD C$91.21 Rel 0.83x; Sep 14 1d CLOSED hit; Sep 8 1w CLOSED hit; Cal refreshed; Analysis missed tracker append (auditor backfilled); log still truncated (restore from dec2bfd2); prompt v1.13 | Yes |
| 2026-09-14 | 86                  | 10          | Official EOD C$93.26 Rel 1.26x trend-down; vol 50-DMA break; U3O8 +0.17% -3.71pp flag; Sep 11 1d CLOSED hit; Sep 4 1w CLOSED hit; Cal refreshed; Analysis missed tracker+log-restore; prompt v1.13 | Yes |

# CCJ Process Health Log

Lightweight tracker for long-term quality of the Analysis Automater and Audit Process.  
One short line per day. Does **not** replace the main living analysis log.

**Current prompt versions (as of 2026-09-17 audit):** Analysis **v1.13** · Audit **v1.4** · Write rules **v1.1** · **Calibration.md live**  
See `finance/CCJ_README.md`. Official cadence: Analysis **16:10 ET** weekdays · Audit 16:30 ET weekdays.

| Date       | Analysis Confidence | Audit Score | Top Issue / Note                          | Data Sources OK? |
|------------|---------------------|-------------|-------------------------------------------|------------------|
| 2026-09-17 | 86                  | 10          | Official EOD C$92.80 Rel 0.78x trend-down; 4th session under 50-DMA; pair flag vs U3O8 +2.37pp; Sep 16 1d CLOSED hit; Sep 10 1w CLOSED hit; Cal refresh; Analysis missed tracker append (auditor backfill); prompt v1.13 | Yes |
| 2026-09-16 | 86                  | 10          | Official EOD C$90.90 Rel 0.71x; Sep 15 1d CLOSED hit; Sep 9 1w CLOSED hit; Sep 14 1d persist-close hit; Cal refreshed; Analysis missed tracker append + Health + log still truncated; auditor backfill; prompt v1.13 | Yes |
| 2026-09-15 | 86                  | 10          | Official EOD C$91.21 Rel 0.83x; Sep 14 1d CLOSED hit; Sep 8 1w CLOSED hit; Cal refreshed; Analysis missed tracker append (auditor backfilled); log still truncated (restore from dec2bfd2); prompt v1.13 | Yes |
| 2026-09-14 | 86                  | 10          | Official EOD C$93.26 Rel 1.26x trend-down; vol 50-DMA break; U3O8 +0.17% −3.71pp flag; Sep 11 1d CLOSED hit; Sep 4 1w CLOSED hit; Cal refreshed; Analysis missed tracker+log-restore; prompt v1.13 | Yes |

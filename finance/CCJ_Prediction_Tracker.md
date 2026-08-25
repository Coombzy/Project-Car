# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

Last price context: 2026-08-25 RTH close CCJ **~$106.90** (L 102.75 H 107.77 Vol ~2.4M), prior close $102.27. Aug 24 1-day upper exceed on strong session.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-25 | 1d | 104.50 | 110.00 | 106.00 | 109.00 | 60 | | | | | | | open | Next session Wed 26 |
| 2026-08-25 | 1w | 102.00 | 115.00 | 107.00 | 112.00 | 55 | | | | | | | open | |
| 2026-08-25 | 1m | 100.00 | 125.00 | 110.00 | 120.00 | 55 | | | | | | | open | |
| 2026-08-25 | 3m | 110.00 | 145.00 | 120.00 | 135.00 | 55 | | | | | | | open | |
| 2026-08-24 | 1d | 99.50 | 104.50 | 100.50 | 103.00 | 55 | 102.75 | 107.77 | 106.90 | no (upper exceed) | strong extension | ~4.5% | closed | Missed upper on +4.5% 200-DMA reclaim |
| 2026-08-24 | 1w | 98.00 | 108.00 | 102.00 | 106.00 | 55 | | | ~106.9 | on-track | | | open | Day 2 |
| 2026-08-24 | 1m | 95.00 | 118.00 | 105.00 | 112.00 | 55 | | | ~106.9 | on-track | | | open | |
| 2026-08-24 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | | | | | | | open | Tracks prior 3m |
| 2026-08-23 | 1d | 99.50 | 106.00 | 101.00 | 104.00 | 60 | 100.29 | 103.73 | 102.38 | yes | mild digestion | ~0.1% | closed | Perfect range hit; close near bias mid |
| 2026-08-23 | 1w | 98.00 | 110.00 | 103.00 | 107.00 | 55 | | | ~106.9 | on-track | | | open | Day 2 of 5 |
| 2026-08-23 | 1m | 95.00 | 120.00 | 105.00 | 115.00 | 55 | | | ~106.9 | on-track | | | open | |
| 2026-08-23 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | | | | | | | open | |
| 2026-08-18 | 1d | 92.50 | 97.50 | 93.50 | 96.00 | 55 | 93.91 | 97.25 | 96.03 | yes | bounce | ~1.3% | closed | Close near bias high |
| 2026-08-18 | 1w | 90.00 | 100.00 | 93.00 | 97.00 | 55 | 93.91 | 102.82 | 102.51 | no (upper exceed) | recovery | ~7.9% vs bias mid | closed | Fri Rel Vol 1.32x rebound |
| 2026-08-18 | 1m | 88.00 | 110.00 | 96.00 | 105.00 | 50 | | | ~106.9 | on-track | | | open | Near/above bias |
| 2026-08-18 | 3m | 100.00 | 130.00 | 110.00 | 120.00 | 55 | | | | | | | open | |
| 2026-08-17 | 1d | 98.50 | 103.00 | 100.00 | 102.00 | 55 | 93.91 | 97.25 | 96.03 | no | wrong (down vs hold) | ~5.0% | closed | Failed $100 break on light vol |
| 2026-08-17 | 1w | 98.00 | 106.00 | 102.00 | 104.00 | 60 | 93.91 | 102.82 | 102.51 | partial | chop then reclaim | ~0.5% vs bias mid | closed | Range low broken; close inside |
| 2026-08-17 | 1m | 100.00 | 115.00 | 105.00 | 110.00 | 55 | | | ~106.9 | on-track (low) | | | open | |
| 2026-08-17 | 3m | 110.00 | 135.00 | 120.00 | 135.00 | 55 | | | | | | | open | |
| 2026-08-15 | 1d | 96.50 | 99.50 | 96.50 | 99.50 | 50 | 97.01 | 100.65 | 98.58 | partial | recovery | n/a | closed | High exceeded $100 |
| 2026-08-15 | 1w | 95.00 | 102.00 | 98.00 | 100.00 | 55 | 93.91 | 102.82 | 102.51 | no (both ends) | up | ~3.5% | closed | Failed-break then volume reclaim |
| 2026-08-15 | 1m | 92.00 | 110.00 | 100.00 | 105.00 | 50 | | | ~106.9 | on-track | | | open | |
| 2026-08-15 | 3m | 100.00 | 125.00 | 110.00 | 125.00 | 55 | | | | | | | open | |

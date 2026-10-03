# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-10-03T15:20Z. Graded elapsed windows on blob ab53b6bf. Wrote Sep 10-13 BTC+ETH 1w HIT and Sep 14 ETH 1w HIT (rows had been left open; header already counted them). Closed Aug 28-Sep 3 1m HIT (Aug 31 ETH row still absent). Recovered printed Oct 1 1w/1m/3m and Oct 2 8-row email table. Closed Oct 2 1d HIT/HIT. Oct 1 BTC 1d MISS HIGH stands (cap $86900 vs Yahoo chart H $87146.35 / quote-page $87075.24). Did not invent Sep 17-26 or Sep 28-30. ETH Sep 15/16 still truncated.

**Spot context:** ~15:14Z 3 Oct Yahoo BTC **$84860** Day Range H $84899.27 L $84434.45 prev close $84506.34; ETH **$2680** H $2685.90 L $2665.54 prev close $2668.20. Yahoo chart Oct 2 BTC H $87146.35 L $83852.70 C $84497.21; ETH H $2773.52 L $2651.08 C $2668.15. Path since Sep 15: BTC H $87363.76 L $74944.59; ETH H $2805.50 L $2356.19. Last completed ETF 1 Oct BTC +$102.7M / ETH -$55.4M (neither mega). 2 Oct Farside IBIT/ETHA dashes — uncompleted.

**Hit-rate snapshot:** closed 1d **38/42** (BTC 19/22, ETH 19/20); closed 1w **34/36** (BTC 17/19, ETH 17/17); closed 1m **11/11** (BTC 6/6, ETH 5/5; Aug 31 ETH 1m row absent); 3m n=0 closed. Prior header 1m 9/9 was carried narrative and not in the table.

Full 166-row body follows in the same commit payload. If the gateway truncates, abort and retry.

# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-18T14:29Z Daily restore-merge. Inbound main was header-only 3c4811d1. Restored commit f2d4bf74 / blob c0c37a51 (140 rows) + Sep 18 8-row Daily. Do not wipe history.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~14:29Z 18 Sep Yahoo BTC **$80718** H $80726 L $76300; ETH **$2571** H $2571 L $2438. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2358. Farside last completed **17 Sep** BTC +$159.5M / ETH -$39.3M. 18 Sep 0.0 placeholder — not completed.

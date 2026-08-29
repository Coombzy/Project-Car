# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-08-29T15:10Z (Coinbase). Closed 1d **n=2** (BTC hit, ETH hit). Aug 29 Daily Analysis ran (title “BTC/ETH digestion continues”) but wrote **no tracker rows**; notification email truncated before Forward Scenarios — bands not recovered, not invented. Aug 11–27 still unrestored.

**Hit-rate snapshot:** closed 1d **2/2**; 1w/1m/3m n=0 closed. Open 1w/1m/3m path-so-far: BTC on-track · ETH on-track (6/6).

**Spot context:** Coinbase 15:09 UTC BTC **$77,940** ETH **$2,444**. 1d window (28th 14:11Z → 29th 14:11Z) BTC H **$79,866** / L **$76,846** / close **$77,689**. ETH H **$2,527** / L **$2,406** / close **$2,436**. Farside 28 Aug US spot BTC ETFs **−$201.9M** (reversal from +$242.3M on 27 Aug); ETH ETFs **+$102.1M**. Weekend — no 29 Aug ETF print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs prior UTC close 80275 (−3.2%); below bias mid 79150 | 1.8% | closed | window 08-28 14:11Z→08-29 14:11Z (Coinbase 15m); H $79866 at 15:00Z 28th; L $76846 at 16:00Z 28th (US/JH session); C $77689 at 14:00–14:15Z 29th; parked-high +$20.5 on $81479 wick (0.008×ATR) did not exceed; Farside BTC ETF 28 Aug −$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76846 | 79866 | 77940 | on-track | fade vs 80275 |  | open | ~25h of 7d; Coinbase 15:09Z last $77940; width 4.0× ATR; window through ~09-04 14:11Z |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 76846 | 79866 | 77940 | on-track |  |  | open | path-so-far inside; 28 Aug ETF reversal −$202M after 27 Aug +$242M |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 76846 | 79866 | 77940 | on-track |  |  | open | ATH $126080 still distant; event-risk wide |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs prior 2512 (−3.0%); below bias mid 2485 | 2.0% | closed | same 24h window; H $2527 / L $2406 (16:00Z 28th) / C $2436; low $31 above floor (0.29×ATR $108); ETH ETFs 28 Aug +$102.1M |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2406 | 2527 | 2444 | on-track | fade vs 2512 |  | open | ~25h of 7d; Coinbase 15:09Z last $2444; ETHBTC ~0.0314; window through ~09-04 14:11Z |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2406 | 2527 | 2444 | on-track |  |  | open | path-so-far inside; ETH ETF inflows continued 28 Aug +$102M |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2406 | 2527 | 2444 | on-track |  |  | open | L2/ETF continuation vs macro; ATH $4946 distant |

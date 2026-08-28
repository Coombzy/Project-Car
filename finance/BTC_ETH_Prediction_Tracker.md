# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-08-28T15:25Z (Coinbase). Closed sample **n=0**. Daily Analysis Aug 11–27 produced no tracker rows; numeric bands not recovered from task metadata (titles only) — do not invent backfill. Aug 28 1d = `preliminary` (window through ~2026-08-29 14:11 UTC).

**Hit-rate snapshot:** closed 1d/1w/1m/3m = n/a. Preliminary 1d path-so-far: BTC yes · ETH yes (2/2).

**Spot context:** Coinbase 15:00 UTC BTC **$79,434** (UTC-day H **$81,479.50** / L **$78,432**) ETH **$2,506.50** (H **$2,535.55** / L **$2,468.48**). CoinGecko 24h BTC −1.6% / ETH −0.8%. Farside 27 Aug US spot BTC ETFs **+$242.3M**.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 78432 | 79866 | 79434 | yes | fade vs prior UTC close 80275; slight above bias mid 79150 | 0.4% | preliminary | ATR-proxy $2507; Warsh Jackson Hole; session rejected $81479; path since 14:00 UTC (Coinbase); high parked +$20.5 on printed wick (0.008×ATR) — window open until ~08-29 14:11Z |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 78432 | 79866 | 79434 | on-track |  |  | open | width 4.0× ATR; post Aug 19–21 impulse range under $81.5k; ~1h of window |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 78432 | 79866 | 79434 | on-track |  |  | open | 30d +23.8%; US spot BTC ETFs +$242M on Aug 27 |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 78432 | 79866 | 79434 | on-track |  |  | open | ATH $126080 still distant; event-risk wide |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2468 | 2527 | 2507 | yes | mild fade vs prior 2512; above bias mid 2485 | 0.9% | preliminary | ATR-proxy $108; ETHBTC 0.0315; path since 14:00 UTC (Coinbase); window open until ~08-29 14:11Z |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2468 | 2527 | 2507 | on-track |  |  | open | width 4.3× ATR; 2355–2567 post-impulse box; ~1h of window |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2468 | 2527 | 2507 | on-track |  |  | open | 30d +32.1%; US spot ETH ETFs +$235M on Aug 27 |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2468 | 2527 | 2507 | on-track |  |  | open | L2/ETF continuation vs macro; ATH $4946 distant |

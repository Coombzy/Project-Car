# SPCX Daily Analysis Prompt

**Version:** 1.13  
**Last edited:** 2026-09-11T16:20:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **SPCX** (Nasdaq: Space Exploration Technologies) with **numeric range bands** (not point targets only) that can be graded later.

- **Hit** = regular-session (or horizon-window) H/L/Close stayed inside the **range**, not only the bias. Range bounds are inclusive.
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.
- **1d window = the next regular session after `analysis_date`.** The Analysis job runs mid-session (~11:00 ET); do not grade 1d on leftover same-day minutes. 1w/1m/3m path starts at analysis as-of (includes the remainder of the analysis-date session + subsequent sessions).

## Process rules (always apply)

1. **ATR-proxy** — compute both (a) median true range of last 5 completed regular sessions and (b) published 14d ATR (Barchart acceptable). State both dollar values. **Range construction uses the larger** of the two when they differ by more than 20%.
2. **Regime:** `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a Rel Vol >= 1.0x trend-up close (close in the top third of the session range).
   - Rel Vol for `pred_rel_vol` is last completed regular session vs **20d** average volume (not Yahoo 3m / MarketWatch 65d).
   - **Live-session impulse (v1.6):** if (Last − last official RTH close) >= **+3%** OR >= **1.0 × ATR-proxy**, do **not** label digestion; default `trend-up`. Symmetric down → `trend-down`. **2026-09-09** titled digestion at −4.81% vs $153.47 — default `trend-down`.
   - **Post-write live-impulse (v1.10):** do not rewrite that day's bands after lock; path-refresh only.
3. **Range construction**
   - 1-day mandatory, next regular session. Width >= **2.0 × ATR-proxy**. On up live-impulse, `bias_low` >= Last. On down live-impulse, `bias_high` <= Last.
   - 1-week width >= **3.0 × ATR-proxy**; >= **4.0 ×** if last 5 include a **>= +5%** RTH.
   - Printed-high clearance: `range_high` >= max(last completed close, printed session high) + **0.5 × ATR**. Never park 1d/1w high on $149 / $150 / $155.
   - Coil-spring: Rel Vol < 0.5x → 0.75× high clearance; last 3 each < 0.6x → 1.0×. **2026-09-02** 1d high $149; 9/03 H $152.30 miss.
   - Known-event extra HIGH and LOW (v1.11): dated lock-up/unlock in next 10 RTH → +0.5×ATR to 1d/1w high AND −0.5×ATR from 1d/1w low. Next dated unlock **2026-09-24**. **2026-09-08** 1d low $144 held vs official 9/09 L $145.55.
   - Live-impulse extra is directional. Post-impulse high: last completed >= +5% or Rel Vol >= 1.0x + close in top third → 1.0× high clearance.
4. **Volume / confidence**
   - Buckets vs 20d: `<0.80x` below-avg; `0.80–1.19x` normal; `>=1.20x` elevated. Same value on all four rows. **2026-09-10** Vol ~118.60M / ~$82.0M ≈ 1.45x = elevated.
   - `prior_day_pct` = last completed official RTH % change. Rel Vol < 0.5x: cut 1d upside conf 10 pts.
5. Mid-session labels use **Last** (not Close). Confidence <= 80 until a completed close is the as-of.
6. Include prior-scenario vs actual from closed tracker rows.
7. Decision map: 3 bullets.
8. **Parseable table first.** No table = unrecoverable (**2026-09-01**).
9. Self-check must include payload-compact used yes/no and TRACKER_SHA present yes/no.
10. Non-session days: no new rows; still refresh path + Day N/5. Weekend SHA-reuse does not clear write-streak.
11. Close clocks: 1d = next RTH; 1w = 5th RTH after analysis_date; 1m = 21st; 3m = 63rd. **Day N/5 after 2026-09-11 begin:** 9/03=5/5 (open until 9/11 official close); 9/04=4/5; 9/08=3/5; 9/09=2/5; 9/10=1/5; 9/11=0/5.
12. pct_error format `X.X%`.
13. Official RTH source order: SpaceX IR if widget date matches, else Yahoo, else StockAnalysis / MarketWatch / Barchart. Stale-IR skip stands.
14. Session-day path maintenance + official-EOD replace. **Frozen closed notes (v1.12):** after a row is closed, do not grow that row's notes.
15. **Write-first / TRACKER_SHA gate.** Never emit `write pending`. Failed runs include **2026-09-10** WRITE FAILED after dual-write and **2026-09-11** SHA-reuse (emitted pre-write `6e4d34f3`).
   - Dual-write: create_or_update_file then push_files.
   - **Payload-compact (v1.12):** on size/schema reject, compact already-closed notes, retry both tools once, then WRITE FAILED + today's 4 rows only.
   - SHA-delta on session days. **v1.13:** if emitted TRACKER_SHA equals the pre-write blob SHA, that is WRITE FAILED — do not treat email as a write.
16. Price-quote cap before write.
17. **Write-streak emergency ON (v1.13).** Current streak: **3** (9/09 + 9/10 + 9/11). Emergency ON at >=3 consecutive session-day misses.
   - After two GitHub reads + one quote batch, use **only write tools** until a new 40-char blob SHA exists.
   - Compact already-closed notes **before** the first write attempt.
   - Confirm today's four `(analysis_date, horizon)` rows exist on a post-write get_file_contents before emitting TRACKER_SHA.

## Report structure

**Key Takeaway** (one sentence)
**Parseable table** (4 rows; skip non-session)
`TRACKER_SHA: <blob sha>`
1. Current Market Snapshot
2. Technical Analysis
3. Fundamental & News
4. Forward Scenarios (1d next session YYYY-MM-DD / 1w / 1m / 3m)
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory)

Get SHA immediately before write; retry once on conflict.
Session day: append four rows; path-refresh; Day N/5; official-EOD replace; freeze closed notes.
Never print `write pending`. Write-streak emergency is ON. Streak = 3. Dual-write + SHA-delta + payload-compact remain. Pre-write SHA emission = WRITE FAILED.

Cite sources. Be objective and data-driven.

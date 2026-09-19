# SPCX Daily Analysis Prompt

**Version:** 1.20  
**Last edited:** 2026-09-19T15:30:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **SPCX** (Nasdaq: Space Exploration Technologies) with **numeric range bands** (not point targets only) that can be graded later.

- **Hit** = regular-session (or horizon-window) H/L/Close stayed inside the **range**, not only the bias. Range bounds are inclusive.
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.
- **1d window = the next regular session after `analysis_date`.** The Analysis job runs mid-session (~11:00 ET); do not grade 1d on leftover same-day minutes. 1w/1m/3m path starts at analysis as-of (includes the remainder of the analysis-date session + subsequent sessions).
- **Live next-session 1d is `preliminary` until that session's official RTH close.** Auditor marks it; Daily does not close it mid-session. **2026-09-16** 1d closed on 9/17 official (L152.63 H156.87 C154.81; H156.87 > 156 miss). **2026-09-17** 1d closed on 9/18 official (L149.93 H156.60 C152.71 vs range 137–164 HIT; dir NO; pct_error 1.5%). **2026-09-18** 1d maps to 9/21 and stays open.

## Process rules (always apply)

1. **ATR-proxy** — compute both (a) median true range of last 5 completed regular sessions and (b) published 14d ATR / 14d mean TR. State both dollar values. **Range construction uses the larger** of the two when they differ by more than 20%. TR = max(H−L, |H−prevC|, |L−prevC|) — never raw H−L. Recompute after every official EOD; do not copy the prior header. **After 9/18 official:** last-5 TRs 6.56 / 5.68 / 9.52 / 5.99 / 6.67 → median **$6.56**; 14d mean TR **$6.88**; differ 5% <20% → use **$6.56**. Do not reuse after-9/17 median $5.99 / 14d $6.79. After a 1d upper-exceed, do not tighten the next 1d high vs the miss print solely because last-5 median fell.
2. **Regime:** `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a Rel Vol >= 1.0x trend-up close (close in the top third of the session range).
   - Rel Vol for `pred_rel_vol` is last completed regular session vs **20d** average volume (not Yahoo 3m / MarketWatch 65d).
   - **Live-session impulse:** if (Last − last official RTH close) >= **+3%** OR >= **1.0 × ATR-proxy**, do **not** label digestion; default `trend-up`. Symmetric down → `trend-down`. **2026-09-09** titled digestion at −4.81% vs $153.47 — default `trend-down`. **2026-09-16** live +5.34% / $7.66 vs ATR $6.56 — trend-up. **2026-09-18** mid-session Last $150.12 vs 9/17 C $154.81 = −3.03% — live-impulse-down tagged; 9/18 recovered rows stayed digestion (Daily lock; do not rewrite). Official 9/18 close −1.36% is not an impulse-down.
   - **Post-write live-impulse:** do not rewrite that day's bands after lock; path-refresh only.
3. **Range construction**
   - 1-day mandatory, next regular session. Width >= **2.0 × ATR-proxy**. On up live-impulse, `bias_low` >= Last. On down live-impulse, `bias_high` <= Last.
   - 1-week width >= **3.0 × ATR-proxy**; >= **4.0 ×** if last 5 include a **>= +5%** RTH.
   - Printed-high clearance: `range_high` >= max(last completed close, printed session high) + **0.5 × ATR**. Never park 1d/1w high on $149 / $150 / $155.
   - Coil-spring: Rel Vol < 0.5x → 0.75× high clearance; last 3 each < 0.6x → 1.0×. **2026-09-02** 1d high $149; 9/03 H $152.30 miss.
   - Known-event extra HIGH and LOW stack: dated lock-up/unlock in next 10 RTH → +0.5×ATR to 1d/1w high AND −0.5×ATR from 1d/1w low. **Stacks on top of printed-high/low clearance** — printed-high floor does not consume the extra. Next dated unlock **2026-09-24** (still inside next 10 RTH as of Mon 9/21). **2026-09-14** 1d high $159 short (required >=$163 and <=$139). **2026-09-15** insert applied stack: 1d 137–163. **2026-09-16** 1d high $156 = printed +0.5×ATR without extra; extra required range_high >= **$158.16**; official 9/17 H **$156.87 > 156 miss**. Do not rewrite locked 9/16 bands. **2026-09-18** recovered 1d high $161 is short of stacked floor (~$162.59 using $5.99); do not rewrite. **Monday 9/21 stacked floors using $6.56:** 1d/1w high >= 156.60 + 1.0×$6.56 = **$163.16**; 1d/1w low <= 149.93 − 1.0×$6.56 = **$143.37**. If stacked 1d high floor > printed range_high, widen range_high **before lock** (same for the low). Self-check must print stacked floors.
   - Live-impulse extra is directional. Post-impulse high: last completed >= +5% or Rel Vol >= 1.0x + close in top third → 1.0× high clearance.
4. **Volume / confidence**
   - Buckets vs 20d: `<0.80x` below-avg; `0.80–1.19x` normal; `>=1.20x` elevated. Same value on all four rows. **2026-09-16** official Vol ~108.77M / 20d ~$77.54M ≈ **1.40x elevated**. **2026-09-17** official Vol ~83.99M / 20d ~$77.93M ≈ **1.08x = normal**. **2026-09-18** official Vol ~335.22M / 20d ~$77.89M ≈ **4.30x elevated** (real spike, not a bad print). Last completed on a 9/19+ / Monday 9/21 run is **9/18 official**, not 9/17. Do **not** reuse 9/17 `normal` / `prior_day_pct=+2.60`. **2026-09-18** recovered rows used `pred_rel_vol=normal` and `prior_day_pct=+2.60` (locked; do not rewrite). Rel Vol >= 3.0x on last completed must flow into the next session's `pred_rel_vol`.
   - `prior_day_pct` = last completed official RTH % change. Monday 9/21 = **−1.36**. Rel Vol < 0.5x: cut 1d upside conf 10 pts.
5. Mid-session labels use **Last** (not Close). Confidence <= 80 until a completed close is the as-of.
6. Include prior-scenario vs actual from closed tracker rows.
7. Decision map: 3 bullets.
8. **Parseable table first.** No table = unrecoverable (**2026-09-01**).
9. Self-check must include payload-compact used yes/no and TRACKER_SHA present yes/no. Self-check must also print known-event extra stacked yes/no with the resulting 1d high/low floors.
10. Non-session days: no new rows; still refresh path + Day N/5. Weekend SHA-reuse does not increment write-streak.
11. Close clocks: 1d = next RTH; 1w = 5th RTH after analysis_date; 1m = 21st; 3m = 63rd. **Day N/5 after 2026-09-18 official:** 9/11=5/5 (closed 9/18); 9/14=4/5; 9/15=3/5; 9/16=2/5; 9/17=1/5; 9/18=0/5. Weekend 9/19–20 no increment. 9/11 1w closed after 9/18 official. 9/14 1w closes after 9/21 official.
12. pct_error format `X.X%` = |close − bias midpoint| / bias midpoint. Do not store the session % change.
13. Official RTH source order: SpaceX IR if widget date matches, else Yahoo, else StockAnalysis / MarketWatch / Barchart. Stale-IR skip stands.
14. Session-day path maintenance + official-EOD replace. **Frozen closed notes:** after a row is closed, do not grow that row's notes.
15. **Write-first / TRACKER_SHA gate.** Never emit `write pending`. Failed runs include **2026-09-10** WRITE FAILED after dual-write, **2026-09-11** SHA-reuse (emitted pre-write `6e4d34f3`), and **2026-09-18** Daily email table + WRITE FAILED (no GitHub tools; Auditor recovered the 4 rows from that table).
   - Dual-write: create_or_update_file then push_files.
   - **Payload-compact:** on size/schema reject, compact already-closed notes, retry both tools once, then WRITE FAILED + today's 4 rows only.
   - SHA-delta on session days. If emitted TRACKER_SHA equals the pre-write blob SHA, that is WRITE FAILED — do not treat email as a write.
16. Price-quote cap before write.
17. **Write-streak emergency OFF.** Streak **0** after 9/14 session-day 4-row INSERT commit **3470d780** / blob **6a6e68f3**. Auditor 9/16 restore **304384dd** / blob **9a0e50bc**. Dual-write + SHA-delta + payload-compact remain. If a future session day emits pre-write SHA or drops today's 4 rows, streak returns to 1 and emergency ON.
   - Confirm today's four `(analysis_date, horizon)` rows exist on a post-write get_file_contents before emitting TRACKER_SHA.
   - Daily inserts session-day rows; Auditor grades / path-refreshes / closes only. Auditor may recover a Daily block that Daily already attempted and failed to write. Do not invent next-session rows.
18. **Anti-wipe (v1.20):** never push a header-only tracker or prompt. Outbound tracker must contain ≥ inbound data-row count and ≥64 data rows. Commit **6a61d877** deleted the table (header-only blob 46a34efb) and truncated the prompt (blob 681c52ab). Restore tracker from 5e9cc670 / 0d488b02 or 304384dd / 9a0e50bc. Restore prompt from b32acbc7 / 1f19bf84 (v1.17 body) if main is stub-only.

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

Self-check: `1d width $X vs ATR-proxy $Y (last-5 med $A / 14d $B; used larger yes/no); 1d maps to next session YYYY-MM-DD; last completed Rel Vol Z.Zx vs 20d; 1d high $C vs last session high $D; coil-spring 0.5/0.75/1.0x; known-event extra stacked yes/no + 1d high/low floors; live-impulse dir up/down/no; post-impulse-high yes/no; write-streak emergency yes/no; dual-write used yes/no; payload-compact used yes/no; SHA-delta session-day yes/n/a; pred_rel_vol same on all 4 rows yes/no; Day N/5 after-only yes/no; TRACKER_SHA present yes/no; anti-wipe row-count >=64 yes/no.`

## GitHub write (mandatory)

Get SHA immediately before write; retry once on conflict.
Session day: append four rows; path-refresh; Day N/5; official-EOD replace; freeze closed notes.
Never print `write pending`. Write-streak emergency is OFF. Streak = 0. Dual-write + SHA-delta + payload-compact remain. Pre-write SHA emission = WRITE FAILED.

Cite sources. Be objective and data-driven.

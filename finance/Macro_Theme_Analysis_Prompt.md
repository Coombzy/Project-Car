# Macro Industry Theme Map — Analysis Prompt

**Version:** 1.2 (2026-08-26)  
**Last edited:** 2026-08-26 18:15 UTC  
**Supersedes:** v1.1 (ETF-first book; 30/60/90 only)  
**Source of v1.2 user edits:** Grok automation **Macro Alpha** (`b78c3446-…`) — rank by upside × chance; prefer single stocks; 3 names per theme.  
**Location:** `Project-Car/finance/`

Read `finance/Macro_WRITE_RULES.md` and `finance/Macro_README.md` first. Not financial advice. Selection support only — no position sizes.

## Goal

Turn the last ~72h of macro / policy / geopolitical news into **at most 3 themes**, each with industry beneficiaries AND hurt side, liquid proxies **and 3 single-stock picks**, **horizon_days**, **% change range**, falsifier, and action. Persist the write-up in the log and append tracker rows for grading.

**Priority:** if more than 3 durable candidates exist, keep the 3 with the **highest potential upside %** and the **highest chance of seeing it**. Score each candidate as `(conf / 100) × pct_high` of its best *benefit* name. State the score in the log. Do not pick a high-upside / low-conf lottery over a medium-upside / higher-conf theme.

If nothing durable, output **0–1** themes and say so — do not invent.

## Hard rules

1. Max **3** themes. Overlaps are **overlay proxies or notes**, not a 4th `theme_id`.
2. Skip celebrity noise, single-name *earnings-only* stories, empty "AI changes everything."
3. **Prefer single stocks with high potential for large % changes.** Names must still be **liquid enough to grade** (primary listing NYSE / Nasdaq / TSX; no OTC/pinks; skip thin story stocks). ETFs remain OK as *hurt-side baskets* or when no clean liquid name exists.
4. Every proxy **and every stock pick** MUST have: `horizon_days` ∈ {14, 30, 60, 90}, `pct_low`, `pct_high`, `conf` (40–85), `spot_at_call`, `due_date`, proxy-specific `falsifier`. (v1.1 banned 14 — v1.2 restores it to match Macro Alpha. Do **not** use 45.)
5. % ranges = expected **total return %** over `horizon_days`. Widen when uncertain; do not fake tight precision.
6. Benefit side → range bias above 0; hurt → bias below 0 when conviction exists.
7. `theme_id` format: `YYYYMMDD-slug`
8. `action`: `watch` | `deep-dive` | `ignore`. **At most one `deep-dive` per run.** Default `watch`. Use `ignore` when the move is already priced.
9. **Do not change** ranges/horizons on already-open tracker rows. New idea = new row.
10. Per theme: **suggest 3 best stocks** (usually benefit-side convexity; 1 of 3 may be the cleanest hurt-side name). If a pick is also a proxy, **one tracker row** — do not duplicate.

## Proxy / pick quality

- **No duplicate beta.** Do not book XLE and USO as two tests of the same oil move. One oil-price expression max per theme (name *or* ETF).
- **Match the barrel / region.** Global autos (CARZ) is not a NA supply-chain name. Country ETF (EWC) is not Alberta energy (XEG or SU / CNQ).
- **Mixed sector ETFs** (XLE, XLF) need a one-line why they beat a single name, or pick the name (e.g. SU, CNQ, COP, JPM, KRE).
- Record **spot_at_call**: last print if known; else the **driver** (e.g. `Brent 86.3`, `WCS-WTI ~16`). Never leave blank.
- `due_date` = analysis_date + horizon_days (ISO date).
- In tracker `notes`: `pick` (single stock) or `basket` (ETF).

## Overlap / stack scan (required)

After drafting ≤3 themes, check every pair for a **shared industry** that is hit by both mechanisms.

Ask, in the log, for each pair:

1. Same cash-flow line (price, volume, cost, FX, policy)?
2. Is the second theme actually a **customs duty** on that line, or only a political/cost tail?
3. Does the stack change **sign** if one theme falsifies?

If the stack is material:

- Attach **overlay proxies / picks** to the **primary** theme (do not create a 4th theme_id).
- State the **state-dependent sign** (e.g. Hormuz thaw → Alberta hurt; Hormuz fail → Alberta relative benefit vs EWC).
- Use a **relative pair** when the stack is about underperformance (XEG vs XOP, SU vs COP), not only an absolute long/short.

Worked example (2026-08-26, keep as prior):

- US Section 338 50% list **excludes energy, potash, fish, critical minerals**. Do not claim a 50% tariff on Alberta crude unless that exemption is reversed.
- Hormuz thaw hits Alberta via (a) lower WTI/Brent **and** (b) returning Gulf heavies widening **WCS–WTI** **and** (c) fading TMX Asia scarcity bid.
- Canada fight stacks via **oil-as-weapon politics** (Ottawa/Ford withhold risk) and **steel capex costs**, plus CAD FX cushion — not via the 50% crude line.
- Required tell when oil + Canada are both live: **WCS–WTI differential**, not Brent alone.
- v1.2 names for that overlay (examples, not a standing book): SU, CNQ, CVE on the hurt side vs COP / PSX on the US side — only if liquid and not already open with frozen ranges.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest log entry + **all open** tracker rows + last 5 closed (if any).
2. Collect ~72h macro/policy/geo news. Cite sources. Record driver spots (Brent, WTI, WCS differential if oil is in play, 10y/30y if fiscal/Fed is in play).
3. Draft candidate themes. **Score** `(conf/100) × pct_high` on the best benefit name. Keep the top ≤3. Run **overlap scan**. Attach overlays.
4. For each kept theme: 3 stock picks + any basket overlay. Enforce uniqueness + {14,30,60,90} + snapshots + proxy-specific falsifiers. At most one `deep-dive`.
5. Quality self-check: duplicate-beta? illiquid name? already-priced `ignore`? energy exemption checked? ranking scores shown? log will be commitable?
6. Commit **log first** (prepend one entry). Get SHA immediately before write.
7. Append tracker rows (`status=open`) for every unique ticker (picks + baskets). Get SHA immediately before write. Retry once on conflict.
8. Report commit SHA(s) in the chat output.

## Output structure (chat + log)

**Key Takeaway** (one sentence)

**Overlap scan** (short; "none" is allowed if true)

**Ranking** (one line per candidate: score = conf/100 × pct_high; which 3 kept / which dropped)

For each theme:
- theme_id, title, mechanism (2–4 sentences)
- **3 best stocks** (ticker · side · why one line)
- horizon_days + why
- Beneficiaries / Hurt (industries)
- Proxies / picks table: ticker | side | pct_low | pct_high | conf | action | spot_at_call | pick_or_basket
- Falsifier (per ticker if they differ)
- Action (theme-level; deep-dive only if a ticker is deep-dive)

Then: Calibration line (from closed rows if any) + Disclaimer.

## Tracker row contract

Columns: `analysis_date, theme_id, theme, side, industry, proxy, horizon_days, pct_low, pct_high, conf, falsifier, action, spot_at_call, due_date, source_note, actual_pct, hit_range, hit_dir, status, graded_date, notes`

Fill the first 15 at analysis time; leave actual_* / hit_* / graded_date blank; `status=open`. `proxy` holds the ticker (stock or ETF). `notes` starts with `pick` or `basket`.

## Success criteria

- [ ] WRITE_RULES followed (SHA, prepend log, append tracker, no range edits on open rows)
- [ ] Prompt file present and version cited (v1.2+)
- [ ] ≤3 themes; ranking scores in the log; overlap scan in the log
- [ ] 3 stock picks per kept theme (or explicit reason if fewer)
- [ ] No duplicate-beta pair; no OTC/thin names
- [ ] Horizons in {14,30,60,90}; snapshots + due_date filled
- [ ] ≤1 deep-dive; energy exemption checked if Canada + oil both appear
- [ ] Commit SHAs reported

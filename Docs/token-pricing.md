# Shop OS token pricing (v1)

**Status:** Living one-pager — product lock  
**Locked:** 2026-09-06 (Ben GO)  
**Shop TZ:** `America/Regina`  
**Related:** `project-car-application-specification.md` §5, `STATUS.md`

How many tokens a hoist slot **costs** at reserve time. Not dollars. Not public brochure prices. Not live until Ben says the shop is open. **No Stripe.**

This file is the lock. Implement later (not this docs PR). Do not invent API, Cloudflare, Apex, or Mission Control work from here.

---

## Stack (locked)

1. **PRIMARY — rate band.** Time-of-day / day-of-week in shop local TZ `America/Regina`. Owner-editable settings table.
2. **OVERLAY — advance / last-minute.** Applied at **reserve time** on top of the band rate.
3. **UI must show the math.** Band + overlay + total before confirm. Existing Shop OS UX must-haves stay (below).

```
final_reserve_cost = base_tokens × band_multiplier × advance_multiplier
```

Order is locked: base, then band, then overlay. Show all three factors and the total before confirm. Lock the same numbers onto the reserve ledger row (`pricing_rule` in meta). Cancel / complete **refund or debit that reserved amount** — do not reprice if bands or overlays change later.

`base_tokens` is the unadjusted slot cost (today: Owner-entered reserve amount; later a duration rule if Ben locks one). Bands and overlay never replace the append-only ledger.

---

## Still true from Shop OS §5

- Append-only token ledger. Never edit history.
- Create **reserves** (`booking_reserve`) → complete **debits** used (`booking_debit`) and **refunds** unused reserve (`booking_refund`) → cancel refunds remaining reserve.
- `member.token_balance` is a **cache** of the ledger. Ledger wins.
- Tier `included_tokens`, `booking_window_days`, and `max_simultaneous_bookings` stay enforced.
- Overdue does **not** auto-charge money.

---

## Surfaces

Token balance + hoist booking is a **primary Member** page — not Owner-only admin. Pricing math applies to **Member bookings** the same as Owner-created ones.

| Who | What |
|-----|------|
| **Owner** | Tiers, band / overlay settings, overrides, at-risk, everyone else's ledger. Still required. |
| **Member** | See their own balance, book / cancel within tier rules, see **band + overlay + total** on their schedule. |

Member self-serve UI is **not live**. Lock the surfaces now so the next product slice is not a vague v2 dump.

---

## Default bands (Owner-editable placeholders)

Hours are **approximate defaults**. Multipliers are placeholders Ben can edit in the settings table. Do not treat them as public prices.

**Fri-evening ambiguity (resolved for the default table):** “after ~16:00 or ~18:00” — default is **Fri 16:00–24:00** at weekend/Fri-eve premium **1.5×**, not the weekday-eve **1.25×**.

Intervals are half-open `[start, end)` in `America/Regina`. Price a booking from the band that contains its **start**. Spanning bands does not split the slot in v1.

| Band id | When (`America/Regina`) | × | Label |
|---------|-------------------------|---|-------|
| `weekday_day` | Mon–Fri 08:00–16:00 | **1.0** | Weekday day (base) |
| `weekday_eve` | Mon–Thu 16:00–21:00 | **1.25** | Weekday evening |
| `weekend_fri_eve` | Fri 16:00–24:00; Sat all day; Sun 00:00–21:00 | **1.5** | Weekend / Fri eve |
| `late_night` | Mon–Thu 21:00–08:00 next day; Sun 21:00–Mon 08:00 | **0.75** | Late night / early morning |

Week grid (same defaults):

| | 00:00–08:00 | 08:00–16:00 | 16:00–21:00 | 21:00–24:00 |
|---|---|---|---|---|
| Mon | 0.75 (`late_night`, Sun→Mon) | 1.0 | 1.25 | 0.75 |
| Tue–Thu | 0.75 | 1.0 | 1.25 | 0.75 |
| Fri | 0.75 (Thu night) | 1.0 | **1.5** | **1.5** |
| Sat | 1.5 | 1.5 | 1.5 | 1.5 |
| Sun | 1.5 | 1.5 | 1.5 | 0.75 (Sun→Mon) |

Shop OS on `main` still labels schedule cells `America/Edmonton`. When pricing is implemented, shop-local TZ for bands **and** the week view must be `America/Regina`. Do not change that in this docs PR.

---

## Default advance overlay (on top of band)

Measured at **reserve time**: now → booking start, shop TZ.

| Ahead of start | × | Label |
|----------------|---|-------|
| ≥ 7 days | **0.85** | Advance |
| 48 hours – 7 days | **1.0** | Standard |
| < 48 hours | **1.25** | Last-minute |

Boundaries: exactly 7 days → 0.85×; exactly 48 hours → 1.0×.

Same rule: Owner-editable placeholders, not public prices.

---

## `pricing_rule` on ledger meta

Every `booking_reserve` (and the matching debit / refund rows) stores the math. Never hide it.

```json
{
  "pricing_rule": {
    "band_id": "weekday_eve",
    "band_label": "Weekday evening",
    "band_multiplier": "1.25",
    "overlay_id": "last_minute",
    "overlay_label": "Last-minute",
    "advance_multiplier": "1.25",
    "base_tokens": "2",
    "final_reserve_cost": "3.13",
    "tz": "America/Regina"
  }
}
```

`final_reserve_cost` is what is reserved, refunded, or debited. Cancel does not re-run the table.

---

## UX must-haves (non-optional)

1. **Create booking.** Show `base × band × overlay = total`, balance **before** and **after**, plus **band label** and **overlay label**, before confirm / reserve.
2. **Week schedule cells.** Band color + token-cost badge. Overlay chip when overlay ≠ 1.0.
3. **Member detail.** Balance + recent ledger. **At-risk** when open reserved tokens **>** remaining (cached) free balance.
4. **Cancel / complete.** Show refund or debit **inline** (the locked reserved amount).
5. **Never hide math.** `pricing_rule` (band id + multipliers + factors + total) on ledger meta; surface it on the ledger, not only in a tooltip.

Existing Owner chrome stays: hoist overlap, reserve → debit / refund, token-at-risk on the dashboard, demo seed is not “shop is open.”

---

## Worked example (defaults only)

Tuesday 17:00 start, reserved **20 hours** ahead, `base_tokens = 2`.

- Band: `weekday_eve` **1.25×**
- Overlay: 48h–7d **1.0×**
- Total: `2 × 1.25 × 1.0 = 2.50` tokens reserved

Same slot reserved **30 hours** ahead: overlay **1.25×** → `2 × 1.25 × 1.25 = 3.13`.

---

## Out of scope

- No API / settings-table implementation in the PR that added this file.
- No Cloudflare. No Apex. No Mission Control cockpit.
- No Stripe. No “shop is open.” Do not put these multipliers on projectcar.ca.

---

**Approved by:** Ben (2026-09-06 GO: bands primary, overlay on top, UI shows the math; Member balance + booking is a primary customer surface)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`

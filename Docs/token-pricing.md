# Shop OS token pricing (v1)

**Status:** Living one-pager — product lock  
**Locked:** 2026-09-06 (Ben GO)  
**Shop TZ:** `America/Regina`  
**Related:** `project-car-application-specification.md` §5, `STATUS.md`

How many tokens a hoist slot **costs** at reserve time. Not dollars. Not public brochure prices. Not live until Ben says the shop is open. **No Stripe.**

This file is the lock. Owner booking now computes reserve in the API. Do not invent Cloudflare, Apex, or Mission Control work from here.

---

## Stack (locked)

1. **PRIMARY — rate band.** Time-of-day / day-of-week in shop local TZ `America/Regina`. Owner-editable settings table.
2. **OVERLAY — advance / last-minute.** Applied at **reserve time** on top of the band rate.
3. **UI must show the math.** Band + overlay + total before confirm. Existing Shop OS UX must-haves stay (below).

```
base_tokens = hours × 100
final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier
```

**`base_tokens` is duration × 100.** One hundred tokens per hour of hoist time. Not an arbitrary Owner-entered reserve amount.

`hours` is the booking duration (end − start) in shop-local time. Fractional hours are allowed (`1.5` → `150`). Order is locked: duration base, then band, then overlay. Show all three factors and the total before confirm. Lock the same numbers onto the reserve ledger row (`pricing_rule` in meta). Cancel / complete **refund or debit that reserved amount** — do not reprice if bands or overlays change later.

Bands and overlay never replace the append-only ledger. Owner create (`POST /bookings`) computes this in the API and ignores any client `tokens` field.

---

## Still true from Shop OS §5

- Append-only token ledger. Never edit history.
- Create **reserves** (`booking_reserve`) → complete **debits** used (`booking_debit`) and **refunds** unused reserve (`booking_refund`) → cancel refunds remaining reserve.
- `member.token_balance` is a **cache** of the ledger. Ledger wins.
- Tier `included_tokens`, `booking_window_days`, and `max_simultaneous_bookings` stay enforced.
- Overdue does **not** auto-charge money.
- Two membership tiers in seed (not three). Allotments below.

---

## Membership allotments (two tiers)

Two tiers. One includes more tokens per period than the other. **Names and dollar prices stay Owner-editable.** Included-token counts below are **Owner-editable placeholders, not public prices.** Do not put them on projectcar.ca.

| Placeholder name | `included_tokens` / period |
|------------------|----------------------------|
| Basic | **400** |
| Pro | **800** |

No third **Weekly** tier in this lock. Drop it from seed notes and seed tier rows. Owner can still add or rename tiers later in data — this is not a schema ban.

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

Shop OS week cells and naive `datetime-local` values still use the existing `shop_time` helper `SHOP_TZ` = `America/Edmonton` (Owner labels stay `America/Edmonton`). Band and overlay math use `PRICING_TZ` = `America/Regina`. During Mountain Daylight both are UTC−6, so clock times match. In winter Edmonton is UTC−7 and Regina stays UTC−6 — the engine converts the stored UTC instant to Regina before picking a band.

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
    "hours": "2",
    "base_tokens": "200",
    "final_reserve_cost": "312.50",
    "tz": "America/Regina"
  }
}
```

`final_reserve_cost` is what is reserved, refunded, or debited. Cancel does not re-run the table.

---

## UX must-haves (non-optional)

1. **Create booking.** Show `(hours × 100) × band × overlay = total`, balance **before** and **after**, plus **band label** and **overlay label**, before confirm / reserve.
2. **Week schedule cells.** Band color + token-cost badge. Overlay chip when overlay ≠ 1.0.
3. **Member detail.** Balance + recent ledger. **At-risk** when open reserved tokens **>** remaining (cached) free balance.
4. **Cancel / complete.** Show refund or debit **inline** (the locked reserved amount).
5. **Never hide math.** `pricing_rule` (band id + multipliers + factors + total) on ledger meta; surface it on the ledger, not only in a tooltip.

Existing Owner chrome stays: hoist overlap, reserve → debit / refund, token-at-risk on the dashboard, demo seed is not “shop is open.”

---

## Worked example (defaults only)

Tuesday 17:00 start, **2-hour** slot, reserved **20 hours** ahead.

- Base: `2 × 100` = **200**
- Band: `weekday_eve` **1.25×**
- Overlay: 48h–7d **1.0×**
- Total: `200 × 1.25 × 1.0 = 250` tokens reserved

Same 2-hour slot reserved **30 hours** ahead: overlay **1.25×** → `200 × 1.25 × 1.25 = 312.50`.

---

## Out of scope

- Owner-editable settings table for bands / overlays (v1 ships the default table in code).
- No Cloudflare. No Apex. No Mission Control cockpit.
- No Stripe. No “shop is open.” Do not put these multipliers on projectcar.ca.
- Member self-serve booking UI.

---

## Later (not v1)

Member-to-member hoist time trades/offers: bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only — do not design the trade system here, and do not put trades in v1 pricing rules.

---

**Approved by:** Ben (2026-09-06 GO: bands primary, overlay on top, UI shows the math; Member balance + booking is a primary customer surface. 2026-09-06 recall: `base_tokens = hours × 100`; two tiers, Basic 400 / Pro 800 placeholders.)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`

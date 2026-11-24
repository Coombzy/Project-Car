# ADR 0007: Locked token pricing doc

**Status:** accepted

**Decision:** Token reserve/debit rates and pricing stack rules live in `Docs/token-pricing.md` and are locked (Ben GO 2026-09-06). The API computes reserve cost from bands, overlays, and fill; the ledger is append-only. Agents do not invent rates, token ids, or vehicle lists the owner must supply.

**Why:** Pricing is a one-way door; mismatched math breaks member trust and ledger integrity.

**Source:** `Docs/token-pricing.md`; `PricingBand`, `PricingOverlay`, `TokenTransaction` in `app/models.py`.

**Consequences:** Read `Docs/token-pricing.md` before changing booking pricing. Never edit ledger history to “fix” totals.
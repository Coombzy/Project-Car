"""Payment collection. A real processor replaces the stand-in behind this interface.

The stand-in does not call a network. It accepts a STANDIN- payment id, or
mints one, and prices GST at the same rate as the token ledger.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.config import get_settings
from app.services.tokens import GST_RATE, _cents


@dataclass(frozen=True)
class PaymentReceipt:
    processor: str
    payment_id: str
    subtotal_cad: Decimal
    gst_cad: Decimal
    total_cad: Decimal


class PaymentProcessor(Protocol):
    name: str

    def collect(
        self,
        *,
        member_id: UUID,
        tokens: Decimal,
        subtotal_cad: Decimal,
        payment_id: str | None,
    ) -> PaymentReceipt:
        """Take the money and return the receipt the ledger will store."""


class StandInPaymentProcessor:
    """Placeholder until a processor is connected. Ids start with STANDIN-."""

    name = "stand-in"

    def collect(
        self,
        *,
        member_id: UUID,
        tokens: Decimal,
        subtotal_cad: Decimal,
        payment_id: str | None,
    ) -> PaymentReceipt:
        del member_id, tokens
        subtotal = _cents(subtotal_cad)
        if subtotal <= 0:
            raise HTTPException(
                status_code=422,
                detail={"code": "invalid_amount", "message": "The before-tax amount must be greater than zero."},
            )
        chosen = (payment_id or "").strip()
        if not chosen:
            chosen = f"STANDIN-{uuid4().hex[:12].upper()}"
        if not chosen.startswith("STANDIN-"):
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "standin_only",
                    "message": "The stand-in processor only accepts a STANDIN- payment id.",
                },
            )
        gst = _cents(subtotal * GST_RATE)
        return PaymentReceipt(
            processor=self.name,
            payment_id=chosen,
            subtotal_cad=subtotal,
            gst_cad=gst,
            total_cad=subtotal + gst,
        )


def get_payment_processor(name: str | None = None) -> PaymentProcessor:
    chosen = get_settings().payment_processor if name is None else name
    if chosen == "stand-in":
        return StandInPaymentProcessor()
    raise HTTPException(
        status_code=500,
        detail={
            "code": "unknown_processor",
            "message": f"No payment processor is registered for {chosen}.",
        },
    )

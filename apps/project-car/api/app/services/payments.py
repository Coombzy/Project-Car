"""Payment collection. A real processor replaces the stand-in behind this interface.

The stand-in does not call a network and does not credit a client-chosen token
count. The owner purchase route is the manual stand-in until a processor
returns a payment id and the server picks the pack.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from fastapi import HTTPException

from app.config import get_settings


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
    """Placeholder until a processor is connected. It does not take money."""

    name = "stand-in"

    def collect(
        self,
        *,
        member_id: UUID,
        tokens: Decimal,
        subtotal_cad: Decimal,
        payment_id: str | None,
    ) -> PaymentReceipt:
        del member_id, tokens, subtotal_cad, payment_id
        raise HTTPException(
            status_code=403,
            detail={
                "code": "owner_records_purchases",
                "message": (
                    "The stand-in does not credit a member-chosen token count. "
                    "The owner records a purchase the owner has seen."
                ),
            },
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

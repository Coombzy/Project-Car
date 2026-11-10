"""Payment collection. Only the stand-in is registered.

The stand-in does not call a network, does not use an API key or a merchant
account, and does not apply a fee rate. Payment ids it accepts or mints start
with STANDIN-. The CAD amount posted by the caller is the amount recorded.
STAND_IN_FEE_RATE is the label for that missing rate. It is not a number.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.config import get_settings

# Named stand-in. A real fee rate is not applied and is not invented.
STAND_IN_FEE_RATE = "stand-in-none"
_CENTS = Decimal("0.01")
_MAX_AMOUNT = Decimal("100000000")
_STAND_IN_NAME = "stand-in"
_STAND_IN_PREFIX = "STANDIN-"


@dataclass(frozen=True)
class PaymentReceipt:
    processor: str
    payment_id: str
    amount_cad: Decimal
    tokens: Decimal
    fee_rate: str


class PaymentProcessor(Protocol):
    name: str

    def collect(
        self,
        *,
        member_id: UUID,
        tokens: Decimal,
        amount_cad: Decimal,
        payment_id: str | None,
    ) -> PaymentReceipt:
        """Take the money and return the receipt the ledger will store."""


def _http(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _amount_cad(value: Decimal) -> Decimal:
    amount = Decimal(value)
    exponent = amount.as_tuple().exponent
    if not isinstance(exponent, int) or exponent < -2 or amount <= 0 or amount >= _MAX_AMOUNT:
        raise _http(
            422,
            "invalid_amount",
            "Enter an amount greater than zero and under 100,000,000, with at most 2 decimal places.",
        )
    return amount.quantize(_CENTS, rounding=ROUND_HALF_UP)


class StandInPaymentProcessor:
    """Placeholder until a processor is connected. Ids start with STANDIN-."""

    name = _STAND_IN_NAME

    def collect(
        self,
        *,
        member_id: UUID,
        tokens: Decimal,
        amount_cad: Decimal,
        payment_id: str | None,
    ) -> PaymentReceipt:
        # The member id is not sent anywhere. There is no account to attach it to.
        del member_id
        charged = _amount_cad(amount_cad)
        chosen = (payment_id or "").strip()
        if not chosen:
            chosen = f"{_STAND_IN_PREFIX}{uuid4().hex[:12].upper()}"
        if not chosen.startswith(_STAND_IN_PREFIX) or len(chosen) > 120:
            raise _http(
                422,
                "standin_only",
                "Enter a payment id that starts with STANDIN-.",
            )
        return PaymentReceipt(
            processor=self.name,
            payment_id=chosen,
            amount_cad=charged,
            tokens=Decimal(tokens),
            fee_rate=STAND_IN_FEE_RATE,
        )


def get_payment_processor() -> PaymentProcessor:
    chosen = get_settings().payment_processor
    if chosen == _STAND_IN_NAME:
        return StandInPaymentProcessor()
    raise _http(
        422,
        "unknown_processor",
        f"No payment processor is registered for {chosen}.",
    )

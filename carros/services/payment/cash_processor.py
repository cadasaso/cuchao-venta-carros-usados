"""Procesador de pago en efectivo."""

import uuid
from decimal import Decimal

from .base import PaymentProcessor, PaymentResult


class CashProcessor(PaymentProcessor):
    """
    Pago en efectivo.
    En este marketplace el pago se acuerda directamente entre las partes;
    el sistema solo registra el compromiso.
    """

    def process(self, amount: Decimal, comprador, carro) -> PaymentResult:
        ref = f"CASH-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=ref,
            message=(
                f"Pago en efectivo registrado. "
                f"Coordina la entrega con el vendedor. Ref: {ref}"
            ),
        )

    def get_display_name(self) -> str:
        return "Efectivo"

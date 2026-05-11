"""Procesador de pago con tarjeta de crédito (simulado)."""

import uuid
from decimal import Decimal

from .base import PaymentProcessor, PaymentResult


class CardProcessor(PaymentProcessor):
    """
    Pago con tarjeta de crédito (simulado).
    En producción aquí iría la integración con Stripe, PayU, etc.
    """

    def process(self, amount: Decimal, comprador, carro) -> PaymentResult:
        ref = f"CARD-{uuid.uuid4().hex[:12].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=ref,
            message=(
                f"Tarjeta de crédito aprobada por ${amount:,.0f}. "
                f"Autorización: {ref}"
            ),
            metadata={
                "autorizacion": ref,
                "monto": str(amount),
                "cuotas": 1,
            },
        )

    def get_display_name(self) -> str:
        return "Tarjeta de Crédito"

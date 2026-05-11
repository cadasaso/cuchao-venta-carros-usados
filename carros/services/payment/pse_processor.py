"""Procesador de pago PSE (simulado)."""

import uuid
from decimal import Decimal

from .base import PaymentProcessor, PaymentResult


class PSEProcessor(PaymentProcessor):
    """
    Transferencia bancaria PSE (simulada).
    En producción aquí iría la integración con la pasarela real.
    """

    def process(self, amount: Decimal, comprador, carro) -> PaymentResult:
        ref = f"PSE-{uuid.uuid4().hex[:12].upper()}"
        return PaymentResult(
            success=True,
            transaction_id=ref,
            message=(
                f"Transferencia PSE aprobada por ${amount:,.0f}. "
                f"Referencia bancaria: {ref}"
            ),
            metadata={
                "banco": "Banco Simulado S.A.",
                "referencia": ref,
                "monto": str(amount),
            },
        )

    def get_display_name(self) -> str:
        return "PSE"

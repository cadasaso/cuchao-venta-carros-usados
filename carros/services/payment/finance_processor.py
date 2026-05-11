"""Procesador de financiamiento (simulado)."""

import uuid
from decimal import Decimal

from .base import PaymentProcessor, PaymentResult


class FinanceProcessor(PaymentProcessor):
    """
    Financiamiento a cuotas (simulado).
    En producción aquí iría la integración con una entidad financiera.
    """

    CUOTAS = 36
    TASA_MENSUAL = Decimal('0.015')  # 1.5 % mensual

    def process(self, amount: Decimal, comprador, carro) -> PaymentResult:
        ref = f"FIN-{uuid.uuid4().hex[:12].upper()}"
        cuota = (
            amount
            * self.TASA_MENSUAL
            / (1 - (1 + self.TASA_MENSUAL) ** -self.CUOTAS)
        ).quantize(Decimal('0.01'))

        return PaymentResult(
            success=True,
            transaction_id=ref,
            message=(
                f"Financiamiento aprobado. {self.CUOTAS} cuotas de "
                f"${cuota:,.0f}/mes. Referencia: {ref}"
            ),
            metadata={
                "referencia": ref,
                "cuotas": self.CUOTAS,
                "cuota_mensual": str(cuota),
                "monto_total": str(amount),
            },
        )

    def get_display_name(self) -> str:
        return "Financiamiento"

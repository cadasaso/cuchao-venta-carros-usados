"""
Interfaz base para procesadores de pago.

Cualquier nuevo método de pago debe heredar de PaymentProcessor
e implementar process(). La vista y el servicio nunca importan
un procesador concreto: solo conocen esta interfaz y la factory.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class PaymentResult:
    """Resultado devuelto por cualquier procesador de pago."""
    success: bool
    transaction_id: str
    message: str
    metadata: dict = field(default_factory=dict)


class PaymentProcessor(ABC):
    """
    Interfaz (contrato) que todo procesador de pago debe implementar.

    Principio de inversión de dependencias:
      - El servicio de alto nivel (VentaService) depende de esta abstracción.
      - Los módulos de bajo nivel (CashProcessor, PSEProcessor, …)
        implementan esta abstracción.
      - Agregar un nuevo método de pago = crear una nueva clase aquí abajo,
        registrarla en la factory. Sin tocar VentaService ni las vistas.
    """

    @abstractmethod
    def process(self, amount: Decimal, comprador, carro) -> PaymentResult:
        """
        Ejecuta el pago y retorna un PaymentResult.

        Args:
            amount:    Monto a cobrar.
            comprador: Instancia del usuario comprador.
            carro:     Instancia del carro que se compra.

        Returns:
            PaymentResult con success=True si el pago fue aprobado.
        """

    @abstractmethod
    def get_display_name(self) -> str:
        """Nombre legible del método de pago (para mensajes y logs)."""

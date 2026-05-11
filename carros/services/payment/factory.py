"""
Factory de procesadores de pago.

Principio Abierto/Cerrado:
  - Para agregar un nuevo método de pago basta con crear una clase
    que herede de PaymentProcessor y registrarla aquí.
  - No hay que modificar VentaService, las vistas ni ningún otro módulo.
"""

from .base import PaymentProcessor
from .cash_processor import CashProcessor
from .pse_processor import PSEProcessor
from .card_processor import CardProcessor
from .finance_processor import FinanceProcessor


class PaymentProcessorFactory:
    """Retorna la instancia del procesador adecuado según el método de pago."""

    _registry: dict[str, type[PaymentProcessor]] = {
        'efectivo':   CashProcessor,
        'pse':        PSEProcessor,
        'tarjeta':    CardProcessor,
        'financiado': FinanceProcessor,
    }

    @classmethod
    def get_processor(cls, metodo_pago: str) -> PaymentProcessor:
        """
        Retorna una instancia del procesador para el método indicado.

        Lanza ValueError si el método no está registrado.
        """
        processor_class = cls._registry.get(metodo_pago)
        if processor_class is None:
            metodos = ', '.join(cls._registry.keys())
            raise ValueError(
                f"Método de pago '{metodo_pago}' no soportado. "
                f"Opciones: {metodos}."
            )
        return processor_class()

    @classmethod
    def metodos_disponibles(cls) -> list[str]:
        """Lista de claves de métodos de pago registrados."""
        return list(cls._registry.keys())

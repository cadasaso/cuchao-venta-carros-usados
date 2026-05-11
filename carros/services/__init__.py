"""
Capa de servicios de Cuchao.

Centraliza la lógica de negocio fuera de las vistas para que sea
fácil de probar, reutilizar y mantener.

Importar desde aquí:
    from carros.services import VentaService, NotificacionService, CatalogoService
"""

from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

from ..models import Carro, Compra, Notificacion
from .payment.factory import PaymentProcessorFactory


# ---------------------------------------------------------------------------
# Servicio de ventas
# ---------------------------------------------------------------------------

class VentaService:
    """Gestiona el proceso de compra de un carro."""

    @staticmethod
    @transaction.atomic
    def procesar_compra(carro_id, comprador, metodo_pago):
        """
        Procesa la compra de un carro de forma atómica.

        Flujo:
          1. Bloquea la fila con select_for_update() (evita compras simultáneas).
          2. Valida reglas de negocio (vendido, propietario, método de pago).
          3. Delega el procesamiento del pago a un PaymentProcessor
             obtenido de PaymentProcessorFactory (inversión de dependencias).
          4. Valida el modelo con full_clean() antes de persistir.
          5. Marca el carro como vendido y dispara las notificaciones.

        Lanza ValueError  si hay un error de negocio o pago rechazado.
        Lanza ValidationError si la instancia de Compra no pasa clean().
        Retorna la Compra creada.
        """
        # 1. Bloqueo de fila
        carro = Carro.objects.select_for_update().get(id=carro_id)

        # 2. Validaciones de negocio
        if carro.propietario == comprador:
            raise ValueError('No puedes comprar tu propio carro.')

        if carro.vendido:
            raise ValueError('Este carro ya ha sido vendido.')

        # 3. Procesar el pago a través de la factory (DIP)
        #    VentaService no sabe si es efectivo, PSE, tarjeta o financiamiento;
        #    solo conoce la interfaz PaymentProcessor.
        processor = PaymentProcessorFactory.get_processor(metodo_pago)
        result = processor.process(carro.precio, comprador, carro)

        if not result.success:
            raise ValueError(f'Pago rechazado: {result.message}')

        # 4. Crear la compra y validar a nivel de modelo (Compra.clean())
        compra = Compra(
            comprador=comprador,
            carro=carro,
            metodo_pago=metodo_pago,
            precio_pagado=carro.precio,
            transaction_id=result.transaction_id,
        )
        compra.full_clean()
        compra.save()

        # 5. Marcar el carro como vendido y notificar
        carro.vendido = True
        carro.save(update_fields=['vendido'])

        NotificacionService.notificar_venta(carro, comprador, result)

        return compra


# ---------------------------------------------------------------------------
# Servicio de notificaciones
# ---------------------------------------------------------------------------

class NotificacionService:
    """Crea notificaciones estándar del sistema."""

    @staticmethod
    def notificar_venta(carro, comprador, payment_result=None):
        """Notifica al vendedor y al comprador tras una compra exitosa."""
        Notificacion.crear(
            carro.propietario, 'venta',
            f'Vendiste tu {carro.modelo}',
            f'{comprador.username} compró tu carro por ${carro.precio:,.0f}.',
            '/dashboard/', ''
        )
        detalle = 'Revisa los detalles en "Mis compras".'
        if payment_result:
            detalle = payment_result.message
        Notificacion.crear(
            comprador, 'compra',
            f'Compra exitosa: {carro.modelo}',
            detalle,
            '/mis-compras/', ''
        )


# ---------------------------------------------------------------------------
# Servicio de catálogo
# ---------------------------------------------------------------------------

class CatalogoService:
    """Aplica filtros y ordenamiento al queryset del catálogo."""

    @staticmethod
    def filtrar_carros(queryset, filtros):
        """
        Recibe un QuerySet base de Carro y un dict de filtros con las
        mismas claves que usa la vista (q, marca, categoria, …).

        Retorna el QuerySet ya filtrado y ordenado.
        """
        q           = filtros.get('q', '').strip()
        marca       = filtros.get('marca', '').strip()
        categoria   = filtros.get('categoria', '').strip()
        transmision = filtros.get('transmision', '').strip()
        combustible = filtros.get('combustible', '').strip()
        precio_min  = filtros.get('precio_min', '').strip()
        precio_max  = filtros.get('precio_max', '').strip()
        anio_min    = filtros.get('anio_min', '').strip()
        etiqueta    = filtros.get('etiqueta', '').strip()
        disponibles = filtros.get('disponibles', '')
        orden       = filtros.get('orden', 'recientes')

        if q:
            queryset = queryset.filter(
                Q(modelo__icontains=q) | Q(marca__icontains=q) |
                Q(descripcion__icontains=q) | Q(ciudad__icontains=q)
            )
        if marca:
            queryset = queryset.filter(marca__icontains=marca)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if transmision:
            queryset = queryset.filter(transmision=transmision)
        if combustible:
            queryset = queryset.filter(combustible=combustible)
        if precio_min.isdigit():
            queryset = queryset.filter(precio__gte=int(precio_min))
        if precio_max.isdigit():
            queryset = queryset.filter(precio__lte=int(precio_max))
        if anio_min.isdigit():
            queryset = queryset.filter(anio__gte=int(anio_min))
        if etiqueta.isdigit():
            queryset = queryset.filter(etiquetas__id=int(etiqueta))
        if disponibles == '1':
            queryset = queryset.filter(vendido=False)

        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'populares':
            queryset = queryset.order_by('-vistas')
        else:
            queryset = queryset.order_by('-fecha_publicacion')

        return queryset

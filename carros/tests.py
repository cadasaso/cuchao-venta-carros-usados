"""
Tests de Cuchao.

Ejecutar con:
    docker compose exec web python manage.py test carros
"""

from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Carro, Compra, Usuario
from .services import VentaService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _crear_usuario(username, password='pass1234'):
    return Usuario.objects.create_user(username=username, password=password)


def _crear_carro(propietario, marca='Toyota', modelo='Corolla', precio=20_000_000):
    return Carro.objects.create(
        propietario=propietario,
        marca=marca,
        modelo=modelo,
        anio=2020,
        precio=precio,
        kilometraje=30000,
        ciudad='Bogota',
        categoria='sedan',
        transmision='automatica',
        combustible='gasolina',
    )


# ---------------------------------------------------------------------------
# Tests de VentaService
# ---------------------------------------------------------------------------

class VentaServiceTests(TestCase):
    """Pruebas unitarias de la lógica de negocio en VentaService."""

    def setUp(self):
        self.vendedor = _crear_usuario('vendedor')
        self.comprador = _crear_usuario('comprador')
        self.carro = _crear_carro(self.vendedor)

    # ------------------------------------------------------------------
    # Test 1: una compra exitosa marca el carro como vendido
    # ------------------------------------------------------------------
    def test_compra_marca_carro_como_vendido(self):
        """Tras procesar_compra, el carro debe quedar con vendido=True."""
        compra = VentaService.procesar_compra(self.carro.id, self.comprador, 'efectivo')

        self.carro.refresh_from_db()
        self.assertTrue(self.carro.vendido, 'El carro debería estar marcado como vendido.')
        self.assertEqual(compra.comprador, self.comprador)
        self.assertEqual(compra.precio_pagado, self.carro.precio)
        self.assertEqual(Compra.objects.filter(carro=self.carro).count(), 1)

    # ------------------------------------------------------------------
    # Test 2: no se puede volver a comprar un carro ya vendido
    # ------------------------------------------------------------------
    def test_no_permite_comprar_carro_vendido(self):
        """Un carro ya vendido no puede comprarse de nuevo."""
        VentaService.procesar_compra(self.carro.id, self.comprador, 'efectivo')

        comprador2 = _crear_usuario('comprador2')
        with self.assertRaises(ValueError) as ctx:
            VentaService.procesar_compra(self.carro.id, comprador2, 'efectivo')

        self.assertIn('ya ha sido vendido', str(ctx.exception))
        # Solo debe existir una compra
        self.assertEqual(Compra.objects.filter(carro=self.carro).count(), 1)

    # ------------------------------------------------------------------
    # Test 3: el propietario no puede comprar su propio carro
    # ------------------------------------------------------------------
    def test_propietario_no_puede_comprar_su_carro(self):
        """El dueño del carro no puede comprárselo a sí mismo."""
        with self.assertRaises(ValueError) as ctx:
            VentaService.procesar_compra(self.carro.id, self.vendedor, 'efectivo')

        self.assertIn('tu propio carro', str(ctx.exception))
        self.carro.refresh_from_db()
        self.assertFalse(self.carro.vendido, 'El carro no debería marcarse como vendido.')


# ---------------------------------------------------------------------------
# Tests del modelo Compra
# ---------------------------------------------------------------------------

class CompraModelTests(TestCase):
    """Pruebas de la validación a nivel de modelo en Compra."""

    def setUp(self):
        self.vendedor = _crear_usuario('model_vendedor')
        self.comprador = _crear_usuario('model_comprador')
        self.carro = _crear_carro(self.vendedor)

    def test_clean_rechaza_propietario_como_comprador(self):
        """Compra.clean() debe lanzar ValidationError si comprador == propietario."""
        compra = Compra(
            comprador=self.vendedor,   # el dueño intenta comprarse su propio carro
            carro=self.carro,
            metodo_pago='efectivo',
            precio_pagado=self.carro.precio,
        )
        with self.assertRaises(ValidationError) as ctx:
            compra.full_clean()
        self.assertIn('propio carro', str(ctx.exception))

    def test_clean_permite_compra_valida(self):
        """Compra.clean() no lanza error si comprador != propietario."""
        compra = Compra(
            comprador=self.comprador,
            carro=self.carro,
            metodo_pago='efectivo',
            precio_pagado=self.carro.precio,
        )
        # No debe lanzar ninguna excepción
        compra.full_clean()


# ---------------------------------------------------------------------------
# Tests de vistas (integración)
# ---------------------------------------------------------------------------

class CompraVistaTests(TestCase):
    """Pruebas de integración sobre los endpoints HTTP de compra."""

    def setUp(self):
        self.client = Client()
        self.vendedor = _crear_usuario('v_usuario')
        self.comprador = _crear_usuario('c_usuario')
        self.carro = _crear_carro(self.vendedor)

    def test_vista_confirmar_compra_requiere_login(self):
        """confirmar_compra redirige al login si el usuario no está autenticado."""
        url = reverse('confirmar_compra', kwargs={'carro_id': self.carro.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp['Location'])

    def test_propietario_redirigido_en_confirmar_compra(self):
        """El propietario no puede ver la página de confirmación de su propio carro."""
        self.client.login(username='v_usuario', password='pass1234')
        url = reverse('confirmar_compra', kwargs={'carro_id': self.carro.id})
        resp = self.client.get(url)
        # Debe redirigir (no mostrar el formulario)
        self.assertEqual(resp.status_code, 302)

    def test_compra_exitosa_via_post(self):
        """POST a procesar_compra completa la compra y redirige a compra_exitosa."""
        self.client.login(username='c_usuario', password='pass1234')
        url = reverse('procesar_compra', kwargs={'carro_id': self.carro.id})
        resp = self.client.post(url, {'metodo_pago': 'efectivo'})
        self.assertEqual(resp.status_code, 302)
        self.assertIn('exitosa', resp['Location'])

        self.carro.refresh_from_db()
        self.assertTrue(self.carro.vendido)


# ---------------------------------------------------------------------------
# Tests de validación del modelo Carro
# ---------------------------------------------------------------------------

class CarroPrecioTests(TestCase):
    """Pruebas de la validación del campo precio en Carro."""

    def setUp(self):
        self.vendedor = _crear_usuario('precio_vendedor')

    def _carro_con_precio(self, precio):
        """Crea un Carro en memoria (sin guardar) con el precio dado."""
        return Carro(
            propietario=self.vendedor,
            marca='Toyota',
            modelo='Corolla',
            anio=2020,
            precio=precio,
            kilometraje=10000,
            ciudad='Bogotá',
            categoria='sedan',
            transmision='automatica',
            combustible='gasolina',
        )

    # ------------------------------------------------------------------
    # Test 4 (rúbrica): precio no puede ser negativo
    # ------------------------------------------------------------------
    def test_precio_no_puede_ser_negativo(self):
        """Un precio negativo debe fallar la validación del modelo."""
        carro = self._carro_con_precio(Decimal('-1.00'))
        with self.assertRaises(ValidationError) as ctx:
            carro.full_clean()
        # El validador MinValueValidator(0.01) debe estar en el mensaje
        errores = str(ctx.exception)
        self.assertTrue(
            'precio' in errores.lower() or 'ensure this value' in errores.lower(),
            f"Se esperaba un error en 'precio', se obtuvo: {errores}"
        )

    def test_precio_cero_no_permitido(self):
        """Un precio de 0 también debe fallar (MinValueValidator(0.01))."""
        carro = self._carro_con_precio(Decimal('0.00'))
        with self.assertRaises(ValidationError):
            carro.full_clean()

    def test_precio_positivo_valido(self):
        """Un precio positivo debe pasar la validación sin errores."""
        carro = self._carro_con_precio(Decimal('1500000.00'))
        # No debe lanzar ninguna excepción
        carro.full_clean()

    def test_precio_minimo_valido(self):
        """El valor mínimo permitido es 0.01."""
        carro = self._carro_con_precio(Decimal('0.01'))
        carro.full_clean()  # No debe lanzar

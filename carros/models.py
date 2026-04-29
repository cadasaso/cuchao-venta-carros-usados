from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Avg


class Usuario(AbstractUser):
    """Usuario extendido con perfil de comprador/vendedor."""
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True, max_length=400)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    verificado = models.BooleanField(default=False, help_text="Vendedor verificado por Cuchao")
    tema_oscuro = models.BooleanField(default=False)

    @property
    def calificacion_promedio(self):
        prom = self.resenas_recibidas.aggregate(p=Avg('calificacion'))['p']
        return round(prom, 1) if prom else 0

    @property
    def total_ventas(self):
        return Compra.objects.filter(carro__propietario=self).count()

    @property
    def total_resenas(self):
        return self.resenas_recibidas.count()

    @property
    def nivel_vendedor(self):
        """Nivel basado en ventas: Bronce/Plata/Oro/Diamante."""
        ventas = self.total_ventas
        if ventas >= 20:
            return ('Diamante', '')
        if ventas >= 10:
            return ('Oro', '')
        if ventas >= 5:
            return ('Plata', '')
        if ventas >= 1:
            return ('Bronce', '')
        return ('Nuevo', '')


class Etiqueta(models.Model):
    """Tags reutilizables para los carros (Económico, Familiar, Off-road, etc.)."""
    nombre = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=20, default='#6366f1')
    icono = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return self.nombre


class Carro(models.Model):
    TRANSMISIONES = [
        ('manual', 'Manual'),
        ('automatica', 'Automática'),
    ]
    COMBUSTIBLES = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('hibrido', 'Híbrido'),
        ('electrico', 'Eléctrico'),
        ('gas', 'Gas'),
    ]
    CATEGORIAS = [
        ('sedan', 'Sedán'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('pickup', 'Pickup'),
        ('coupe', 'Coupé'),
        ('convertible', 'Convertible'),
        ('van', 'Van'),
        ('deportivo', 'Deportivo'),
    ]
    ESTADOS = [
        ('excelente', 'Excelente'),
        ('muy_bueno', 'Muy bueno'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
    ]

    propietario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True, blank=True
    )
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=80, blank=True)
    anio = models.PositiveIntegerField(null=True, blank=True)
    kilometraje = models.PositiveIntegerField(null=True, blank=True, help_text="km")
    color = models.CharField(max_length=40, blank=True)
    transmision = models.CharField(max_length=20, choices=TRANSMISIONES, blank=True)
    combustible = models.CharField(max_length=20, choices=COMBUSTIBLES, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, blank=True)
    ciudad = models.CharField(max_length=80, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='carros/', blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    precio_negociable = models.BooleanField(default=True, help_text="Permite recibir ofertas")
    vendido = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    vistas = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='carros')

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.modelo

    def esta_disponible(self):
        return not self.vendido

    @property
    def total_favoritos(self):
        return self.favoritos.count()

    @property
    def total_ofertas(self):
        return self.ofertas.filter(estado='pendiente').count()


class CarroImagen(models.Model):
    """Imágenes adicionales (galería) por carro."""
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='carros/galeria/')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos_set')
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='favoritos')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'carro')
        ordering = ['-fecha']


class Resena(models.Model):
    """Reseñas/calificaciones a vendedores."""
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='resenas_dadas')
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='resenas_recibidas')
    calificacion = models.PositiveSmallIntegerField(default=5)
    comentario = models.TextField(blank=True, max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        unique_together = ('autor', 'vendedor')


class Mensaje(models.Model):
    """Mensajería simple comprador-vendedor."""
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    carro = models.ForeignKey(Carro, on_delete=models.SET_NULL, null=True, blank=True, related_name='mensajes')
    contenido = models.TextField(max_length=1000)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']


class Compra(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('pse', 'PSE (Simulado)'),
        ('tarjeta', 'Tarjeta de Crédito (Simulado)'),
        ('financiado', 'Financiamiento (Simulado)'),
    ]

    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='ventas')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    precio_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_compra']

    def __str__(self):
        return f"Compra de {self.comprador.username} - {self.carro.modelo}"


# ====== NUEVOS MODELOS ======

class Oferta(models.Model):
    """Ofertas/contraofertas que los compradores hacen a los vendedores."""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('contraoferta', 'Contraoferta'),
        ('expirada', 'Expirada'),
    ]
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='ofertas')
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ofertas_hechas')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    mensaje = models.TextField(max_length=500, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    contraoferta_monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Oferta {self.monto} por {self.carro.modelo}"

    @property
    def porcentaje_descuento(self):
        if not self.carro.precio:
            return 0
        return round(100 - (float(self.monto) / float(self.carro.precio) * 100), 1)


class Notificacion(models.Model):
    """Sistema de notificaciones internas para usuarios."""
    TIPOS = [
        ('mensaje', 'Mensaje recibido'),
        ('oferta', 'Nueva oferta'),
        ('oferta_resp', 'Respuesta a oferta'),
        ('venta', 'Carro vendido'),
        ('compra', 'Compra realizada'),
        ('favorito', 'Te marcaron favorito'),
        ('resena', 'Nueva reseña'),
        ('sistema', 'Sistema'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='sistema')
    titulo = models.CharField(max_length=140)
    mensaje = models.CharField(max_length=300, blank=True)
    url = models.CharField(max_length=300, blank=True)
    icono = models.CharField(max_length=10, default='')
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    @classmethod
    def crear(cls, usuario, tipo, titulo, mensaje='', url='', icono=''):
        if not usuario:
            return None
        return cls.objects.create(
            usuario=usuario, tipo=tipo, titulo=titulo,
            mensaje=mensaje, url=url, icono=icono
        )


class HistorialVista(models.Model):
    """Carros vistos recientemente por usuario (para 'Continuar viendo')."""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial')
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='historial_vistas')
    fecha = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'carro')
        ordering = ['-fecha']

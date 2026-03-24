from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    pass

class Carro(models.Model):
    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='carros/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    vendido = models.BooleanField(default=False)

    def __str__(self):
        return self.modelo
    
    def esta_disponible(self):
        """Retorna True si el carro no está vendido"""
        return not self.vendido


class Compra(models.Model):
    """Modelo para guardar el historial de compras simuladas"""
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('pse', 'PSE (Simulado)'),
    ]
    
    comprador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='compras'
    )
    carro = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO,
        default='efectivo'
    )
    precio_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    fecha_compra = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_compra']
    
    def __str__(self):
        return f"Compra de {self.comprador.username} - {self.carro.modelo} ({self.fecha_compra.strftime('%d/%m/%Y')})"
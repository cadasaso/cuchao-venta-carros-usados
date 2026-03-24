from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return self.modelo
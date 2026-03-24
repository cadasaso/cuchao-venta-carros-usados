from django.contrib import admin
from .models import Usuario, Carro, Compra

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']

class CarroAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'propietario', 'precio', 'vendido']
    list_filter = ['precio', 'vendido']
    search_fields = ['modelo']
    readonly_fields = ['vendido']  # Campo de solo lectura (se controla desde la venta)

class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'comprador', 'carro', 'metodo_pago', 'precio_pagado', 'fecha_compra']
    list_filter = ['metodo_pago', 'fecha_compra']
    search_fields = ['comprador__username', 'carro__modelo']
    readonly_fields = ['fecha_compra']  # Solo lectura, se asigna automáticamente

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Carro, CarroAdmin)
admin.site.register(Compra, CompraAdmin)

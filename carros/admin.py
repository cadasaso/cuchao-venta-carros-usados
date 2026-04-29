from django.contrib import admin
from .models import (
    Usuario, Carro, Compra, Favorito, Resena, Mensaje, CarroImagen,
    Oferta, Notificacion, HistorialVista, Etiqueta
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'ciudad', 'verificado', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'verificado', 'ciudad']
    list_editable = ['verificado']
    search_fields = ['username', 'email']


class CarroImagenInline(admin.TabularInline):
    model = CarroImagen
    extra = 1


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'marca', 'anio', 'propietario', 'precio', 'vendido', 'destacado', 'vistas']
    list_filter = ['vendido', 'destacado', 'categoria', 'transmision', 'combustible']
    search_fields = ['modelo', 'marca', 'descripcion']
    list_editable = ['destacado']
    readonly_fields = ['vistas', 'fecha_publicacion']
    filter_horizontal = ['etiquetas']
    inlines = [CarroImagenInline]


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'comprador', 'carro', 'metodo_pago', 'precio_pagado', 'fecha_compra']
    list_filter = ['metodo_pago', 'fecha_compra']
    search_fields = ['comprador__username', 'carro__modelo']
    readonly_fields = ['fecha_compra']


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'carro', 'fecha']


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['autor', 'vendedor', 'calificacion', 'fecha']
    list_filter = ['calificacion']


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['remitente', 'destinatario', 'carro', 'leido', 'fecha']
    list_filter = ['leido']


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['carro', 'comprador', 'monto', 'estado', 'fecha']
    list_filter = ['estado', 'fecha']
    search_fields = ['carro__modelo', 'comprador__username']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'titulo', 'leida', 'fecha']
    list_filter = ['tipo', 'leida']


@admin.register(HistorialVista)
class HistorialVistaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'carro', 'fecha']


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'color']

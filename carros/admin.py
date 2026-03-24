from django.contrib import admin
from .models import Usuario, Carro

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']

class CarroAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'propietario', 'precio']
    list_filter = ['precio']
    search_fields = ['modelo']

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Carro, CarroAdmin)

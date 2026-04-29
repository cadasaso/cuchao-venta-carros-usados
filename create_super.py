#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuchao.settings')
django.setup()

from carros.models import Usuario

# Crear superusuario si no existe
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin',
        email='admin@ejemplo.com',
        password='admin123'
    )
    print("[OK] Superusuario 'admin' creado exitosamente")
else:
    print("[WARNING] El usuario 'admin' ya existe")

# Cuchao - Gestión de Carros

Aplicación Django para la gestión y catalogación de carros con autenticación de usuarios.

## Requisitos Previos

### Opción 1: Con Docker (Recomendado)
- Docker Engine
- Docker Compose

### Opción 2: Sin Docker
- Python 3.12+
- PostgreSQL 15+
- pip (gestor de paquetes de Python)

---

## Instalación y Ejecución

### Opción 1: Con Docker Compose (Recomendado)

1. **Navega a la carpeta del proyecto:**
   ```bash
   cd cuchao
   ```

2. **Inicia los servicios con Docker Compose:**
   ```bash
   docker compose up
   ```

   Esto creará e iniciará automáticamente:
   - Base de datos PostgreSQL (puerto 5432)
   - Servidor Django (puerto 8000)

3. **En otra terminal, ejecuta las migraciones:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

4. **Crea un superusuario (administrador):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   Sigue las indicaciones para crear tu usuario.

5. **Accede a la aplicación:**
   - Aplicación: http://localhost:8000
   - Panel de administración: http://localhost:8000/admin

6. **Para detener los servicios:**
   ```bash
   docker compose down
   ```

---

### Opción 2: Sin Docker (Desarrollo Local)

1. **Navega a la carpeta del proyecto:**
   ```bash
   cd cuchao
   ```

2. **Crea un entorno virtual:**
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   
   Asegúrate de que PostgreSQL está corriendo en tu sistema. Por defecto, la aplicación espera:
   - Host: localhost
   - Usuario: cuchao_user
   - Contraseña: Cuchao123
   - Base de datos: cuchao_db

   O modifica las credenciales en `cuchao/settings.py` en la sección `DATABASES`.

5. **Ejecuta las migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Crea un superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicia el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

8. **Accede a la aplicación:**
   - Aplicación: http://localhost:8000
   - Panel de administración: http://localhost:8000/admin

---

## Estructura del Proyecto

```
cuchao/
├── carros/                    # Aplicación principal de Django
│   ├── migrations/           # Migraciones de base de datos
│   ├── templates/            # Archivos HTML
│   ├── static/               # Archivos CSS y otros estáticos
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas
│   ├── forms.py             # Formularios
│   ├── urls.py              # Rutas
│   └── admin.py             # Configuración del panel admin
├── cuchao/                   # Configuración del proyecto Django
│   ├── settings.py          # Configuraciones principales
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # WSGI para producción
│   └── asgi.py              # ASGI para producción
├── templates/                # Archivos HTML globales
├── media/                    # Archivos de medios subidos
├── Dockerfile               # Configuración para Docker
├── docker-compose.yml       # Orquestación de servicios
├── manage.py                # Herramienta de gestión de Django
├── requirements.txt         # Dependencias de Python
└── README.md               # Este archivo
```

---

## Comandos Útiles

### Con Docker Compose

```bash
# Ver logs del contenedor web
docker compose logs -f web

# Ver logs de la base de datos
docker compose logs -f db

# Ejecutar shell interactivo de Django
docker compose exec web python manage.py shell

# Crear nuevas migraciones
docker compose exec web python manage.py makemigrations

# Aplicar migraciones
docker compose exec web python manage.py migrate

# Detener sin eliminar volúmenes
docker compose stop

# Reiniciar servicios
docker compose restart

# Eliminar todo (bases de datos incluidas)
docker compose down -v
```

### Sin Docker

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

---

## Credenciales por Defecto (Docker)

- **Base de datos PostgreSQL:**
  - Usuario: `cuchao_user`
  - Contraseña: `Cuchao123`
  - Base de datos: `cuchao_db`

## Solución de Problemas

### Puerto 8000 ya está en uso
```bash
# Cambiar el puerto en docker-compose.yml o ejecutar:
docker compose up -p 8001:8000
```

### Errores de conexión a base de datos
```bash
# Verificar que la base de datos está lista:
docker compose ps

# Reiniciar los servicios:
docker compose restart
```

### Migraciones no aplicadas
```bash
docker compose exec web python manage.py migrate
```

---

## Tecnologías Utilizadas

- **Django 5.2.4** - Framework web
- **PostgreSQL 15** - Base de datos
- **Python 3.12** - Lenguaje de programación
- **Docker** - Contenedorización
- **Pillow** - Procesamiento de imágenes

---

## Licencia

Este proyecto está bajo licencia MIT.

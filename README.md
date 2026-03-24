# Cuchao - Gestión de Carros

<div align="center">

**Plataforma web moderna para la gestión de catálogo de vehículos**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django 5.2](https://img.shields.io/badge/Django-5.2-darkgreen.svg)](https://www.djangoproject.com/)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

</div>

---

## Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Comandos Útiles](#comandos-útiles)
- [Solución de Problemas](#solución-de-problemas)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Licencia](#licencia)

---

## Características

- Autenticación y registro de usuarios
- Catálogo de vehículos con búsqueda
- Gestión completa de carros (crear, editar, eliminar)
- Carga y visualización de imágenes
- Panel de administración de Django
- Base de datos PostgreSQL
- Dockerizado para fácil despliegue
- Interfaz responsiva

---

## Requisitos Previos

### Opción 1: Con Docker (Recomendado)
- Docker Engine
- Docker Compose

### Opción 2: Sin Docker
- Python 3.12+
- PostgreSQL 15+
- pip (gestor de paquetes de Python)

---

## Inicio Rápido

La forma más fácil de empezar es con Docker:

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/cuchao.git
cd cuchao

# Iniciar con Docker
docker compose up

# En otra terminal, ejecutar migraciones
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

# Acceder a la aplicación
# - Web: http://localhost:8000
# - Admin: http://localhost:8000/admin
```

---

## Instalación y Ejecución

### Opción 1: Con Docker Compose (Recomendado)

**Requisitos:** Docker Engine y Docker Compose instalados

1. **Inicia los servicios:**
   ```bash
   docker compose up
   ```
   
   Se crearán automáticamente:
   - Contenedor PostgreSQL en puerto 5432
   - Servidor Django en puerto 8000

2. **En otra terminal, ejecuta migraciones:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

3. **Crea tu superusuario (administrador):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

4. **Accede a tu aplicación:**
   - Sitio web: http://localhost:8000
   - Panel admin: http://localhost:8000/admin

5. **Detener los servicios:**
   ```bash
   docker compose down
   ```
   
   Los datos se preservan automáticamente. Para limpiar completamente:
   ```bash
   docker compose down -v
   ```

---

### Opción 2: Sin Docker (Desarrollo Local)

**Requisitos:** Python 3.12+, PostgreSQL 16 instalados localmente

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/cuchao.git
   cd cuchao
   ```

2. **Crea un entorno virtual:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura PostgreSQL:**
   
   Asegúrate que PostgreSQL esté corriendo. Por defecto la app espera:
   - **Host:** localhost
   - **Usuario:** cuchao_user
   - **Contraseña:** Cuchao123
   - **Base de datos:** cuchao_db
   
   O modifica `cuchao/settings.py` en la sección `DATABASES`.

5. **Ejecuta las migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Crea tu superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

8. **Accede en tu navegador:**
   - Sitio web: http://localhost:8000
   - Panel admin: http://localhost:8000/admin

---

## Estructura del Proyecto

```
cuchao/
├── carros/                    # Aplicación principal de Django
│   ├── migrations/           # Migraciones de base de datos
│   ├── static/               # Archivos CSS
│   ├── models.py            # Modelos de datos (Usuario, Carro)
│   ├── views.py             # Vistas de la aplicación
│   ├── forms.py             # Formularios (UsuarioCreationForm, CarroForm)
│   ├── urls.py              # Rutas de carros
│   └── admin.py             # Configuración del panel admin
│
├── cuchao/                   # Configuración del proyecto Django
│   ├── settings.py          # Configuraciones principales
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # WSGI para producción
│   └── asgi.py              # ASGI para producción
│
├── templates/                # Archivos HTML
│   ├── base.html            # Template base
│   ├── agregar_carro.html
│   ├── editar_carro.html
│   ├── catalogo.html
│   ├── login.html
│   └── register.html
│
├── static/                    # Archivos estáticos globales
├── media/                     # Archivos de medios subidos por usuarios
│
├── Dockerfile               # Configuración para Docker
├── docker-compose.yml       # Orquestación de servicios (PostgreSQL + Django)
├── manage.py                # Herramienta de gestión de Django
├── requirements.txt         # Dependencias de Python
└── README.md               # Este archivo
```

---

## Comandos Útiles

### Con Docker Compose

```bash
# Iniciar servicios
docker compose up

# Iniciar en background
docker compose up -d

# Detener sin eliminar datos
docker compose down

# Ver logs en tiempo real
docker compose logs -f web

# Ejecutar comando en contenedor web
docker compose exec web python manage.py <comando>

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Aplicar migraciones
docker compose exec web python manage.py migrate

# Shell interactivo de Django
docker compose exec web python manage.py shell

# Acceder a PostgreSQL
docker compose exec db psql -U cuchao_user -d cuchao_db
```

### Sin Docker (Local)

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Runserver
python manage.py runserver

# Shell interactivo
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

---

## Configuración Predeterminada (Docker)

**Base de datos PostgreSQL:**
```
Usuario: cuchao_user
Contraseña: Cuchao123
Base de datos: cuchao_db
Puerto: 5432
```

**Importante:** Cambia estas credenciales en producción. Ver `cuchao/settings.py` para variables de entorno.

## Solución de Problemas

### Puerto 8000 ya está en uso

**Solution:** Cambia el puerto en docker-compose.yml o usa:

```bash
docker compose up -p 8001:8000
```

Luego accede a http://localhost:8001

### Errores de conexión a la base de datos

```bash
# Verifica el estatus de los contenedores
docker compose ps

# Reinicia los servicios
docker compose restart

# Ver logs detallados
docker compose logs -f web
docker compose logs -f db
```

### Las migraciones no se aplican

```bash
# Manualmente
docker compose exec web python manage.py migrate

# En desarrollo local
python manage.py migrate
```

### Error: "base de datos cuchao_user no existe"

Este error ocurre cuando PostgreSQL intenta conectarse sin especificar la BD.

**Solución:** Verifica el `docker-compose.yml` y que `DB_NAME=cuchao_db` esté configurado.

---

## Tecnologías Utilizadas

- **Django 5.2.4** - Framework web Python
- **PostgreSQL 16** - Base de datos relacional
- **Python 3.12** - Lenguaje de programación
- **Docker & Docker Compose** - Contenedorización
- **Pillow** - Procesamiento de imágenes
- **HTML5 & CSS3** - Frontend

---

## Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Autor

**Cuchao Team**

---

## Soporte

Si encuentras algún problema o tienes preguntas, abre un issue en el repositorio.

---

## Licencia

Este proyecto está bajo licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

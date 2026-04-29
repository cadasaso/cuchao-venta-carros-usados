# Cuchao — Marketplace de Carros Usados

<div align="center">

**Plataforma web para comprar y vender carros usados directamente entre personas**

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-darkgreen.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

</div>

---

## Características

- Catálogo de carros con búsqueda en vivo y filtros avanzados
- Publicación de carros con foto, descripción y precio
- **Generador de descripciones con IA** (Cohere) — genera título, descripción, ventajas y texto de venta automáticamente
- **Chat en tiempo real** entre comprador y vendedor por carro
- Sistema de ofertas y negociación de precios
- Favoritos, comparador de hasta 4 carros, historial de visitas
- Notificaciones en tiempo real (campana en el navbar)
- Perfiles públicos de vendedores con reseñas y calificaciones
- Modo oscuro / modo claro con persistencia
- Panel de dashboard para vendedores
- Panel de administración Django (`/admin/`)

---

## Requisitos previos

- [Docker](https://www.docker.com/get-started) y Docker Compose
- Cuenta gratuita en [Cohere](https://dashboard.cohere.com/) para obtener la API key (necesaria para el generador de descripciones con IA)

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/cadasaso/cuchao-venta-carros-usados.git
cd cuchao-venta-carros-usados
```

### 2. Crear el archivo `.env`

En la raíz del proyecto (junto a `docker-compose.yml`) crea un archivo llamado `.env`:

```
COHERE_API_KEY=tu-api-key-de-cohere-aqui
```

Para obtener la key gratuitamente:
1. Ve a [dashboard.cohere.com](https://dashboard.cohere.com/)
2. Crea una cuenta (no requiere tarjeta de crédito)
3. En **API Keys** copia la key que aparece por defecto

> El generador de IA funciona con la cuenta gratuita. Si no quieres usar esta función, puedes dejar el valor vacío (`COHERE_API_KEY=`) y el resto de la aplicación funcionará normalmente.

### 3. Levantar la aplicación

```bash
docker compose up --build
```

Las migraciones de base de datos se ejecutan automáticamente al iniciar.

### 4. Abrir en el navegador

- **Aplicación:** http://localhost:8000
- **Panel de administración:** http://localhost:8000/admin

### 5. Crear un superusuario (opcional, para acceder al admin)

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Detener la aplicación

```bash
# Detener sin borrar datos
docker compose down

# Detener y borrar todos los datos (base de datos incluida)
docker compose down -v
```

---

## Comandos útiles

```bash
# Ver logs en tiempo real
docker compose logs -f web

# Reiniciar solo el servidor web
docker compose restart web

# Acceder a la consola de Django
docker compose exec web python manage.py shell

# Acceder a la base de datos PostgreSQL
docker compose exec db psql -U cuchao_user -d cuchao_db
```

---

## Estructura del proyecto

```
cuchao/
├── carros/                   # Aplicación principal
│   ├── migrations/           # Migraciones de base de datos
│   ├── static/carros/        # CSS global (styles.css)
│   ├── models.py             # Modelos: Usuario, Carro, Mensaje, Oferta, etc.
│   ├── views.py              # Vistas y endpoints de la API interna
│   ├── forms.py              # Formularios
│   ├── urls.py               # Rutas
│   ├── admin.py              # Configuración del panel admin
│   └── context_processors.py # Variables globales de contexto
│
├── cuchao/                   # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
│
├── templates/                # Plantillas HTML
│   ├── base.html             # Base con navbar, footer, notificaciones
│   ├── catalogo.html         # Catálogo principal con filtros
│   ├── detalle_carro.html    # Página de detalle del carro
│   ├── chat.html             # Chat en tiempo real
│   ├── mensajes.html         # Bandeja de conversaciones
│   ├── dashboard.html        # Panel del vendedor
│   ├── agregar_carro.html    # Formulario con generador IA
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                      # No se sube al repo (contiene la API key)
```

---

## Variables de entorno

| Variable | Descripción | Requerida |
|---|---|---|
| `COHERE_API_KEY` | API key de Cohere para el generador de descripciones con IA | No (la función simplemente no estará disponible) |

Las credenciales de la base de datos ya vienen configuradas en `docker-compose.yml` para el entorno de desarrollo.

---

## Tecnologías

- **Django 5.2** — framework web
- **PostgreSQL 16** — base de datos
- **Docker & Docker Compose** — contenedorización
- **Cohere (command-a-03-2025)** — generación de texto con IA
- **Pillow** — procesamiento de imágenes
- **HTML5 / CSS3 / JavaScript** — frontend sin frameworks externos

---

## Solución de problemas

**El puerto 8000 ya está en uso:**
```bash
# Cambia el puerto en docker-compose.yml: "8001:8000"
# Luego accede a http://localhost:8001
```

**Error de conexión a la base de datos al iniciar:**
```bash
docker compose logs -f db   # Ver si PostgreSQL terminó de iniciar
docker compose restart web  # Reiniciar el servidor web
```

**Los cambios en el código no se reflejan:**
```bash
docker compose restart web
# Si es CSS, haz Ctrl+Shift+R en el navegador para limpiar caché
```

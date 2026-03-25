# CUCHAO - Plataforma de compra y venta de carros usados

<div align="center">

Aplicación web desarrollada con **Django**, **PostgreSQL** y **Docker** para la gestión de un catálogo de carros usados, con autenticación de usuarios, administración de publicaciones y compra simulada.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)

</div>

---

## Descripción del proyecto

**CUCHAO** es una aplicación web orientada a la compra y venta de carros usados. El sistema permite que los usuarios se registren, inicien sesión, publiquen vehículos, editen o eliminen sus publicaciones y realicen compras simuladas de carros disponibles.

El proyecto fue desarrollado siguiendo la arquitectura **MVT (Model - View - Template)** de Django, utilizando **PostgreSQL** como motor de base de datos y **Docker** para facilitar su ejecución.

---

## Objetivo

Construir una plataforma web que separe claramente la experiencia del **usuario final** y la del **administrador**, permitiendo la gestión de vehículos usados y simulando el flujo de compra dentro del sistema.

---

## Funcionalidades implementadas

### Funcionalidades principales
- Registro de usuarios
- Inicio y cierre de sesión
- Catálogo público de carros
- Publicación de carros por usuarios autenticados
- Edición de carros por su propietario
- Eliminación de carros por su propietario
- Visualización del estado del vehículo: disponible o vendido
- Panel de administración con Django Admin

### Funcionalidades interesantes implementadas
- **Compra simulada de carros** con selección de método de pago
- **Registro de compras** en base de datos mediante el modelo `Compra`
- **Marcado automático de carros vendidos** después de una compra exitosa
- **Control de permisos** para que solo el propietario pueda editar o eliminar sus publicaciones

> Nota: en el código actual sí está implementado el flujo de compra simulada. No se encontró una funcionalidad de búsqueda activa en las vistas o rutas actuales, por lo que no se incluye como funcionalidad terminada.

---

## Arquitectura del proyecto

El proyecto sigue la arquitectura **MVT**:

- **Modelos:** definen la estructura de datos del sistema
- **Vistas:** procesan la lógica de negocio
- **Templates:** renderizan la interfaz HTML al usuario

### Modelos principales
- **Usuario**: modelo personalizado basado en `AbstractUser`
- **Carro**: almacena la información del vehículo publicado
- **Compra**: guarda el historial de compras simuladas

### Secciones del sistema
- **Sección usuario final:** catálogo, registro, login, publicación y compra
- **Sección administrador:** gestión desde `/admin/`

---

## Tecnologías utilizadas

- **Python 3.12**
- **Django 5.2.4**
- **PostgreSQL 16**
- **Docker / Docker Compose**
- **Pillow**
- **HTML5 / CSS3**

---

## Estructura del proyecto

```text
cuchao-venta-carros-usados-main/
├── carros/                     # App principal
│   ├── migrations/             # Migraciones de base de datos
│   ├── admin.py                # Configuración de panel admin
│   ├── forms.py                # Formularios del sistema
│   ├── models.py               # Modelos Usuario, Carro y Compra
│   ├── urls.py                 # Rutas de la app
│   └── views.py                # Lógica principal
├── cuchao/                     # Configuración del proyecto Django
├── templates/                  # Interfaces HTML
├── media/                      # Imágenes subidas por usuarios
├── docs/                       # Documentación técnica adicional
├── wiki/                       # Contenido base para la Wiki de GitHub
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## Rutas principales

- **Ruta principal del sistema:** `http://localhost:8000/`
- **Panel de administración:** `http://localhost:8000/admin/`
- **Registro:** `http://localhost:8000/register/`
- **Login:** `http://localhost:8000/login/`

---

## Requisitos previos

Para ejecutar el proyecto necesitas tener instalado:

- **Docker** y **Docker Compose**

Si deseas correrlo sin Docker, necesitas además:
- **Python 3.12**
- **PostgreSQL**
- **pip**
- un entorno virtual recomendado

---

## Ejecución del proyecto

### Opción recomendada: con Docker

1. Clona el repositorio:

```bash
git clone https://github.com/cadasaso/cuchao-venta-carros-usados.git
cd cuchao-venta-carros-usados
```

2. Levanta los contenedores:

```bash
docker compose up --build
```

3. El proyecto aplicará migraciones al iniciar el contenedor web. Si deseas crear un usuario administrador:

```bash
docker compose exec web python manage.py createsuperuser
```

4. Accede al sistema desde:

```text
http://localhost:8000/
```

---

### Opción local sin Docker

1. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura PostgreSQL y las variables de entorno necesarias.

Ejemplo:

```bash
export DB_NAME=cuchao_db
export DB_USER=cuchao_user
export DB_PASSWORD=Cuchao123
export DB_HOST=localhost
export DB_PORT=5432
```

4. Ejecuta migraciones:

```bash
python manage.py migrate
```

5. Crea un superusuario:

```bash
python manage.py createsuperuser
```

6. Inicia el servidor:

```bash
python manage.py runserver
```

---

## Variables de entorno

El proyecto incluye un archivo `.env.example` con la configuración base:

```env
DEBUG=1
SECRET_KEY=change-me-in-production
DB_NAME=cuchao_db
DB_USER=cuchao_user
DB_PASSWORD=Cuchao123
DB_HOST=db
DB_PORT=5432
```

Para ejecución local sin Docker, normalmente `DB_HOST` debe cambiarse a `localhost`.

---

## Flujo general del sistema

1. El usuario se registra o inicia sesión.
2. Puede publicar un carro con modelo, descripción, imagen y precio.
3. El catálogo muestra todos los carros disponibles o vendidos.
4. Si el carro pertenece al usuario, este puede editarlo o eliminarlo.
5. Si el carro pertenece a otro usuario y está disponible, puede comprarlo.
6. El sistema registra la compra y marca el carro como vendido.
7. El administrador puede gestionar usuarios, carros y compras desde Django Admin.

---

## Modelos del sistema

### `Usuario`
Modelo personalizado basado en `AbstractUser`.

### `Carro`
Campos principales:
- `propietario`
- `modelo`
- `descripcion`
- `imagen`
- `precio`
- `vendido`

### `Compra`
Campos principales:
- `comprador`
- `carro`
- `metodo_pago`
- `precio_pagado`
- `fecha_compra`

---

## Archivos importantes del proyecto

- `carros/models.py`: definición de modelos
- `carros/views.py`: lógica de registro, login, catálogo, CRUD y compra
- `carros/forms.py`: formularios de usuario y carro
- `carros/admin.py`: configuración del panel de administración
- `templates/`: vistas HTML del sistema
- `docker-compose.yml`: configuración de contenedores
- `COMPRAS.md`: documentación específica del flujo de compra simulada

---

## Estado actual del proyecto

Actualmente el proyecto incluye:
- autenticación de usuarios
- catálogo funcional
- CRUD de carros
- compra simulada
- registro de compras
- soporte con Docker y PostgreSQL
- migraciones de base de datos
- documentación base para fortalecer el repositorio

### Mejoras futuras recomendadas
- agregar pantallazos del sistema al repositorio
- incluir pruebas automatizadas
- exportar y documentar datos ficticios en SQL si el docente lo solicita
- completar la Wiki pública en GitHub
- crear issues, project board y releases para fortalecer la gestión del repositorio
- desplegar la aplicación en la nube

---

## Integrantes
- Carlos Sanchez
- Julian Osorio Alturo 
- Samuel Lenis Mira

> Reemplaza esta sección con los nombres reales del equipo.

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

## Repositorio

Repositorio del proyecto:

```text
https://github.com/cadasaso/cuchao-venta-carros-usados.git
```

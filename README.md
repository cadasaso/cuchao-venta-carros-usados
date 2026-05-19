# Cuchao — Marketplace de Carros Usados

<div align="center">

**Plataforma web para comprar y vender carros usados directamente entre personas**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

</div>

---

## Descripción

**CUCHAO** es una aplicación web desarrollada en **Django** para la compra y venta de carros usados.  
El sistema permite publicar vehículos, explorar el catálogo, buscar y filtrar carros, guardar favoritos, realizar ofertas, enviar mensajes entre comprador y vendedor, simular compras, generar comprobantes, administrar información desde el panel de Django y generar descripciones automáticas con inteligencia artificial.

El proyecto se ejecuta con **Docker Compose**, usando un contenedor web con Django/Gunicorn y un contenedor de base de datos con **PostgreSQL**.

---

## Características principales

- Catálogo de carros usados.
- Búsqueda de vehículos.
- Filtros por marca, categoría, transmisión, combustible, precio y año.
- Registro e inicio de sesión de usuarios.
- Panel administrativo de Django.
- Publicación, edición y eliminación de carros.
- Carga de imágenes de vehículos.
- Favoritos.
- Ofertas y negociación.
- Chat entre comprador y vendedor.
- Notificaciones.
- Historial de visualización.
- Comparador de carros.
- Flujo de compra simulado.
- Selección de método de pago.
- Comprobante final de compra.
- Inversión de dependencias para procesadores de pago.
- API JSON propia para búsqueda de carros.
- Generación automática de descripción con IA usando Cohere.
- Selector de idioma ES/EN.
- Modo claro / modo oscuro.
- Pruebas unitarias.
- Ejecución con Docker y PostgreSQL.

---

## Tecnologías usadas

- Python 3.12+
- Django 5.2
- PostgreSQL 16
- Docker
- Docker Compose
- Gunicorn
- Cohere API
- Pillow
- HTML5
- CSS3
- JavaScript

---

## Requisitos previos

Antes de ejecutar el proyecto se necesita tener instalado:

- Docker
- Docker Compose
- Git

Opcional para la funcionalidad de IA:

- Cuenta en Cohere.
- API key de Cohere.

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/cadasaso/cuchao-venta-carros-usados.git
cd cuchao-venta-carros-usados
```

---

### 2. Crear archivo `.env`

En la raíz del proyecto, al mismo nivel de `docker-compose.yml`, crear un archivo llamado:

```text
.env
```

Contenido recomendado:

```env
COHERE_API_KEY=PEGAR_AQUI_TU_API_KEY
```

Si no se tiene una API key de Cohere, se puede dejar vacío:

```env
COHERE_API_KEY=
```

La aplicación seguirá funcionando normalmente, pero la opción de generación automática de descripción mostrará un mensaje indicando que la variable `COHERE_API_KEY` no está configurada.

**Importante:**  
No subir el archivo `.env` a GitHub.

---

### 3. Levantar el proyecto

```bash
docker compose up -d --build
```

Este comando construye la imagen, levanta la base de datos PostgreSQL y ejecuta la aplicación Django.

---

### 4. Verificar que los contenedores estén activos

```bash
docker compose ps
```

El resultado esperado debe mostrar algo parecido a:

```text
cuchao_db    Up / healthy
cuchao_web   Up
0.0.0.0:8000->8000/tcp
```

---

### 5. Abrir la aplicación

Aplicación:

```text
http://localhost:8000/
```

Panel de administración:

```text
http://localhost:8000/admin/
```

---

## Crear superusuario

Para acceder al panel administrativo de Django, ejecutar:

```bash
docker compose exec web python manage.py createsuperuser
```

Luego ingresar a:

```text
http://localhost:8000/admin/
```

---

## Crear datos de prueba

Si el catálogo aparece vacío, se deben crear carros desde el panel de administración.

Ruta:

```text
http://localhost:8000/admin/
```

Crear por lo menos dos carros de prueba.

### Ejemplo 1

```text
Marca: Mazda
Modelo: Mazda 3
Año: 2021
Kilometraje: 28000
Color: Azul
Transmisión: Automática
Combustible: Gasolina
Categoría: Sedan
Estado: Excelente
Ciudad: Medellín
Precio: 62000000
Vendido: No marcado
Destacado: Marcado
```

### Ejemplo 2

```text
Marca: Toyota
Modelo: Corolla
Año: 2020
Kilometraje: 35000
Color: Blanco
Transmisión: Automática
Combustible: Gasolina
Categoría: Sedan
Estado: Excelente
Ciudad: Bogotá
Precio: 45000000
Vendido: No marcado
Destacado: Marcado
```

Después de crearlos, volver al catálogo:

```text
http://localhost:8000/
```

---

## Rutas principales

| Funcionalidad | Ruta |
|---|---|
| Catálogo principal | `/` |
| Login | `/login/` |
| Registro | `/register/` |
| Panel admin | `/admin/` |
| Agregar carro | `/agregar-carro/` |
| Detalle de carro | `/carro/<carro_id>/` |
| Editar carro | `/editar-carro/<carro_id>/` |
| Eliminar carro | `/eliminar-carro/<carro_id>/` |
| Comprar carro | `/comprar/<carro_id>/` |
| Procesar compra | `/procesar-compra/<carro_id>/` |
| Compra exitosa | `/compra-exitosa/<compra_id>/` |
| Mis compras | `/mis-compras/` |
| Favoritos | `/mis-favoritos/` |
| Agregar o quitar favorito | `/favorito/<carro_id>/` |
| Ofertas | `/ofertas/` |
| Crear oferta | `/ofertar/<carro_id>/` |
| Mensajes | `/mensajes/` |
| Chat | `/chat/<carro_id>/<username>/` |
| Notificaciones | `/notificaciones/` |
| Comparador | `/comparar/` |
| Historial | `/historial/` |
| Dashboard | `/dashboard/` |
| Perfil público | `/perfil/<username>/` |
| Crear reseña | `/perfil/<username>/resena/` |
| Cambiar idioma | `/idioma/` |
| Cambiar tema | `/toggle-tema/` |
| API búsqueda de carros | `/api/buscar/?q=Mazda` |
| API enviar mensaje chat | `/api/chat/<carro_id>/<username>/enviar/` |
| API consultar chat | `/api/chat/<carro_id>/<username>/poll/` |
| API notificaciones | `/api/notificaciones/` |
| API generación de descripción IA | `/api/generar-descripcion/` |

---

## API JSON propia

La aplicación cuenta con un endpoint JSON para buscar carros registrados en el sistema.

Ejemplo:

```text
http://localhost:8000/api/buscar/?q=Mazda
```

Respuesta esperada:

```json
{
  "results": [
    {
      "id": 2,
      "titulo": "Mazda Mazda 3",
      "precio": 62000000,
      "anio": 2021,
      "imagen": "/media/carros/...",
      "url": "/carro/2/"
    }
  ]
}
```

Si la respuesta aparece vacía:

```json
{
  "results": []
}
```

revisar que exista un carro con esa marca o modelo en el panel de administración.

---

## Generación automática de descripción con IA

La aplicación incluye una funcionalidad para generar automáticamente la descripción de un carro usando una API externa de inteligencia artificial.

Ruta principal:

```text
http://localhost:8000/agregar-carro/
```

Endpoint relacionado:

```text
/api/generar-descripcion/
```

### Configurar API key de Cohere

En el archivo `.env` agregar:

```env
COHERE_API_KEY=TU_API_KEY_REAL
```

Luego reiniciar Docker:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

Verificar que Docker leyó la variable:

```bash
docker compose exec web python -c "import os; print('OK' if os.getenv('COHERE_API_KEY') else 'NO')"
```

Resultado esperado:

```text
OK
```

### Probar generación con IA

1. Entrar a:

```text
http://localhost:8000/agregar-carro/
```

2. Llenar datos básicos del carro:

```text
Marca
Modelo
Año
Kilometraje
Color
Transmisión
Combustible
Precio
```

3. Presionar el botón:

```text
Generate with AI
```

4. El sistema generará una descripción sugerida para la publicación.

Si aparece el mensaje:

```text
COHERE_API_KEY no está configurada en las variables de entorno.
```

revisar que:

- El archivo `.env` esté en la raíz del proyecto.
- La variable se llame exactamente `COHERE_API_KEY`.
- El contenedor haya sido reiniciado después de crear o modificar el `.env`.

---

## Chat entre usuarios

La aplicación permite comunicación entre comprador y vendedor mediante una vista de chat asociada a un carro.

Rutas relacionadas:

```text
/mensajes/
/mensaje/enviar/<carro_id>/
/chat/<carro_id>/<username>/
/api/chat/<carro_id>/<username>/enviar/
/api/chat/<carro_id>/<username>/poll/
```

Para probar el chat:

1. Crear un carro con un usuario vendedor.
2. Iniciar sesión con otro usuario comprador.
3. Entrar al detalle del carro.
4. Enviar mensaje al vendedor.
5. Revisar la conversación en la vista de chat.

---

## Flujo de compra

La compra es simulada y no realiza cobros reales.

Para probar el flujo:

1. Iniciar sesión con un usuario que no sea el propietario del carro.
2. Entrar al catálogo:

```text
http://localhost:8000/
```

3. Abrir el detalle de un carro.
4. Presionar comprar.
5. Seleccionar método de pago.
6. Confirmar compra.
7. Ver el comprobante final de compra.

Rutas relacionadas:

```text
/comprar/<carro_id>/
/procesar-compra/<carro_id>/
/compra-exitosa/<compra_id>/
/mis-compras/
```

Métodos de pago simulados:

- Efectivo
- PSE
- Tarjeta de crédito
- Financiación

---

## Inversión de dependencias en métodos de pago

El sistema aplica inversión de dependencias en la lógica de pagos.  
La lógica principal de compra no depende directamente de una única clase concreta, sino de una abstracción que permite manejar diferentes métodos de pago.

Elementos principales:

```text
PaymentProcessor
CashProcessor
PSEProcessor
CardProcessor
FinanceProcessor
PaymentProcessorFactory
```

Esto permite agregar nuevos métodos de pago sin modificar directamente todo el flujo principal de compra.

---

## Internacionalización ES/EN

La aplicación cuenta con selector de idioma en la barra de navegación.

Rutas de cambio de idioma:

```text
/idioma/?lang=es&next=/
/idioma/?lang=en&next=/
```

Si al presionar ES o EN el idioma no cambia, ejecutar:

```bash
docker compose exec web sh -c "apt-get update && apt-get install -y gettext"
docker compose exec web python manage.py compilemessages
docker compose restart web
```

Después recargar el navegador con:

```text
Ctrl + F5
```

---

## Modo claro / oscuro

La aplicación permite cambiar entre modo claro y modo oscuro desde la barra de navegación.

Ruta relacionada:

```text
/toggle-tema/
```

---

## Pruebas unitarias

Para ejecutar las pruebas:

```bash
docker compose exec web python manage.py test
```

Resultado esperado:

```text
Found 12 test(s).
System check identified no issues.
Ran 12 tests in ...
OK
```

---

## Comandos útiles

Ver contenedores:

```bash
docker compose ps
```

Ver logs del contenedor web:

```bash
docker compose logs -f web
```

Ver logs de la base de datos:

```bash
docker compose logs -f db
```

Reiniciar solo el servidor web:

```bash
docker compose restart web
```

Entrar a la consola de Django:

```bash
docker compose exec web python manage.py shell
```

Crear superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Acceder a PostgreSQL:

```bash
docker compose exec db psql -U cuchao_user -d cuchao_db
```

Apagar contenedores sin borrar datos:

```bash
docker compose down
```

Apagar contenedores y borrar datos de base de datos:

```bash
docker compose down -v
```

Reconstruir todo desde cero:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d --force-recreate
```

---

## Solución de problemas comunes

### 1. El catálogo aparece vacío

Crear carros desde el panel de administración:

```text
http://localhost:8000/admin/
```

Verificar que:

- El carro no esté marcado como vendido.
- El carro tenga precio.
- El carro tenga marca y modelo.
- El usuario propietario esté asignado.

---

### 2. El puerto 8000 ya está ocupado

Revisar contenedores activos:

```bash
docker ps
```

Si hay un contenedor viejo usando el puerto `8000`, eliminarlo:

```bash
docker rm -f NOMBRE_DEL_CONTENEDOR
```

También se puede cambiar el puerto en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

Y abrir:

```text
http://localhost:8001/
```

---

### 3. Se muestra una versión vieja del catálogo

Puede ocurrir si hay contenedores antiguos activos o caché del navegador.

Ejecutar:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

Luego recargar el navegador con:

```text
Ctrl + F5
```

Si el problema sigue, revisar contenedores antiguos:

```bash
docker ps -a
```

Eliminar los contenedores viejos relacionados con CUCHAO:

```bash
docker rm -f cuchao_web
docker rm -f cuchao_db
```

Y volver a levantar:

```bash
docker compose up -d --build
```

---

### 4. La base de datos no conecta

Revisar estado:

```bash
docker compose ps
```

Ver logs de PostgreSQL:

```bash
docker compose logs -f db
```

Reiniciar el contenedor web:

```bash
docker compose restart web
```

Si sigue fallando:

```bash
docker compose down
docker compose up -d --build
```

---

### 5. No puedo entrar al admin

Crear un superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Luego entrar a:

```text
http://localhost:8000/admin/
```

---

### 6. La API `/api/buscar/` responde vacío

Probar con una marca existente:

```text
http://localhost:8000/api/buscar/?q=Mazda
```

Si responde vacío, revisar que exista un carro Mazda en el panel de administración.

---

### 7. La IA no genera descripción

Verificar que el archivo `.env` tenga:

```env
COHERE_API_KEY=TU_API_KEY_REAL
```

Verificar que Docker reconoce la variable:

```bash
docker compose exec web python -c "import os; print('OK' if os.getenv('COHERE_API_KEY') else 'NO')"
```

Si sale:

```text
NO
```

revisar que el archivo `.env` esté en la raíz del proyecto y reiniciar:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

---

### 8. El selector de idioma no cambia

Instalar `gettext`, compilar traducciones y reiniciar:

```bash
docker compose exec web sh -c "apt-get update && apt-get install -y gettext"
docker compose exec web python manage.py compilemessages
docker compose restart web
```

Después recargar con:

```text
Ctrl + F5
```

---

### 9. Aparece advertencia de Docker Compose sobre `version`

Si aparece una advertencia como:

```text
the attribute `version` is obsolete
```

no afecta la ejecución del proyecto.

Para quitarla, borrar la línea `version:` del archivo `docker-compose.yml`.

---

### 10. Los cambios no se ven en el navegador

Reiniciar el servidor web:

```bash
docker compose restart web
```

Recargar sin caché:

```text
Ctrl + F5
```

---

## Estructura del proyecto

```text
cuchao-venta-carros-usados/
├── carros/
│   ├── migrations/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── context_processors.py
│   └── services/
├── cuchao/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   ├── catalogo.html
│   ├── detalle_carro.html
│   ├── agregar_carro.html
│   ├── chat.html
│   ├── mensajes.html
│   ├── dashboard.html
│   └── ...
├── static/
├── media/
├── locale/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## Notas para evaluadores

- El proyecto se ejecuta con Docker Compose.
- La base de datos usada es PostgreSQL.
- Las migraciones se ejecutan automáticamente al iniciar el contenedor web.
- Si el catálogo aparece vacío, se deben crear carros desde `/admin/`.
- La compra es simulada y no realiza cobros reales.
- Para usar la generación con IA se necesita configurar `COHERE_API_KEY`.
- Si `COHERE_API_KEY` no está configurada, el resto de la aplicación funciona normalmente.
- El endpoint JSON propio disponible es `/api/buscar/?q=Mazda`.
- El chat se evidencia mediante `/chat/<carro_id>/<username>/`.
- Las pruebas unitarias se ejecutan con `docker compose exec web python manage.py test`.
- El selector ES/EN está disponible en la barra de navegación.

---

## Autores

Proyecto desarrollado para la materia **Tópicos Especiales en Ingeniería de Software**.

Integrantes:

- Carlos David Sanchez Soto
- Julian
- Samuel


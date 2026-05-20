# README de Arquitectura — CUCHAO

## 1. Descripción general

**CUCHAO** es una aplicación web para compra y venta de carros usados desarrollada con **Django**. El sistema permite publicar vehículos, explorar un catálogo, filtrar carros, enviar mensajes entre comprador y vendedor, realizar ofertas, simular compras, generar comprobantes, exponer un servicio JSON propio, generar descripciones con IA y administrar información desde el panel de Django.

La aplicación sigue la arquitectura **MVT** propia de Django, equivalente al patrón MVC:

- **Model**: define las entidades y reglas de persistencia.
- **View**: procesa las solicitudes, ejecuta lógica de negocio y retorna respuestas.
- **Template**: renderiza la interfaz visible para el usuario.

Además, el proyecto incorpora una capa de **servicios** para separar lógica de negocio, mejorar la mantenibilidad y aplicar inversión de dependencias en el procesamiento de pagos.

---

## 2. Tecnologías principales

| Tecnología | Uso dentro del proyecto |
|---|---|
| Python 3.12+ | Lenguaje principal |
| Django 5.2 | Framework web |
| PostgreSQL 16 | Base de datos relacional |
| Docker | Contenedorización |
| Docker Compose | Orquestación local de contenedores |
| Gunicorn | Servidor WSGI para ejecutar Django |
| Cohere API | Generación automática de descripciones con IA |
| HTML/CSS/JavaScript | Interfaz de usuario |
| Pillow | Manejo de imágenes |

---

## 3. Vista general de arquitectura

La arquitectura general del sistema se organiza así:

```text
Usuario / Navegador
        ↓
Docker Compose
        ↓
Contenedor web: Django + Gunicorn
        ↓
urls.py
        ↓
views.py
        ↓
services/
        ↓
models.py
        ↓
PostgreSQL
        ↑
templates/
        ↑
Usuario / Navegador
```

La aplicación se ejecuta dentro de Docker Compose con dos servicios principales:

```text
Docker Compose
├── web: Django + Gunicorn
└── db: PostgreSQL
```

---

## 4. Arquitectura MVT en Django

### 4.1 Model

Los modelos representan las entidades principales del sistema y se encuentran en:

```text
carros/models.py
```

Entidades principales:

- `Usuario`
- `Carro`
- `CarroImagen`
- `Etiqueta`
- `Favorito`
- `Oferta`
- `Mensaje`
- `Compra`
- `Notificacion`
- `Resena`
- `HistorialVista`

Estos modelos permiten representar el catálogo de carros, los usuarios, la comunicación, las compras, favoritos, ofertas, reseñas y notificaciones del sistema.

### 4.2 View

Las vistas se encuentran principalmente en:

```text
carros/views.py
```

Las vistas reciben solicitudes del navegador o de endpoints internos, procesan la lógica necesaria y devuelven una respuesta HTML o JSON.

Funcionalidades procesadas por las vistas:

- Catálogo principal.
- Detalle de carro.
- Login y registro.
- Publicación de carros.
- Flujo de compra.
- Chat entre usuarios.
- Favoritos.
- Ofertas.
- Notificaciones.
- API JSON de búsqueda.
- Generación automática de descripción con IA.
- Cambio de idioma.
- Cambio de tema claro/oscuro.

### 4.3 Template

Los templates contienen la interfaz visual del sistema y se encuentran en:

```text
templates/
```

Templates principales:

- `base.html`
- `catalogo.html`
- `detalle_carro.html`
- `agregar_carro.html`
- `chat.html`
- `mensajes.html`
- `dashboard.html`
- templates de compra
- templates de autenticación
- templates de perfil

Los templates reciben información desde las vistas y muestran la interfaz al usuario final.

---

## 5. Capa de servicios

El proyecto incluye una capa de servicios para separar lógica de negocio de las vistas.

Ubicación:

```text
carros/services/
```

Servicios principales:

- `VentaService`
- `CatalogoService`
- `NotificacionService`
- `PaymentProcessorFactory`
- procesadores de pago

Esta separación permite que las vistas no contengan toda la lógica del negocio y facilita el mantenimiento del código.

---

## 6. Lógica de negocio principal

### 6.1 Catálogo de vehículos

El catálogo permite visualizar carros publicados, usar filtros y buscar vehículos.

Ruta principal:

```text
/
```

Flujo:

```text
Usuario → Catálogo → View → Query a Carro → Template
```

### 6.2 Publicación de carros

Los usuarios autenticados pueden publicar carros indicando marca, modelo, año, precio, kilometraje, imágenes y descripción.

Ruta:

```text
/agregar-carro/
```

La descripción puede ser escrita manualmente o generada automáticamente con IA.

### 6.3 Compra simulada

El flujo de compra permite seleccionar un vehículo disponible, elegir método de pago y generar un comprobante.

Rutas relacionadas:

```text
/comprar/<carro_id>/
/procesar-compra/<carro_id>/
/compra-exitosa/<compra_id>/
/mis-compras/
```

Reglas de negocio principales:

- Un usuario no debe comprar su propio carro.
- Un carro vendido no debe venderse nuevamente.
- La compra se registra con precio, comprador, carro, método de pago y referencia.
- El carro queda marcado como vendido después de la compra.
- Se genera un comprobante final.

### 6.4 Chat entre comprador y vendedor

El sistema permite comunicación entre usuarios relacionada con un vehículo.

Rutas relacionadas:

```text
/mensajes/
/mensaje/enviar/<carro_id>/
/chat/<carro_id>/<username>/
/api/chat/<carro_id>/<username>/enviar/
/api/chat/<carro_id>/<username>/poll/
```

Flujo:

```text
Comprador → Detalle del carro → Enviar mensaje → Mensaje guardado → Chat visible para ambos usuarios
```

### 6.5 Ofertas

Los usuarios pueden realizar ofertas sobre un vehículo publicado.

Ruta relacionada:

```text
/ofertar/<carro_id>/
```

La oferta queda asociada al comprador, al carro y al vendedor.

### 6.6 Favoritos

El usuario puede guardar carros de interés para consultarlos después.

Rutas relacionadas:

```text
/favorito/<carro_id>/
/mis-favoritos/
```

---

## 7. API JSON propia

CUCHAO expone un endpoint JSON propio para buscar carros.

Ruta:

```text
/api/buscar/?q=Mazda
```

Ejemplo de respuesta:

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

Uso dentro de la arquitectura:

```text
Cliente externo / navegador
        ↓
/api/buscar/
        ↓
urls.py
        ↓
views.py
        ↓
models.py
        ↓
PostgreSQL
        ↓
Respuesta JSON
```

---

## 8. Consumo de API externa

La aplicación consume una API externa mediante la funcionalidad de generación automática de descripción con IA.

Ruta principal:

```text
/agregar-carro/
```

Endpoint relacionado:

```text
/api/generar-descripcion/
```

Variable de entorno necesaria:

```env
COHERE_API_KEY=TU_API_KEY_REAL
```

Flujo:

```text
Usuario llena datos del carro
        ↓
Presiona Generate with AI
        ↓
Django recibe la solicitud
        ↓
Se envían datos a Cohere API
        ↓
Cohere responde con texto generado
        ↓
La descripción sugerida se muestra en el formulario
```

Si `COHERE_API_KEY` no está configurada, el sistema muestra un mensaje controlado y el resto de la aplicación continúa funcionando.

---

## 9. Inversión de dependencias

El sistema aplica inversión de dependencias en el procesamiento de pagos.

La lógica principal de compra no depende directamente de una clase concreta, sino de una abstracción para manejar diferentes métodos de pago.

Elementos principales:

```text
PaymentProcessor
CashProcessor
PSEProcessor
CardProcessor
FinanceProcessor
PaymentProcessorFactory
```

Relación general:

```text
VentaService
    ↓
PaymentProcessorFactory
    ↓
PaymentProcessor
    ├── CashProcessor
    ├── PSEProcessor
    ├── CardProcessor
    └── FinanceProcessor
```

Ventajas:

- Permite agregar nuevos métodos de pago sin modificar todo el flujo principal.
- Reduce acoplamiento.
- Mejora mantenibilidad.
- Cumple el principio de inversión de dependencias.

---

## 10. Internacionalización

La aplicación incluye soporte para español e inglés mediante el sistema de internacionalización de Django.

Elementos relacionados:

```text
LocaleMiddleware
locale/
templates/
selector ES/EN
```

Rutas de cambio de idioma:

```text
/idioma/?lang=es&next=/
/idioma/?lang=en&next=/
```

El selector ES/EN se muestra en la barra de navegación.

---

## 11. Docker y despliegue local

El proyecto se ejecuta con Docker Compose.

Servicios principales:

```text
web: Django + Gunicorn
db: PostgreSQL
```

Comando de ejecución:

```bash
docker compose up -d --build
```

Comando de verificación:

```bash
docker compose ps
```

Resultado esperado:

```text
cuchao_db    Up / healthy
cuchao_web   Up
0.0.0.0:8000->8000/tcp
```

---

## 12. Base de datos

La base de datos usada es PostgreSQL.

El contenedor de base de datos almacena la información de:

- usuarios
- carros
- imágenes
- compras
- ofertas
- favoritos
- mensajes
- notificaciones
- reseñas
- historial

---

## 13. Pruebas unitarias

El proyecto cuenta con pruebas unitarias ejecutables desde Docker.

Comando:

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

## 14. Seguridad y configuración

El archivo `.env` se usa para variables sensibles como:

```env
COHERE_API_KEY=
```

Este archivo no debe subirse al repositorio.

El archivo `.gitignore` debe incluir:

```gitignore
.env
```

---

## 15. Resumen de componentes

```text
Usuario / Navegador
    ↓
Django urls.py
    ↓
Django views.py
    ↓
services/
    ↓
models.py
    ↓
PostgreSQL
```

Componentes externos:

```text
Cohere API ← Django services/views
Cliente externo → /api/buscar/ → Django → JSON
```

Componentes de interfaz:

```text
Templates HTML
CSS
JavaScript
Selector ES/EN
Modo claro/oscuro
```

---

## 16. Conclusión

La arquitectura de CUCHAO combina el patrón MVT de Django con una capa de servicios para separar responsabilidades. El sistema integra Docker, PostgreSQL, API JSON propia, consumo de API externa, internacionalización, lógica de negocio de compra, chat, favoritos, ofertas y pruebas unitarias.

Esta estructura permite que la aplicación sea más mantenible, fácil de ejecutar y coherente con los requisitos de la entrega.

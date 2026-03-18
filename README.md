# CUCHAO

## Descripción
CUCHAO es una aplicación web desarrollada para la venta de carros usados. El sistema busca facilitar a los clientes la consulta de vehículos disponibles, permitiendo visualizar información detallada, aplicar filtros de búsqueda y apoyar el proceso de compra de manera más clara, rápida y confiable.

## Objetivo
Desarrollar una aplicación web con Django y PostgreSQL que permita gestionar la venta de carros usados, diferenciando una sección para usuarios finales y una sección para administradores, con autenticación mediante login y funcionalidades que mejoren la experiencia del usuario.

## Integrantes
- Nombre del integrante 1
- Nombre del integrante 2
- Nombre del integrante 3
- Nombre del integrante 4

## Tecnologías utilizadas
- Python
- Django
- PostgreSQL
- Docker
- HTML
- CSS
- JavaScript

## Arquitectura del sistema
El proyecto está basado en la arquitectura **MVT (Model - View - Template)** de Django, permitiendo organizar el sistema en capas para facilitar la interacción entre cliente, servidor, modelos de datos, vistas y plantillas.

## Estructura general del sistema
El sistema gestiona la información relacionada con:
- Carros
- Clientes
- Vendedores
- Ventas

## Secciones principales de la aplicación
La aplicación cuenta con dos secciones principales:

### 1. Sección de usuario final
Permite al usuario consultar los carros disponibles, ver sus características, aplicar filtros de búsqueda y realizar acciones relacionadas con la consulta o compra de vehículos.

**Ruta principal sugerida:**  
`/`

### 2. Sección de administrador
Permite la gestión interna del sistema, incluyendo administración de vehículos, ventas, clientes y demás elementos del proyecto.

**Ruta sugerida del panel administrativo:**  
`/admin/`

## Sistema de autenticación
El proyecto implementa un sistema de login funcional con Django, permitiendo controlar el acceso a la sección administrativa y diferenciar las vistas del usuario final de las vistas del administrador.

## Funcionalidades principales
- Visualización del catálogo de carros usados
- Consulta detallada de cada vehículo
- Registro e inicio de sesión de usuarios
- Gestión de ventas
- Gestión de clientes
- Gestión de vehículos

## Funcionalidades interesantes
El sistema debe incluir al menos 4 funcionalidades interesantes diferentes a las operaciones tradicionales de crear, editar, borrar y leer. Algunas funcionalidades planteadas para el proyecto son:

- Búsqueda de carros por nombre, marca o modelo
- Filtrado de vehículos por precio, año o kilometraje
- Generación de factura de venta en PDF
- Visualización de los vehículos más vendidos o destacados

## Ejecución del proyecto
El proyecto está preparado para ejecutarse usando Docker.

### Requisitos previos
- Docker
- Docker Compose

### Pasos generales de ejecución
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/cadasaso/cuchao-venta-carros-usados.git

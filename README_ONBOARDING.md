# README de Onboarding — CUCHAO

## 1. Objetivo de este documento

Este documento explica cómo una persona nueva puede preparar, ejecutar, probar y validar el proyecto **CUCHAO** desde cero.

Incluye:

- instalación
- configuración
- ejecución con Docker
- creación de datos de prueba
- uso del panel admin
- prueba de funcionalidades principales
- ejecución de pruebas unitarias
- solución de errores comunes

---

## 2. Requisitos previos

Antes de empezar se necesita tener instalado:

- Git
- Docker
- Docker Compose
- Navegador web

Opcional:

- Cuenta en Cohere para usar generación automática de descripción con IA.

---

## 3. Clonar el repositorio

Ejecutar:

```bash
git clone https://github.com/cadasaso/cuchao-venta-carros-usados.git
cd cuchao-venta-carros-usados
```

---

## 4. Crear archivo `.env`

En la raíz del proyecto, donde está `docker-compose.yml`, crear un archivo llamado:

```text
.env
```

Contenido:

```env
COHERE_API_KEY=PEGAR_AQUI_TU_API_KEY
```

Si no se tiene API key, dejarlo así:

```env
COHERE_API_KEY=
```

La aplicación funciona aunque la key esté vacía. Lo único que no funcionará completamente será la generación automática de descripción con IA.

No subir `.env` a GitHub.

---

## 5. Levantar el proyecto con Docker

Ejecutar:

```bash
docker compose up -d --build
```

Este comando:

- construye la imagen del proyecto
- levanta el contenedor web
- levanta el contenedor de PostgreSQL
- deja la aplicación disponible en el puerto 8000

---

## 6. Verificar contenedores

Ejecutar:

```bash
docker compose ps
```

Resultado esperado:

```text
cuchao_db    Up / healthy
cuchao_web   Up
0.0.0.0:8000->8000/tcp
```

Si ambos contenedores están arriba, abrir:

```text
http://localhost:8000/
```

---

## 7. Crear superusuario

Para entrar al panel de administración:

```bash
docker compose exec web python manage.py createsuperuser
```

Luego abrir:

```text
http://localhost:8000/admin/
```

Ingresar con el usuario creado.

---

## 8. Crear datos de prueba

Si el catálogo está vacío, crear carros desde:

```text
http://localhost:8000/admin/
```

Entrar a la sección de carros y crear mínimo dos registros.

### Carro de prueba 1

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

### Carro de prueba 2

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

Después volver a:

```text
http://localhost:8000/
```

---

## 9. Probar catálogo

Abrir:

```text
http://localhost:8000/
```

Validar que se vea:

- listado de carros
- filtros
- botones de detalle
- selector ES/EN
- navegación principal

---

## 10. Probar login y registro

Registro:

```text
http://localhost:8000/register/
```

Login:

```text
http://localhost:8000/login/
```

Crear un usuario normal para probar funcionalidades como compra, favoritos, ofertas y mensajes.

---

## 11. Probar publicación de carro

Abrir:

```text
http://localhost:8000/agregar-carro/
```

Llenar datos del carro y guardar.

Campos recomendados:

```text
Marca
Modelo
Año
Kilometraje
Color
Transmisión
Combustible
Categoría
Estado
Ciudad
Descripción
Precio
Imagen
```

---

## 12. Probar generación de descripción con IA

Primero verificar que el `.env` tenga:

```env
COHERE_API_KEY=TU_API_KEY_REAL
```

Reiniciar:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

Verificar que Docker leyó la variable:

```bash
docker compose exec web python -c "import os; print('OK' if os.getenv('COHERE_API_KEY') else 'NO')"
```

Debe salir:

```text
OK
```

Luego abrir:

```text
http://localhost:8000/agregar-carro/
```

Llenar datos básicos y presionar:

```text
Generate with AI
```

El sistema debe generar una descripción sugerida.

---

## 13. Probar API JSON propia

Abrir en navegador:

```text
http://localhost:8000/api/buscar/?q=Mazda
```

Debe responder JSON parecido a:

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

Si responde vacío, revisar que exista un carro Mazda en el admin y que no esté marcado como vendido.

---

## 14. Probar compra simulada

Pasos:

1. Iniciar sesión con un usuario que no sea el dueño del carro.
2. Ir al catálogo:

```text
http://localhost:8000/
```

3. Entrar al detalle de un carro.
4. Presionar comprar.
5. Seleccionar método de pago.
6. Confirmar compra.
7. Ver comprobante final.

Rutas relacionadas:

```text
/comprar/<carro_id>/
/procesar-compra/<carro_id>/
/compra-exitosa/<compra_id>/
```

Importante:

- La compra es simulada.
- No se realizan pagos reales.
- Después de comprar, el carro puede quedar marcado como vendido.

---

## 15. Probar chat entre usuarios

Para probar el chat correctamente se necesitan dos usuarios:

- usuario vendedor
- usuario comprador

Pasos:

1. Crear un carro con el usuario vendedor.
2. Cerrar sesión.
3. Iniciar sesión con el usuario comprador.
4. Entrar al detalle del carro.
5. Enviar mensaje al vendedor.
6. Abrir la conversación.

Rutas relacionadas:

```text
/mensajes/
/mensaje/enviar/<carro_id>/
/chat/<carro_id>/<username>/
/api/chat/<carro_id>/<username>/enviar/
/api/chat/<carro_id>/<username>/poll/
```

---

## 16. Probar favoritos

Abrir el detalle de un carro y usar el botón de favorito.

Rutas relacionadas:

```text
/favorito/<carro_id>/
/mis-favoritos/
```

---

## 17. Probar ofertas

Abrir un carro y realizar oferta.

Ruta relacionada:

```text
/ofertar/<carro_id>/
```

---

## 18. Probar selector de idioma

Abrir:

```text
http://localhost:8000/
```

Usar los botones:

```text
ES
EN
```

También se puede probar directamente:

```text
http://localhost:8000/idioma/?lang=es&next=/
http://localhost:8000/idioma/?lang=en&next=/
```

Si no cambia el idioma, revisar la sección de errores comunes.

---

## 19. Probar modo claro / oscuro

Usar el botón de tema en la barra de navegación.

Ruta relacionada:

```text
/toggle-tema/
```

---

## 20. Ejecutar pruebas unitarias

Ejecutar:

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

## 21. Comandos útiles

Ver contenedores:

```bash
docker compose ps
```

Ver logs web:

```bash
docker compose logs -f web
```

Ver logs base de datos:

```bash
docker compose logs -f db
```

Reiniciar web:

```bash
docker compose restart web
```

Entrar a shell Django:

```bash
docker compose exec web python manage.py shell
```

Crear superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Apagar sin borrar datos:

```bash
docker compose down
```

Apagar borrando datos:

```bash
docker compose down -v
```

Reconstruir desde cero:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d --force-recreate
```

---

## 22. Errores comunes y solución

### Error: el catálogo aparece vacío

Solución:

1. Entrar a:

```text
http://localhost:8000/admin/
```

2. Crear carros.
3. Verificar que no estén marcados como vendidos.

---

### Error: el puerto 8000 está ocupado

Ver contenedores:

```bash
docker ps
```

Eliminar contenedor viejo:

```bash
docker rm -f NOMBRE_DEL_CONTENEDOR
```

O cambiar el puerto en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

Abrir:

```text
http://localhost:8001/
```

---

### Error: aparece una versión vieja del catálogo

Ejecutar:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

Luego recargar navegador:

```text
Ctrl + F5
```

Si sigue pasando:

```bash
docker ps -a
```

Eliminar contenedores viejos de CUCHAO.

---

### Error: no puedo entrar al admin

Crear superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

---

### Error: `/api/buscar/` responde vacío

Probar con una marca existente:

```text
http://localhost:8000/api/buscar/?q=Mazda
```

Si sigue vacío, crear un carro Mazda desde el admin.

---

### Error: la IA no genera descripción

Verificar `.env`:

```env
COHERE_API_KEY=TU_API_KEY_REAL
```

Verificar variable dentro del contenedor:

```bash
docker compose exec web python -c "import os; print('OK' if os.getenv('COHERE_API_KEY') else 'NO')"
```

Si sale `NO`, el archivo `.env` está mal ubicado o no se reinició Docker.

Reiniciar:

```bash
docker compose down
docker compose up -d --build --force-recreate
```

---

### Error: el idioma no cambia

Ejecutar:

```bash
docker compose exec web sh -c "apt-get update && apt-get install -y gettext"
docker compose exec web python manage.py compilemessages
docker compose restart web
```

Luego recargar con:

```text
Ctrl + F5
```

---

### Advertencia: `version` is obsolete

Si Docker muestra:

```text
the attribute `version` is obsolete
```

no afecta el funcionamiento.

Para quitarlo, borrar la línea `version:` de `docker-compose.yml`.

---

## 23. Checklist final para una persona nueva

Antes de considerar el proyecto listo, verificar:

- [ ] Docker levanta correctamente.
- [ ] `docker compose ps` muestra web y db activos.
- [ ] La app abre en `http://localhost:8000/`.
- [ ] El admin abre en `/admin/`.
- [ ] Hay mínimo dos carros creados.
- [ ] El catálogo muestra carros.
- [ ] `/api/buscar/?q=Mazda` responde JSON.
- [ ] La generación con IA funciona o muestra error controlado.
- [ ] El chat funciona entre dos usuarios.
- [ ] La compra simulada genera comprobante.
- [ ] El selector ES/EN está visible.
- [ ] Las pruebas terminan en `OK`.

---

## 24. Recomendación para evaluadores

Para revisar rápidamente el proyecto:

1. Ejecutar Docker.
2. Crear superusuario.
3. Crear dos carros desde admin.
4. Abrir catálogo.
5. Probar compra.
6. Probar `/api/buscar/?q=Mazda`.
7. Probar generación con IA.
8. Ejecutar pruebas.

Con estos pasos se validan los elementos principales del sistema.

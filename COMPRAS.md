# Sistema de Compra Simulada - Documentación

Esta documentación explica cómo funciona el sistema de compra simulada implementado en Cuchao.

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Modelos de Datos](#modelos-de-datos)
3. [Flujo de Compra](#flujo-de-compra)
4. [Vistas Implementadas](#vistas-implementadas)
5. [Templates](#templates)
6. [Rutas](#rutas)
7. [Instalación y Runing](#instalación-y-running)
8. [Pruebas](#pruebas)

---

## Descripción General

El sistema permite a los usuarios **comprar productos simulados (vehículos)** sin integrar pasarelas de pago reales. 

### Características:
- Flujo de compra simple de 3 pasos
- Selección de método de pago (Efectivo, PSE simulado)
- Registro de compras en la base de datos
- Marcar productos como vendidos automáticamente
- Confirmación visual de compra exitosa
- Validaciones de seguridad

---

## Modelos de Datos

### 1. Modelo `Carro` (Actualizado)

```python
class Carro(models.Model):
    propietario = ForeignKey(Usuario, ...)
    modelo = CharField(max_length=100)
    descripcion = TextField(blank=True)
    imagen = ImageField(upload_to='carros/', ...)
    precio = DecimalField(max_digits=10, decimal_places=2)
    vendido = BooleanField(default=False) 
    
    def esta_disponible(self):
        """Retorna True si el carro no está vendido"""
        return not self.vendido
```

**Cambios:**
- Agregado campo `vendido` (BooleanField, por defecto False)
- Agregado método `esta_disponible()` para verificar disponibilidad

---

### 2. Modelo `Compra` (NUEVO)

```python
class Compra(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('pse', 'PSE (Simulado)'),
    ]
    
    comprador = ForeignKey(Usuario, related_name='compras')
    carro = ForeignKey(Carro, related_name='ventas')
    metodo_pago = CharField(max_length=20, choices=METODOS_PAGO)
    precio_pagado = DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_compra']
```

**Campos:**
- `comprador`: Usuario que realiza la compra
- `carro`: Vehículo que se compra
- `metodo_pago`: 'efectivo' o 'pse'
- `precio_pagado`: Monto pagado (snapshot del precio al momento de la compra)
- `fecha_compra`: Timestamp automático de cuándo se realizó la compra

---

## Flujo de Compra

El flujo consta de **3 pasos**:

### Paso 1: Ver Catálogo y Seleccionar Producto
```
Catálogo → [Botón "Comprar"] → Vista de Confirmación
```

- Usuario ve el catálogo con productos disponibles
- Si el producto está disponible (vendido=False) y el usuario está autenticado, ve el botón "Comprar"
- Al hacer clic, se redirige a `confirmar_compra`

### Paso 2: Confirmar Compra y Elegir Método de Pago
```
Vista Confirmación → [Seleccionar método] → [Botón "Realizar Compra"]
```

- Se muestra:
  - Image del producto
  - Nombre, descripción, precio
  - Opciones de método de pago (radio buttons)
- Usuario selecciona un método de pago
- Al hacer clic "Realizar Compra", se envía un POST a `procesar_compra`

### Paso 3: Procesar Compra y Mostrar Éxito
```
Procesamiento → [Guardar en BD] → Página de Éxito
```

- Se crea un registro de `Compra` en la BD
- Se marca el `Carro` como `vendido=True`
- Se redirige a la página de éxito
- Se muestra número de transacción (ID de la compra)

---

## Vistas Implementadas

### 1. Vista `confirmar_compra()` - GET

**URL:** `/comprar/<int:carro_id>/`

**Propósito:** Mostrar la página de confirmación de compra

**Código:**
```python
@login_required(login_url='login')
@require_http_methods(["GET"])
def confirmar_compra(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    
    # Verificar que el carro no esté vendido
    if carro.vendido:
        messages.error(request, 'Este carro ya ha sido vendido.')
        return redirect('catalogo')
    
    metodos_pago = [
        ('efectivo', 'Efectivo'),
        ('pse', 'PSE (Simulado)'),
    ]
    
    contexto = {
        'carro': carro,
        'metodos_pago': metodos_pago,
    }
    
    return render(request, 'confirmar_compra.html', contexto)
```

**Validaciones:**
- Usuario debe estar autenticado (`@login_required`)
- Solo acepta GET (`@require_http_methods(["GET"])`)
- Verifica que el carro existe
- Verifica que no está vendido

---

### 2. Vista `procesar_compra()` - POST

**URL:** `/procesar-compra/<int:carro_id>/` (POST)

**Propósito:** Procesar la compra y guardarla en BD

**Código:**
```python
@login_required(login_url='login')
@require_http_methods(["POST"])
def procesar_compra(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    
    # Validar que no esté vendido
    if carro.vendido:
        messages.error(request, 'Este carro ya ha sido vendido.')
        return redirect('catalogo')
    
    # Obtener método de pago del formulario
    metodo_pago = request.POST.get('metodo_pago', 'efectivo')
    
    # Validar método de pago
    if metodo_pago not in ['efectivo', 'pse']:
        messages.error(request, 'Método de pago inválido.')
        return redirect('confirmar_compra', carro_id=carro_id)
    
    # Crear compra
    compra = Compra.objects.create(
        comprador=request.user,
        carro=carro,
        metodo_pago=metodo_pago,
        precio_pagado=carro.precio
    )
    
    # Marcar como vendido
    carro.vendido = True
    carro.save()
    
    # Mensaje de éxito
    messages.success(request, f'¡Compra realizada exitosamente!')
    
    # Redirigir a éxito
    return redirect('compra_exitosa', compra_id=compra.id)
```

**Lógica:**
1. Validar que el carro existe y no está vendido
2. Obtener el método de pago del formulario POST
3. Validar que es un método permitido
4. Crear registroCompra con los datos
5. Marcar el carro como vendido
6. Guardar cambios
7. Mostrar mensaje de éxito
8. Redirigir a página de éxito

---

### 3. Vista `compra_exitosa()` - GET

**URL:** `/compra-exitosa/<int:compra_id>/`

**Propósito:** Mostrar confirmación final de la compra

**Código:**
```python
@login_required(login_url='login')
@require_http_methods(["GET"])
def compra_exitosa(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    
    # Verificar que el usuario es el comprador
    if compra.comprador != request.user:
        return HttpResponseForbidden('No tienes permiso para ver esta compra.')
    
    contexto = {'compra': compra}
    return render(request, 'compra_exitosa.html', contexto)
```

**Validaciones:**
- Usuario debe estar autenticado
- Solo muestra si el usuario actual es el comprador (seguridad)

---

## Templates

### 1. `confirmar_compra.html`

**Ubicación:** `templates/confirmar_compra.html`

**Contenido:**
- Imagen del producto
- Modelo, descripción, precio
- Vendedor
- Radio buttons para seleccionar método de pago
- Botón "Realizar Compra" (POST)
- Botón "Cancelar"

### 2. `compra_exitosa.html`

**Ubicación:** `templates/compra_exitosa.html`

**Contenido:**
- Icono de éxito (✔)
- Mensaje de confirmación
- Detalles de la compra:
  - Producto
  - Precio pagado
  - Método de pago
  - Fecha y hora
  - ID de transacción simulado
- Botón "Volver al Catálogo"

### 3. `catalogo.html` (Actualizado)

**Cambios:**
- Agregado indicador de estado: "Disponible" o "Vendido"
- Agregado botón "Comprar" (solo si está disponible)
- El botón de compra solo aparece si:
  - El usuario está autenticado
  - El producto no está vendido
  - El usuario no es el propietario

---

## Rutas

Agregadas las siguientes rutas a `carros/urls.py`:

```python
path('comprar/<int:carro_id>/', views.confirmar_compra, name='confirmar_compra'),
path('procesar-compra/<int:carro_id>/', views.procesar_compra, name='procesar_compra'),
path('compra-exitosa/<int:compra_id>/', views.compra_exitosa, name='compra_exitosa'),
```

---

## Instalación y Running

### Paso 1: Aplicar Migraciones

```bash
# Con Docker
docker compose exec web python manage.py makemigrations

# Sin Docker
python manage.py makemigrations
```

Esto creará un archivo de migración en `carros/migrations/` con los cambios a los modelos.

### Paso 2: Aplicar la Migración

```bash
# Con Docker
docker compose exec web python manage.py migrate

# Sin Docker
python manage.py migrate
```

Esto creará:
- Nueva columna `vendido` en tabla `Carro`
- Nueva tabla `Compra`

### Paso 3: Reiniciar el Servidor (si es necesario)

```bash
# Con Docker
docker compose restart web

# Sin Docker
python manage.py runserver
```

---

## Pruebas

### Test Manual Completo:

1. **Registrarse como Usuario A**
   - Ir a http://localhost:8000/register/
   - Crear usuario "usuario_a" con contraseña

2. **Crear un Producto**
   - Ir a http://localhost:8000/agregar-carro/
   - Llenar formulario
   - Guardar
   - Se debe ver en el catálogo

3. **Registrarse como Usuario B**
   - Logout primero
   - Registrarse como "usuario_b"

4. **Comprar el Producto**
   - Ir al catálogo
   - Encontrar el producto de usuario_a
   - Verificar que aparece botón "Disponible" y botón "Comprar"
   - Hacer clic en "Comprar"
   - Seleccionar método de pago
   - Hacer clic en "Realizar Compra"
   - Debe redirigir a página de éxito con detalles

5. **Verificar que se Marcó como Vendido**
   - Ir al catálogo
   - El producto debe mostrar "Vendido" (sin botón de compra)

6. **Verificar en Admin**
   - Ir a http://localhost:8000/admin/
   - Buscar el carro: debe mostrar `vendido = True`
   - Ver tabla de Compras: debe haber un registro con usuario_b como comprador

---

## Notas de Seguridad

1. **Autenticación:** Todas las vistas de compra requieren usuario autenticado
2. **Autorización:** 
   - No puedes comprar tu propio producto
   - No puedes ver detalles de compra de otros usuarios
3. **Validación:** Se valida que un producto no se venda dos veces (field `vendido`)
4. **Atomicidad:** Compra y cambio de `vendido` en la misma transacción

---

## Posibles Mejoras Futuras

1. Historial de compras en el panel de usuario
2. Descargar recibo (PDF)
3. Cancelación de compra (con período de tiempo)
4. Notificaciones por email
5. Sistema de calificaciones comprador/vendedor
6. Exposición de API REST

---

## Contacto

Para preguntas sobre la implementación, consulta los comentarios en:
- `carros/models.py`
- `carros/views.py`
- `carros/urls.py`


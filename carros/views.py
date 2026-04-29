from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, InvalidOperation
import json

from .forms import (
    UsuarioCreationForm, CarroForm, PerfilForm, ResenaForm, MensajeForm, OfertaForm
)
from .models import (
    Carro, Compra, Favorito, Resena, Mensaje, Usuario,
    Oferta, Notificacion, HistorialVista, Etiqueta
)


# ----------------- AUTH -----------------
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Notificacion.crear(
                user, 'sistema', 'Bienvenido a Cuchao',
                'Empieza explorando el catálogo o publica tu primer carro.',
                '/', ''
            )
            messages.success(request, f'¡Bienvenido a Cuchao, {user.username}!')
            return redirect('catalogo')
    else:
        form = UsuarioCreationForm()
    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username or not password:
            return render(request, 'login.html', {'error': 'Usuario y contraseña requeridos'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalogo')
        return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('catalogo')


# ----------------- CATÁLOGO Y BÚSQUEDA -----------------
def catalogo(request):
    """Catálogo con filtros y búsqueda avanzada."""
    carros = Carro.objects.select_related('propietario').prefetch_related('etiquetas')

    q = request.GET.get('q', '').strip()
    marca = request.GET.get('marca', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    transmision = request.GET.get('transmision', '').strip()
    combustible = request.GET.get('combustible', '').strip()
    precio_min = request.GET.get('precio_min', '').strip()
    precio_max = request.GET.get('precio_max', '').strip()
    anio_min = request.GET.get('anio_min', '').strip()
    etiqueta = request.GET.get('etiqueta', '').strip()
    solo_disponibles = request.GET.get('disponibles', '')
    orden = request.GET.get('orden', 'recientes')

    if q:
        carros = carros.filter(
            Q(modelo__icontains=q) | Q(marca__icontains=q) |
            Q(descripcion__icontains=q) | Q(ciudad__icontains=q)
        )
    if marca:
        carros = carros.filter(marca__icontains=marca)
    if categoria:
        carros = carros.filter(categoria=categoria)
    if transmision:
        carros = carros.filter(transmision=transmision)
    if combustible:
        carros = carros.filter(combustible=combustible)
    if precio_min.isdigit():
        carros = carros.filter(precio__gte=int(precio_min))
    if precio_max.isdigit():
        carros = carros.filter(precio__lte=int(precio_max))
    if anio_min.isdigit():
        carros = carros.filter(anio__gte=int(anio_min))
    if etiqueta.isdigit():
        carros = carros.filter(etiquetas__id=int(etiqueta))
    if solo_disponibles == '1':
        carros = carros.filter(vendido=False)

    if orden == 'precio_asc':
        carros = carros.order_by('precio')
    elif orden == 'precio_desc':
        carros = carros.order_by('-precio')
    elif orden == 'populares':
        carros = carros.order_by('-vistas')
    else:
        carros = carros.order_by('-fecha_publicacion')

    favoritos_ids = set()
    if request.user.is_authenticated:
        favoritos_ids = set(
            Favorito.objects.filter(usuario=request.user).values_list('carro_id', flat=True)
        )

    destacados = Carro.objects.filter(destacado=True, vendido=False)[:3]
    if not destacados.exists():
        destacados = Carro.objects.filter(vendido=False).order_by('-vistas')[:3]

    # Recientemente vistos
    recientes = []
    if request.user.is_authenticated:
        recientes = Carro.objects.filter(
            historial_vistas__usuario=request.user
        ).order_by('-historial_vistas__fecha').distinct()[:4]

    context = {
        'carros': carros,
        'destacados': destacados,
        'favoritos_ids': favoritos_ids,
        'recientes': recientes,
        'todas_etiquetas': Etiqueta.objects.all(),
        'filtros': {
            'q': q, 'marca': marca, 'categoria': categoria,
            'transmision': transmision, 'combustible': combustible,
            'precio_min': precio_min, 'precio_max': precio_max,
            'anio_min': anio_min, 'orden': orden, 'etiqueta': etiqueta,
            'disponibles': solo_disponibles,
        },
        'categorias': Carro.CATEGORIAS,
        'transmisiones': Carro.TRANSMISIONES,
        'combustibles': Carro.COMBUSTIBLES,
        'total_resultados': carros.count(),
    }
    return render(request, 'catalogo.html', context)


def detalle_carro(request, carro_id):
    carro = get_object_or_404(
        Carro.objects.select_related('propietario').prefetch_related('etiquetas', 'imagenes'),
        id=carro_id
    )
    Carro.objects.filter(id=carro_id).update(vistas=carro.vistas + 1)

    es_favorito = False
    mis_ofertas = []
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, carro=carro).exists()
        # registrar historial
        HistorialVista.objects.update_or_create(usuario=request.user, carro=carro)
        mis_ofertas = Oferta.objects.filter(carro=carro, comprador=request.user).order_by('-fecha')[:3]

    similares = Carro.objects.filter(
        categoria=carro.categoria, vendido=False
    ).exclude(id=carro.id)[:4]

    return render(request, 'detalle_carro.html', {
        'carro': carro,
        'es_favorito': es_favorito,
        'similares': similares,
        'mensaje_form': MensajeForm(),
        'oferta_form': OfertaForm(),
        'mis_ofertas': mis_ofertas,
    })


# ----------------- CRUD CARRO -----------------
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def agregar_carro(request):
    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save(commit=False)
            carro.propietario = request.user
            carro.save()
            form.save_m2m()
            messages.success(request, '¡Tu carro fue publicado exitosamente!')
            return redirect('catalogo')
    else:
        form = CarroForm()
    return render(request, 'agregar_carro.html', {'form': form})


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def editar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if carro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso para editar este carro')
    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES, instance=carro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carro actualizado correctamente.')
            return redirect('catalogo')
    else:
        form = CarroForm(instance=carro)
    return render(request, 'editar_carro.html', {'form': form, 'carro': carro})


@login_required(login_url='login')
@require_http_methods(["POST"])
def eliminar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if carro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso para eliminar este carro')
    carro.delete()
    messages.success(request, 'Carro eliminado.')
    return redirect('catalogo')


# ----------------- COMPRAS -----------------
@login_required(login_url='login')
@require_http_methods(["GET"])
def confirmar_compra(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if carro.vendido:
        messages.error(request, 'Este carro ya ha sido vendido.')
        return redirect('catalogo')
    return render(request, 'confirmar_compra.html', {
        'carro': carro,
        'metodos_pago': Compra.METODOS_PAGO,
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def procesar_compra(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if carro.vendido:
        messages.error(request, 'Este carro ya ha sido vendido.')
        return redirect('catalogo')
    metodo_pago = request.POST.get('metodo_pago', 'efectivo')
    if metodo_pago not in dict(Compra.METODOS_PAGO):
        messages.error(request, 'Método de pago inválido.')
        return redirect('confirmar_compra', carro_id=carro_id)
    compra = Compra.objects.create(
        comprador=request.user, carro=carro,
        metodo_pago=metodo_pago, precio_pagado=carro.precio
    )
    carro.vendido = True
    carro.save()
    # Notificaciones
    Notificacion.crear(
        carro.propietario, 'venta', f'Vendiste tu {carro.modelo}',
        f'{request.user.username} compró tu carro por ${carro.precio:,.0f}.',
        f'/dashboard/', ''
    )
    Notificacion.crear(
        request.user, 'compra', f'Compra exitosa: {carro.modelo}',
        'Revisa los detalles en "Mis compras".',
        f'/mis-compras/', ''
    )
    messages.success(request, f'¡Compra realizada! Adquiriste {carro.modelo}.')
    return redirect('compra_exitosa', compra_id=compra.id)


@login_required(login_url='login')
@require_http_methods(["GET"])
def compra_exitosa(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if compra.comprador != request.user:
        return HttpResponseForbidden('No tienes permiso para ver esta compra.')
    return render(request, 'compra_exitosa.html', {'compra': compra})


@login_required(login_url='login')
def mis_compras(request):
    compras = Compra.objects.filter(comprador=request.user).select_related('carro')
    return render(request, 'mis_compras.html', {'compras': compras})


# ----------------- FAVORITOS -----------------
@login_required(login_url='login')
@require_http_methods(["POST"])
def toggle_favorito(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    fav, creado = Favorito.objects.get_or_create(usuario=request.user, carro=carro)
    if not creado:
        fav.delete()
        accion = 'removido'
    else:
        accion = 'agregado'
        if carro.propietario and carro.propietario != request.user:
            Notificacion.crear(
                carro.propietario, 'favorito',
                f'A {request.user.username} le encantó tu {carro.modelo}',
                'Tu publicación está ganando atención.',
                f'/carro/{carro.id}/', ''
            )
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'accion': accion})
    return redirect(request.META.get('HTTP_REFERER') or 'catalogo')


@login_required(login_url='login')
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('carro')
    return render(request, 'favoritos.html', {'favoritos': favoritos})


# ----------------- DASHBOARD -----------------
@login_required(login_url='login')
def dashboard(request):
    """Dashboard de vendedor con estadísticas + chart por meses."""
    user = request.user
    mis_carros = Carro.objects.filter(propietario=user)
    ventas = Compra.objects.filter(carro__propietario=user)
    ingresos = ventas.aggregate(t=Sum('precio_pagado'))['t'] or 0
    total_vistas = mis_carros.aggregate(t=Sum('vistas'))['t'] or 0

    hace_30 = timezone.now() - timedelta(days=30)
    ventas_recientes = ventas.filter(fecha_compra__gte=hace_30).count()

    no_leidos = Mensaje.objects.filter(destinatario=user, leido=False).count()
    ofertas_pendientes = Oferta.objects.filter(carro__propietario=user, estado='pendiente').count()

    # Serie mensual de ventas (últimos 6 meses)
    ahora = timezone.now()
    chart_labels, chart_values = [], []
    meses_es = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    for i in range(5, -1, -1):
        # Compute month i months ago
        m = ahora.month - i
        y = ahora.year
        while m <= 0:
            m += 12
            y -= 1
        count = ventas.filter(fecha_compra__year=y, fecha_compra__month=m).count()
        chart_labels.append(meses_es[m-1])
        chart_values.append(count)
    max_chart = max(chart_values) if chart_values and max(chart_values) > 0 else 1
    chart_data = [
        {'label': l, 'value': v, 'pct': int(v / max_chart * 100)}
        for l, v in zip(chart_labels, chart_values)
    ]

    context = {
        'mis_carros': mis_carros,
        'total_carros': mis_carros.count(),
        'disponibles': mis_carros.filter(vendido=False).count(),
        'vendidos': mis_carros.filter(vendido=True).count(),
        'total_ventas': ventas.count(),
        'ingresos': ingresos,
        'total_vistas': total_vistas,
        'ventas_recientes': ventas_recientes,
        'mensajes_no_leidos': no_leidos,
        'ofertas_pendientes': ofertas_pendientes,
        'favoritos_recibidos': Favorito.objects.filter(carro__propietario=user).count(),
        'ultimas_ventas': ventas.order_by('-fecha_compra')[:5],
        'chart_data': chart_data,
    }
    return render(request, 'dashboard.html', context)


# ----------------- PERFIL -----------------
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('perfil_publico', username=request.user.username)
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'editar_perfil.html', {'form': form})


def perfil_publico(request, username):
    vendedor = get_object_or_404(Usuario, username=username)
    carros = Carro.objects.filter(propietario=vendedor)
    resenas = vendedor.resenas_recibidas.all()
    ya_calificado = False
    if request.user.is_authenticated and request.user != vendedor:
        ya_calificado = Resena.objects.filter(autor=request.user, vendedor=vendedor).exists()
    return render(request, 'perfil.html', {
        'vendedor': vendedor,
        'carros': carros,
        'resenas': resenas,
        'ya_calificado': ya_calificado,
        'resena_form': ResenaForm(),
    })


@login_required(login_url='login')
@require_http_methods(["POST"])
def crear_resena(request, username):
    vendedor = get_object_or_404(Usuario, username=username)
    if vendedor == request.user:
        messages.error(request, 'No puedes calificarte a ti mismo.')
        return redirect('perfil_publico', username=username)
    if Resena.objects.filter(autor=request.user, vendedor=vendedor).exists():
        messages.error(request, 'Ya has calificado a este vendedor.')
        return redirect('perfil_publico', username=username)
    form = ResenaForm(request.POST)
    if form.is_valid():
        r = form.save(commit=False)
        r.autor = request.user
        r.vendedor = vendedor
        r.save()
        Notificacion.crear(
            vendedor, 'resena', f'{request.user.username} te dejó una reseña',
            f'Calificación: {r.calificacion}/5',
            f'/perfil/{vendedor.username}/', ''
        )
        messages.success(request, '¡Reseña publicada!')
    return redirect('perfil_publico', username=username)


# ----------------- MENSAJES / CHAT -----------------
@login_required(login_url='login')
@require_http_methods(["POST"])
def enviar_mensaje(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if not carro.propietario or carro.propietario == request.user:
        messages.error(request, 'No puedes enviarte mensajes a ti mismo.')
        return redirect('detalle_carro', carro_id=carro_id)
    form = MensajeForm(request.POST)
    if form.is_valid():
        m = form.save(commit=False)
        m.remitente = request.user
        m.destinatario = carro.propietario
        m.carro = carro
        m.save()
        Notificacion.crear(
            carro.propietario, 'mensaje', f'Nuevo mensaje de {request.user.username}',
            m.contenido[:80], f'/chat/{carro.id}/{request.user.username}/', ''
        )
    return redirect('chat', carro_id=carro_id, username=carro.propietario.username)


@login_required(login_url='login')
def bandeja_mensajes(request):
    todos = Mensaje.objects.filter(
        Q(remitente=request.user) | Q(destinatario=request.user)
    ).select_related('remitente', 'destinatario', 'carro').order_by('-fecha')

    seen = set()
    conversaciones = []
    for m in todos:
        otro = m.destinatario if m.remitente == request.user else m.remitente
        key = (otro.id, m.carro_id)
        if key not in seen:
            seen.add(key)
            no_leidos = Mensaje.objects.filter(
                remitente=otro, destinatario=request.user,
                carro=m.carro, leido=False
            ).count()
            conversaciones.append({
                'otro': otro,
                'carro': m.carro,
                'ultimo': m,
                'no_leidos': no_leidos,
            })
    return render(request, 'mensajes.html', {'conversaciones': conversaciones})


@login_required(login_url='login')
def chat(request, carro_id, username):
    carro = get_object_or_404(Carro, id=carro_id)
    otro = get_object_or_404(Usuario, username=username)
    if otro == request.user:
        return redirect('bandeja_mensajes')
    mensajes_chat = Mensaje.objects.filter(carro=carro).filter(
        Q(remitente=request.user, destinatario=otro) |
        Q(remitente=otro, destinatario=request.user)
    ).order_by('fecha')
    mensajes_chat.filter(destinatario=request.user, leido=False).update(leido=True)
    return render(request, 'chat.html', {
        'carro': carro,
        'otro': otro,
        'mensajes': mensajes_chat,
    })


@login_required(login_url='login')
@require_POST
def api_enviar_chat(request, carro_id, username):
    carro = get_object_or_404(Carro, id=carro_id)
    otro = get_object_or_404(Usuario, username=username)
    if otro == request.user:
        return JsonResponse({'error': 'No puedes enviarte mensajes a ti mismo.'}, status=400)
    contenido = request.POST.get('contenido', '').strip()
    if not contenido:
        return JsonResponse({'error': 'Mensaje vacío.'}, status=400)
    if len(contenido) > 1000:
        return JsonResponse({'error': 'Mensaje demasiado largo.'}, status=400)
    m = Mensaje.objects.create(
        remitente=request.user, destinatario=otro,
        carro=carro, contenido=contenido,
    )
    Notificacion.crear(
        otro, 'mensaje', f'Nuevo mensaje de {request.user.username}',
        contenido[:80], f'/chat/{carro.id}/{request.user.username}/', ''
    )
    return JsonResponse({
        'ok': True, 'id': m.id,
        'contenido': m.contenido,
        'fecha': m.fecha.strftime('%d/%m %H:%M'),
    })


@login_required(login_url='login')
def api_chat_poll(request, carro_id, username):
    carro = get_object_or_404(Carro, id=carro_id)
    otro = get_object_or_404(Usuario, username=username)
    since_id = int(request.GET.get('since', 0))
    nuevos = Mensaje.objects.filter(
        carro=carro, id__gt=since_id
    ).filter(
        Q(remitente=request.user, destinatario=otro) |
        Q(remitente=otro, destinatario=request.user)
    ).order_by('fecha')
    nuevos.filter(destinatario=request.user, leido=False).update(leido=True)
    return JsonResponse({'mensajes': [
        {
            'id': m.id,
            'contenido': m.contenido,
            'fecha': m.fecha.strftime('%d/%m %H:%M'),
            'es_mio': m.remitente_id == request.user.id,
        }
        for m in nuevos
    ]})


# ====================================================
# ===========  NUEVAS FUNCIONES AVANZADAS  ===========
# ====================================================

# ----------------- OFERTAS / NEGOCIACIÓN -----------------
@login_required(login_url='login')
@require_POST
def crear_oferta(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    if carro.vendido:
        messages.error(request, 'Este carro ya fue vendido.')
        return redirect('detalle_carro', carro_id=carro_id)
    if carro.propietario == request.user:
        messages.error(request, 'No puedes ofertar por tu propio carro.')
        return redirect('detalle_carro', carro_id=carro_id)
    form = OfertaForm(request.POST)
    if form.is_valid():
        oferta = form.save(commit=False)
        oferta.carro = carro
        oferta.comprador = request.user
        oferta.save()
        Notificacion.crear(
            carro.propietario, 'oferta',
            f'Nueva oferta por tu {carro.modelo}: ${oferta.monto:,.0f}',
            f'{request.user.username} hizo una oferta ({oferta.porcentaje_descuento}% menos).',
            '/ofertas/', ''
        )
        messages.success(request, 'Tu oferta fue enviada al vendedor.')
    else:
        messages.error(request, 'Oferta inválida.')
    return redirect('detalle_carro', carro_id=carro_id)


@login_required(login_url='login')
def mis_ofertas(request):
    """Ofertas hechas por mí + ofertas recibidas en mis carros."""
    hechas = Oferta.objects.filter(comprador=request.user).select_related('carro')
    recibidas = Oferta.objects.filter(carro__propietario=request.user).select_related('carro', 'comprador')
    return render(request, 'ofertas.html', {
        'hechas': hechas,
        'recibidas': recibidas,
    })


@login_required(login_url='login')
@require_POST
def responder_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    if oferta.carro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso.')
    accion = request.POST.get('accion')
    if accion == 'aceptar':
        oferta.estado = 'aceptada'
        oferta.save()
        Notificacion.crear(
            oferta.comprador, 'oferta_resp',
            f'Tu oferta por {oferta.carro.modelo} fue ACEPTADA',
            f'Procede con la compra por ${oferta.monto:,.0f}.',
            f'/carro/{oferta.carro.id}/', ''
        )
        messages.success(request, 'Oferta aceptada.')
    elif accion == 'rechazar':
        oferta.estado = 'rechazada'
        oferta.save()
        Notificacion.crear(
            oferta.comprador, 'oferta_resp',
            f'Tu oferta por {oferta.carro.modelo} fue rechazada',
            'Puedes hacer una nueva oferta más alta.',
            f'/carro/{oferta.carro.id}/', ''
        )
        messages.info(request, 'Oferta rechazada.')
    elif accion == 'contraofertar':
        try:
            monto = Decimal(request.POST.get('monto', '0'))
            if monto <= 0:
                raise InvalidOperation
            oferta.estado = 'contraoferta'
            oferta.contraoferta_monto = monto
            oferta.save()
            Notificacion.crear(
                oferta.comprador, 'oferta_resp',
                f'Contraoferta por {oferta.carro.modelo}: ${monto:,.0f}',
                'El vendedor propone un nuevo precio.',
                f'/carro/{oferta.carro.id}/', ''
            )
            messages.success(request, 'Contraoferta enviada.')
        except (InvalidOperation, TypeError):
            messages.error(request, 'Monto de contraoferta inválido.')
    return redirect('mis_ofertas')


# ----------------- NOTIFICACIONES -----------------
@login_required(login_url='login')
def notificaciones_panel(request):
    notifs = Notificacion.objects.filter(usuario=request.user)[:50]
    return render(request, 'notificaciones.html', {'notificaciones': notifs})


@login_required(login_url='login')
def api_notificaciones(request):
    """Endpoint AJAX para el dropdown de notificaciones."""
    qs = Notificacion.objects.filter(usuario=request.user)[:10]
    no_leidas = Notificacion.objects.filter(usuario=request.user, leida=False).count()
    data = [
        {
            'id': n.id, 'tipo': n.tipo, 'titulo': n.titulo,
            'mensaje': n.mensaje, 'icono': n.icono, 'url': n.url,
            'leida': n.leida,
            'hace': _humanizar_tiempo(n.fecha),
        }
        for n in qs
    ]
    return JsonResponse({'notificaciones': data, 'no_leidas': no_leidas})


@login_required(login_url='login')
@require_POST
def marcar_notif_leida(request, notif_id):
    n = get_object_or_404(Notificacion, id=notif_id, usuario=request.user)
    n.leida = True
    n.save()
    return JsonResponse({'ok': True})


@login_required(login_url='login')
@require_POST
def marcar_todas_leidas(request):
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    return JsonResponse({'ok': True})


def _humanizar_tiempo(fecha):
    delta = timezone.now() - fecha
    s = delta.total_seconds()
    if s < 60: return 'hace un momento'
    if s < 3600: return f'hace {int(s//60)} min'
    if s < 86400: return f'hace {int(s//3600)} h'
    if s < 604800: return f'hace {int(s//86400)} d'
    return fecha.strftime('%d/%m/%Y')


# ----------------- COMPARACIÓN DE CARROS -----------------
def comparar_carros(request):
    """Compara hasta 4 carros lado a lado vía ?ids=1,2,3"""
    ids_str = request.GET.get('ids', '')
    ids = [int(x) for x in ids_str.split(',') if x.strip().isdigit()][:4]
    carros = list(Carro.objects.filter(id__in=ids).select_related('propietario'))
    # ordenar como llegaron
    carros.sort(key=lambda c: ids.index(c.id))
    return render(request, 'comparar.html', {
        'carros': carros,
        'ids_csv': ','.join(str(c.id) for c in carros),
    })


# ----------------- API: BÚSQUEDA EN VIVO -----------------
def api_busqueda_rapida(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    carros = Carro.objects.filter(
        Q(modelo__icontains=q) | Q(marca__icontains=q),
        vendido=False
    )[:6]
    results = [
        {
            'id': c.id,
            'titulo': f"{c.marca} {c.modelo}",
            'precio': float(c.precio),
            'anio': c.anio,
            'imagen': c.imagen.url if c.imagen else '',
            'url': f'/carro/{c.id}/',
        }
        for c in carros
    ]
    return JsonResponse({'results': results})


# ----------------- TEMA OSCURO -----------------
@require_POST
def toggle_tema(request):
    if request.user.is_authenticated:
        request.user.tema_oscuro = not request.user.tema_oscuro
        request.user.save(update_fields=['tema_oscuro'])
        return JsonResponse({'ok': True, 'tema_oscuro': request.user.tema_oscuro})
    # invitado: lo maneja JS con localStorage
    return JsonResponse({'ok': True})


# ----------------- HISTORIAL -----------------
@login_required(login_url='login')
def historial(request):
    items = HistorialVista.objects.filter(usuario=request.user).select_related('carro')[:30]
    return render(request, 'historial.html', {'items': items})


# ----------------- IA: GENERAR DESCRIPCIÓN -----------------
@login_required(login_url='login')
@require_POST
def generar_descripcion_ia(request):
    import re
    import cohere

    marca = request.POST.get('marca', '').strip()
    modelo = request.POST.get('modelo', '').strip()
    anio = request.POST.get('anio', '').strip()
    kilometraje = request.POST.get('kilometraje', '').strip()

    if not marca or not modelo or not anio:
        return JsonResponse({'error': 'Marca, modelo y año son requeridos.'}, status=400)

    api_key = getattr(settings, 'COHERE_API_KEY', '')
    if not api_key:
        return JsonResponse(
            {'error': 'COHERE_API_KEY no está configurada en las variables de entorno.'},
            status=500
        )

    try:
        km_desc = f"{int(kilometraje):,} km" if kilometraje.isdigit() else "no especificado"

        prompt = f"""Eres un redactor experto en el mercado automotriz latinoamericano.
Genera contenido de venta para este vehículo:

- Marca: {marca}
- Modelo: {modelo}
- Año: {anio}
- Kilometraje: {km_desc}

Responde ÚNICAMENTE con un JSON válido con esta estructura exacta, sin texto adicional, sin markdown:
{{
  "titulo": "Título atractivo para el anuncio (máximo 80 caracteres)",
  "descripcion": "Descripción profesional del vehículo entre 150 y 200 palabras",
  "ventajas": ["ventaja 1", "ventaja 2", "ventaja 3", "ventaja 4"],
  "texto_persuasivo": "Texto de cierre de 50 a 70 palabras que motive a contactar al vendedor"
}}

Reglas:
- Todo en español con buena ortografía
- Lenguaje natural, confiable y atractivo para un marketplace
- No inventes datos técnicos específicos (CV, torque, consumo exacto)
- Si el kilometraje es bajo para el año, menciónalo como punto positivo
- Adapta el tono al mercado latinoamericano"""

        co = cohere.ClientV2(api_key=api_key)
        response = co.chat(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un redactor experto en automóviles. Responde siempre con JSON puro válido, sin bloques de código markdown ni texto extra.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        text = response.message.content[0].text
        # Elimina bloques ```json ... ``` si el modelo los incluye
        text = re.sub(r'```(?:json)?\s*', '', text).strip().rstrip('`').strip()
        contenido = json.loads(text)
        return JsonResponse({'ok': True, 'data': contenido})

    except Exception as e:
        return JsonResponse({'error': f'Error al generar contenido: {str(e)}'}, status=500)

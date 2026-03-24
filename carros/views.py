from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import UsuarioCreationForm, CarroForm
from .models import Carro, Compra

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogo')
        else:
            print('Errores en el formulario:', form.errors)
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
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('catalogo')

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def agregar_carro(request):
    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save(commit=False)
            carro.propietario = request.user
            carro.save()
            return redirect('catalogo')
    else:
        form = CarroForm()
    return render(request, 'agregar_carro.html', {'form': form})

def catalogo(request):
    carros = Carro.objects.all()
    return render(request, 'catalogo.html', {'carros': carros})

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
    return redirect('catalogo')

@login_required(login_url='login')
@require_http_methods(["GET"])
def confirmar_compra(request, carro_id):
    """
    Vista para mostrar la confirmación de compra.
    Muestra el producto y opciones de método de pago.
    """
    carro = get_object_or_404(Carro, id=carro_id)
    
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


@login_required(login_url='login')
@require_http_methods(["POST"])
def procesar_compra(request, carro_id):
    """
    Vista que procesa la compra simulada.
    - Valida que el carro existe y no esté vendido
    - Recibe el método de pago del formulario
    - Crea un registro de Compra
    - Marca el carro como vendido
    - Redirige a página de éxito
    """
    carro = get_object_or_404(Carro, id=carro_id)
    
    if carro.vendido:
        messages.error(request, 'Este carro ya ha sido vendido.')
        return redirect('catalogo')
    
    metodo_pago = request.POST.get('metodo_pago', 'efectivo')
    
    metodos_validos = ['efectivo', 'pse']
    if metodo_pago not in metodos_validos:
        messages.error(request, 'Método de pago inválido.')
        return redirect('confirmar_compra', carro_id=carro_id)
    
    compra = Compra.objects.create(
        comprador=request.user,
        carro=carro,
        metodo_pago=metodo_pago,
        precio_pagado=carro.precio
    )
    
    carro.vendido = True
    carro.save()
    
    messages.success(
        request,
        f'¡Compra realizada exitosamente! Has comprado {carro.modelo} por ${carro.precio}'
    )
    
    return redirect('compra_exitosa', compra_id=compra.id)


@login_required(login_url='login')
@require_http_methods(["GET"])
def compra_exitosa(request, compra_id):
    """
    Vista que muestra la confirmación final de compra.
    Muestra los detalles de la compra realizada.
    """
    compra = get_object_or_404(Compra, id=compra_id)
    
    if compra.comprador != request.user:
        return HttpResponseForbidden('No tienes permiso para ver esta compra.')
    
    contexto = {
        'compra': compra,
    }
    
    return render(request, 'compra_exitosa.html', contexto)
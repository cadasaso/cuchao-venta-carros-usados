from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from .forms import UsuarioCreationForm, CarroForm
from .models import Carro

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogo')
        else:
            # Mostrar los errores en la consola para debugging
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
    
    # Verificar que solo el propietario puede editar
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
    
    # Verificar que solo el propietario puede eliminar
    if carro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso para eliminar este carro')
    
    carro.delete()
    return redirect('catalogo')
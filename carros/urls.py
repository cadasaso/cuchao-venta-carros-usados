from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('agregar-carro/', views.agregar_carro, name='agregar_carro'),
    path('editar-carro/<int:carro_id>/', views.editar_carro, name='editar_carro'),
    path('eliminar-carro/<int:carro_id>/', views.eliminar_carro, name='eliminar_carro'),
]
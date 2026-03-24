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
    
    path('comprar/<int:carro_id>/', views.confirmar_compra, name='confirmar_compra'),
    path('procesar-compra/<int:carro_id>/', views.procesar_compra, name='procesar_compra'),
    path('compra-exitosa/<int:compra_id>/', views.compra_exitosa, name='compra_exitosa'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('carro/<int:carro_id>/', views.detalle_carro, name='detalle_carro'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD carros
    path('agregar-carro/', views.agregar_carro, name='agregar_carro'),
    path('editar-carro/<int:carro_id>/', views.editar_carro, name='editar_carro'),
    path('eliminar-carro/<int:carro_id>/', views.eliminar_carro, name='eliminar_carro'),

    # Compras
    path('comprar/<int:carro_id>/', views.confirmar_compra, name='confirmar_compra'),
    path('procesar-compra/<int:carro_id>/', views.procesar_compra, name='procesar_compra'),
    path('compra-exitosa/<int:compra_id>/', views.compra_exitosa, name='compra_exitosa'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),

    # Favoritos
    path('favorito/<int:carro_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),

    # Dashboard y perfil
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil_publico, name='perfil_publico'),
    path('perfil/<str:username>/resena/', views.crear_resena, name='crear_resena'),

    # Mensajes / Chat
    path('mensajes/', views.bandeja_mensajes, name='bandeja_mensajes'),
    path('mensaje/enviar/<int:carro_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('chat/<int:carro_id>/<str:username>/', views.chat, name='chat'),
    path('api/chat/<int:carro_id>/<str:username>/enviar/', views.api_enviar_chat, name='api_enviar_chat'),
    path('api/chat/<int:carro_id>/<str:username>/poll/', views.api_chat_poll, name='api_chat_poll'),

    # Ofertas (negociación)
    path('oferta/crear/<int:carro_id>/', views.crear_oferta, name='crear_oferta'),
    path('ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('oferta/<int:oferta_id>/responder/', views.responder_oferta, name='responder_oferta'),

    # Notificaciones
    path('notificaciones/', views.notificaciones_panel, name='notificaciones'),
    path('api/notificaciones/', views.api_notificaciones, name='api_notificaciones'),
    path('api/notificaciones/<int:notif_id>/leida/', views.marcar_notif_leida, name='marcar_notif_leida'),
    path('api/notificaciones/marcar-todas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),

    # Comparador
    path('comparar/', views.comparar_carros, name='comparar_carros'),

    # API búsqueda live
    path('api/buscar/', views.api_busqueda_rapida, name='api_buscar'),

    # Tema oscuro
    path('toggle-tema/', views.toggle_tema, name='toggle_tema'),

    # Historial
    path('historial/', views.historial, name='historial'),

    # Cambio de idioma (GET, sin CSRF)
    path('idioma/', views.cambiar_idioma, name='cambiar_idioma'),

    # IA: generador de descripción
    path('api/generar-descripcion/', views.generar_descripcion_ia, name='generar_descripcion_ia'),
]

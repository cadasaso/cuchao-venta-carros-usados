from .models import Mensaje, Favorito, Notificacion, Oferta


def cuchao_globals(request):
    data = {
        'mensajes_no_leidos_count': 0,
        'favoritos_count': 0,
        'notif_no_leidas': 0,
        'ofertas_pendientes_count': 0,
        'tema_oscuro_user': False,
    }
    if request.user.is_authenticated:
        data['mensajes_no_leidos_count'] = Mensaje.objects.filter(
            destinatario=request.user, leido=False
        ).count()
        data['favoritos_count'] = Favorito.objects.filter(usuario=request.user).count()
        data['notif_no_leidas'] = Notificacion.objects.filter(
            usuario=request.user, leida=False
        ).count()
        data['ofertas_pendientes_count'] = Oferta.objects.filter(
            carro__propietario=request.user, estado='pendiente'
        ).count()
        data['tema_oscuro_user'] = getattr(request.user, 'tema_oscuro', False)
    return data

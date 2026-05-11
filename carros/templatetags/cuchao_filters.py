"""
Filtros de template personalizados para Cuchao.

Uso en templates:
    {% load cuchao_filters %}
    ${{ carro.precio|precio_fmt }}     →  $1.500.000
    ${{ compra.precio_pagado|precio_fmt }}  →  $20.000.000
"""

from django import template

register = template.Library()


@register.filter(name='precio_fmt')
def precio_fmt(value):
    """
    Formatea un número como precio con punto de miles y sin decimales.
    Ejemplos:
        1000        →  1.000
        1500000     →  1.500.000
        20000000    →  20.000.000
    """
    try:
        numero = int(round(float(value)))
        return f"{numero:,}".replace(",", ".")
    except (TypeError, ValueError):
        return value

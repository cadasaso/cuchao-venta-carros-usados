"""
Migración 0008: propietario pasa a NOT NULL con related_name='carros_publicados'.

Pasos:
  1. Elimina cualquier Carro que tenga propietario=NULL (datos huérfanos que
     no deberían existir en un marketplace real).
  2. Altera la columna para quitar NULL y añadir el related_name.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def eliminar_carros_sin_propietario(apps, schema_editor):
    """Borra filas con propietario_id NULL antes de imponer NOT NULL."""
    Carro = apps.get_model('carros', 'Carro')
    huerfanos = Carro.objects.filter(propietario__isnull=True)
    cantidad = huerfanos.count()
    if cantidad:
        huerfanos.delete()
        print(f'  Eliminados {cantidad} carro(s) sin propietario.')


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0007_precio_min_validator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Paso 1: limpiar datos huérfanos
        migrations.RunPython(
            eliminar_carros_sin_propietario,
            reverse_code=migrations.RunPython.noop,
        ),
        # Paso 2: alterar la columna — quita NULL, añade related_name
        migrations.AlterField(
            model_name='carro',
            name='propietario',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='carros_publicados',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

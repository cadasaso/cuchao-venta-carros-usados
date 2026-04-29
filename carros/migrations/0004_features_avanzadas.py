# Migration generada manualmente para las nuevas funciones de Cuchao.
# IMPORTANTE: si tu proyecto ya tiene migraciones intermedias (favoritos, mensajes,
# resenas, etc.), Django las detectará. Lo más seguro es ejecutar:
#   python manage.py makemigrations carros
#   python manage.py migrate
# para que Django sincronice cualquier diferencia automáticamente.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0003_carro_vendido_compra'),
    ]

    operations = [
        # ========== Etiquetas ==========
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, unique=True)),
                ('color', models.CharField(default='#6366f1', max_length=20)),
                ('icono', models.CharField(blank=True, default='🏷', max_length=10)),
            ],
        ),

        # ========== Campos nuevos en Usuario y Carro ==========
        migrations.AddField(
            model_name='usuario',
            name='verificado',
            field=models.BooleanField(default=False, help_text='Vendedor verificado por Cuchao'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='tema_oscuro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carro',
            name='precio_negociable',
            field=models.BooleanField(default=True, help_text='Permite recibir ofertas'),
        ),
        migrations.AddField(
            model_name='carro',
            name='etiquetas',
            field=models.ManyToManyField(blank=True, related_name='carros', to='carros.etiqueta'),
        ),

        # ========== Oferta ==========
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('mensaje', models.TextField(blank=True, max_length=500)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada'), ('contraoferta', 'Contraoferta'), ('expirada', 'Expirada')], default='pendiente', max_length=20)),
                ('contraoferta_monto', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('carro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='carros.carro')),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_hechas', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-fecha']},
        ),

        # ========== Notificacion ==========
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('mensaje', 'Mensaje recibido'), ('oferta', 'Nueva oferta'), ('oferta_resp', 'Respuesta a oferta'), ('venta', 'Carro vendido'), ('compra', 'Compra realizada'), ('favorito', 'Te marcaron favorito'), ('resena', 'Nueva reseña'), ('sistema', 'Sistema')], default='sistema', max_length=20)),
                ('titulo', models.CharField(max_length=140)),
                ('mensaje', models.CharField(blank=True, max_length=300)),
                ('url', models.CharField(blank=True, max_length=300)),
                ('icono', models.CharField(default='', max_length=10)),
                ('leida', models.BooleanField(default=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-fecha']},
        ),

        # ========== HistorialVista ==========
        migrations.CreateModel(
            name='HistorialVista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('carro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_vistas', to='carros.carro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha'],
                'unique_together': {('usuario', 'carro')},
            },
        ),
    ]

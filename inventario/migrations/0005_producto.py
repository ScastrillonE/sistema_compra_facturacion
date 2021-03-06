# Generated by Django 3.0.5 on 2020-04-24 03:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0004_unidadmedida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('user_modification', models.IntegerField(blank=True, null=True)),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('codigo_barra', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio', models.FloatField(default=0)),
                ('existencia', models.IntegerField(default=0)),
                ('ultima_compra', models.DateField(blank=True, null=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Marca')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.SubCategoria')),
                ('unidad_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.UnidadMedida')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'unique_together': {('codigo', 'codigo_barra')},
            },
        ),
    ]

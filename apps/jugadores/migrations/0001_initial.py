# Generated by Django 5.0.3 on 2024-04-28 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugadores',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('posicion_jugador', models.CharField(max_length=200)),
                ('imagen_dni', models.ImageField(blank=True, null=True, upload_to='jugadores/dni')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='jugadores/foto')),
                ('direccion', models.CharField(max_length=150, null=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jugadores', to='equipos.equipos')),
            ],
            options={
                'verbose_name': 'Jugador',
                'verbose_name_plural': 'Jugadores',
            },
        ),
    ]

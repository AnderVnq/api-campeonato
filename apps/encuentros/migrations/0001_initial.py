# Generated by Django 5.0.3 on 2024-04-28 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('arbitros', '0001_initial'),
        ('campeonatos', '0001_initial'),
        ('equipos', '0001_initial'),
        ('jugadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('fecha', models.DateField()),
                ('arbitros', models.ManyToManyField(to='arbitros.arbitro')),
                ('campeonato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encuentros', to='campeonatos.campeonato')),
                ('equipo_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_local', to='equipos.equipos')),
                ('equipo_visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_visitante', to='equipos.equipos')),
            ],
            options={
                'verbose_name': 'Encuentro',
                'verbose_name_plural': 'Encuentros',
            },
        ),
        migrations.CreateModel(
            name='Goles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('minuto', models.PositiveIntegerField()),
                ('encuentro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goles', to='encuentros.encuentro')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goles_jugador', to='jugadores.jugadores')),
            ],
            options={
                'verbose_name': 'Goles',
                'verbose_name_plural': 'Goles',
            },
        ),
        migrations.CreateModel(
            name='Sancion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('tipo', models.CharField(max_length=50)),
                ('minuto', models.PositiveIntegerField()),
                ('motivo', models.TextField()),
                ('encuentro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sanciones', to='encuentros.encuentro')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sancion_jugador', to='jugadores.jugadores')),
            ],
            options={
                'verbose_name': 'Sancion',
                'verbose_name_plural': 'Sanciones',
            },
        ),
    ]

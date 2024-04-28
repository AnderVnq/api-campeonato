# Generated by Django 5.0.3 on 2024-04-28 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campeonato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('nombre', models.CharField(max_length=250, unique=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('tipo', models.CharField(max_length=200)),
                ('lugar', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Campeonato',
                'verbose_name_plural': 'Campeonatos',
            },
        ),
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('nombre', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-20 23:33

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('delegado', models.CharField(max_length=150)),
                ('logo_equipo', models.ImageField(blank=True, null=True, upload_to='logo_equipos')),
            ],
            options={
                'verbose_name': 'Modelo Base',
                'verbose_name_plural': 'Modelos Base',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalEquipos',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(blank=True, editable=False, verbose_name='Fecha Eliminacion')),
                ('nombre', models.CharField(db_index=True, max_length=150)),
                ('delegado', models.CharField(max_length=150)),
                ('logo_equipo', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Modelo Base',
                'verbose_name_plural': 'historical Modelos Base',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

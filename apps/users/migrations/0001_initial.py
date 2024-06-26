# Generated by Django 5.0.3 on 2024-04-28 04:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electrónico')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Apellidos')),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to='perfil/', verbose_name='Imagen de perfil')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', related_query_name='custom_user_group', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', related_query_name='custom_user_permission', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Historical_Emails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion ')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha Modificacion ')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha Eliminacion')),
                ('asunto', models.CharField(max_length=250)),
                ('send_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_send_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Modelo Base',
                'verbose_name_plural': 'Modelos Base',
                'abstract': False,
            },
        ),
    ]

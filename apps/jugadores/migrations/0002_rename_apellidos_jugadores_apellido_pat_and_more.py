# Generated by Django 5.0.3 on 2024-05-01 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugadores', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jugadores',
            old_name='apellidos',
            new_name='apellido_pat',
        ),
        migrations.AddField(
            model_name='jugadores',
            name='apellido_mat',
            field=models.CharField(default=None, max_length=100),
        ),
    ]

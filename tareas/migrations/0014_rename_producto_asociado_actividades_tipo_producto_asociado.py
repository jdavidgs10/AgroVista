# Generated by Django 4.2 on 2024-05-10 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0013_actividades_producto_asociado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actividades',
            old_name='producto_asociado',
            new_name='tipo_producto_asociado',
        ),
    ]

# Generated by Django 4.2 on 2023-12-31 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0013_tareas_id_agroptima'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tareas',
            name='producto_semilla',
        ),
    ]

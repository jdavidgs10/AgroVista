# Generated by Django 4.2 on 2024-05-10 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0014_rename_producto_asociado_actividades_tipo_producto_asociado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tareas',
            name='producto_asociado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tareas.productos'),
        ),
    ]

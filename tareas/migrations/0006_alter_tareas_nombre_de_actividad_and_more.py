# Generated by Django 5.0 on 2023-12-26 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0005_alter_tareas_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tareas',
            name='nombre_de_actividad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividad_nombre', to='tareas.actividades'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='nombre_de_cosecha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tareas.cosechas'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='predio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tareas.predios'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='producto_semilla',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_semilla', to='tareas.productos'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='producto_utilizado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto_utilizado', to='tareas.productos'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='unidades_siembra',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

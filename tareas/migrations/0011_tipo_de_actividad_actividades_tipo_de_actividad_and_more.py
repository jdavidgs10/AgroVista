# Generated by Django 5.0 on 2023-12-27 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0010_remove_actividades_tipo_de_actividad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_de_Actividad',
            fields=[
                ('theme_act_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Theme')),
                ('tipo_de_actividad', models.CharField(max_length=200, null=True)),
                ('descripcion', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='actividades',
            name='tipo_de_actividad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tareas.tipo_de_actividad'),
        ),
        migrations.DeleteModel(
            name='Themes_Actividades',
        ),
    ]

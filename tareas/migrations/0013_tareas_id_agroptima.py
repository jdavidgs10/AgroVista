# Generated by Django 5.0 on 2023-12-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0012_rename_theme_act_id_tipo_de_actividad_tipo_act_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tareas',
            name='id_agroptima',
            field=models.IntegerField(null=True),
        ),
    ]

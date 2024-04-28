# Generated by Django 4.2 on 2024-03-17 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0008_doc_repo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indice_Calor',
            fields=[
                ('indice_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Lluvias')),
                ('fecha', models.DateField(null=True)),
                ('lectura_de_temperatura', models.FloatField(null=True)),
                ('lectura_de_humedad', models.FloatField(null=True)),
                ('indice_de_calor', models.FloatField(null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
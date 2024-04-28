import csv
from django.core.management.base import BaseCommand
from tareas.models import Actividades, Tipo_de_Actividad

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the Actividades model, matching each actividad with its tipo_de_actividad'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Attempt to find an existing Tipo_de_Actividad based on a unique identifier, such as its name
                tipo_de_actividad, _ = Tipo_de_Actividad.objects.get_or_create(
                    tipo_de_actividad=row['tipo_de_actividad'],
                    descripcion={'descripcion': 'Automatically created'}
                )

                # Create or update Actividades instance
                Actividades.objects.update_or_create(
                    actividades_id=row['actividades_id'],
                    defaults={
                        'nombre_de_actividad': row['nombre_de_actividad'],
                        'descripcion': row['descripcion'],
                        'tiempo_requerido': int(row['tiempo_requerido']) if row['tiempo_requerido'] else None,
                        'tipo_de_actividad': tipo_de_actividad,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from "{csv_file_path}"'))

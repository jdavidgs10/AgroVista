import csv
from django.core.management.base import BaseCommand
from tareas.models import Tipo_de_Actividad  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the Tipo_de_Actividades model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Tipo_de_Actividad.objects.create(
                    tipo_de_actividad=row['tipo_de_actividad'],
                    descripcion=row['descripcion']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file_path))

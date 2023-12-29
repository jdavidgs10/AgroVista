import csv
from django.core.management.base import BaseCommand
from tareas.models import Cosechas  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the Cosechas model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Cosechas.objects.create(
                    nombre_de_cosecha=row['nombre_de_cosecha'],
                    descripcion=row['descripcion']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file_path))

import csv
from django.core.management.base import BaseCommand
from tareas.models import Lluvias
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the Lluvias model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fecha = datetime.strptime(row['fecha'], '%Y-%m-%d').date()
                lectura_de_lluvia = float(row['lectura_de_lluvia'])  # Convert to float instead of int
                Lluvias.objects.create(fecha=fecha, lectura_de_lluvia=lectura_de_lluvia)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file_path))

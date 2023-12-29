import csv
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from tareas.models import Tareas, Actividades, Cosechas, Predios, Empleados  # Replace with your actual models

class Command(BaseCommand):
    help = 'Import Tareas data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8', errors='ignore') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        actividad = Actividades.objects.get(row['nombre_de_actividad']) if row['nombre_de_actividad'] else None
                        cosecha = Cosechas.objects.get(row['nombre_de_cosecha']) if row['nombre_de_cosecha'] else None
                        predio = Predios.objects.get(row['predio']) if row['predio'] else None
                        empleado = Empleados.objects.get(row['empleado']) if row['empleado'] else None
                    except ValueError as e:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to value error: {e}"))

                       
                        # Create Tareas object
                        Tareas.objects.create(
                            nombre_de_actividad=actividad,
                            nombre_de_cosecha=cosecha,
                            predio=predio,
                            empleado=empleado,
                            tiempo_de_actividad=int(row['tiempo_de_actividad']) if row['tiempo_de_actividad'] else None,
                            # ... other fields ...
                        )
                    except ObjectDoesNotExist as e:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to missing object: {e}"))
                    except ValueError as e:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to value error: {e}"))

            self.stdout.write(self.style.SUCCESS('Data successfully imported from "%s"' % csv_file_path))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))


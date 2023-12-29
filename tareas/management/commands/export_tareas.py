import csv
from django.core.management.base import BaseCommand
from tareas.models import Tareas  # Replace 'tareas' with your actual app name if different

class Command(BaseCommand):
    help = 'Export Tareas data to a CSV file'

    def handle(self, *args, **kwargs):
        with open('tareas_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Writing the header with original field names
            writer.writerow([
                'tareas_id', 'nombre_de_actividad', 'nombre_de_cosecha', 'predio', 'empleado',
                'tiempo_de_actividad', 'notas', 'fecha_planificada', 'fecha_completada',
                'planned', 'numero_de_injertos', 'cantidad_agua_galones', 'cantidad_agua_tiempo',
                'producto_semilla', 'cantidad_siembra', 'unidades_siembra', 'cantidad_cosecha_unidades',
                'cantidad_cosecha_lbs', 'producto_utilizado', 'cantidad_utilizada', 'unidades_fertilizacion'
            ])

            # Writing the data
            for tarea in Tareas.objects.all():
                writer.writerow([
                    tarea.tareas_id,
                    tarea.nombre_de_actividad if tarea.nombre_de_actividad else '',
                    tarea.nombre_de_cosecha if tarea.nombre_de_cosecha else '',
                    tarea.predio if tarea.predio else '',
                    tarea.empleado if tarea.empleado else '',
                    tarea.tiempo_de_actividad,
                    tarea.notas,
                    tarea.fecha_planificada,
                    tarea.fecha_completada,
                    tarea.planned,
                    tarea.numero_de_injertos,
                    tarea.cantidad_agua_galones,
                    tarea.cantidad_agua_tiempo,
                    tarea.producto_semilla if tarea.producto_semilla else '',
                    tarea.cantidad_siembra,
                    tarea.unidades_siembra,
                    tarea.cantidad_cosecha_unidades,
                    tarea.cantidad_cosecha_lbs,
                    tarea.producto_utilizado if tarea.producto_utilizado else '',
                    tarea.cantidad_utilizada,
                    tarea.unidades_fertilizacion
                ])

        self.stdout.write(self.style.SUCCESS('Data successfully exported to tareas_data.csv'))

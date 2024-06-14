from django.shortcuts import render, redirect
from .forms import *
from datetime import timedelta, date, datetime
import io
from django.shortcuts import render
from .models import Lluvias
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.db.models.functions import TruncDay
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Tareas
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

@login_required
def home(request):
    title = 'Welcome to the Pura Energía Estimate Generator!'
    name = request.user

    today = datetime.today()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)

    # Fetch planned activities for the week
    planned_activities = Tareas.objects.filter(
        fecha_planificada__range=[start_week, end_week],
        planned=True  # Assuming you have a 'planned' field to indicate planned activities
    )

    context = {
        "title": title,
        "name": name,
        'planned_activities': planned_activities,
        'start_week': start_week,
        'end_week': end_week
        
    }

    return render(request, 'home.html', context)




def add_lluvia(request):
    if request.method == 'POST':
        form = LluviasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_lluvia')  # Redirect to the list of lluvias
    else:
        form = LluviasForm()
    return render(request, 'add_lluvia.html', {'form': form})


def planned_add_tarea(request):
    if request.method == 'POST':
        form = PlannedTareasForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.planned = True
            tarea.save()

            # Logic to trigger recipes based on the planned task
            planned_activity = tarea.nombre_de_actividad
            planned_cosecha = tarea.nombre_de_cosecha

            matching_recipes = Recetas.objects.filter(
                trigger_actividad_asociado=planned_activity,
                cosecha_asociada=planned_cosecha
            )

            for recipe in matching_recipes:
                dias = recipe.dias
                cadence = recipe.cadence

                # Calculate the fecha_planificada for the first task
                first_fecha_planificada = tarea.fecha_planificada + timedelta(days=dias)

                new_task = Tareas(
                    nombre_de_actividad=recipe.actividades_a_crear,
                    nombre_de_cosecha=planned_cosecha,
                    predio=tarea.predio,
                    fecha_planificada=first_fecha_planificada,  # Use calculated first fecha_planificada
                    planned=True
                )
                new_task.save()

                for i in range(1, cadence):
                    # Calculate the fecha_planificada for the next task by adding `dias` to the previous `new_task.fecha_planificada`
                    new_fecha_planificada = new_task.fecha_planificada + timedelta(days=dias)

                    new_task = Tareas(
                        nombre_de_actividad=recipe.actividades_a_crear,
                        nombre_de_cosecha=planned_cosecha,
                        predio=tarea.predio,
                        fecha_planificada=new_fecha_planificada,  # Use the new fecha_planificada for the next task
                        planned=True
                    )
                    new_task.save()

            return redirect('tareas_list_planned')
    else:
        form = PlannedTareasForm()

    return render(request, 'add_tarea_planned.html', {'form': form})


def tareas_list_done(request):
    tareas = Tareas.objects.all()  # Fetch all Tareas from the database
    return render(request, 'tareas_list_done.html', {'tareas': tareas})


def tareas_list_planned(request):
    tareas = Tareas.objects.filter(planned=True)
    return render(request, 'tareas_list_planned.html', {'tareas': tareas})

def graph_lluvias(request):
    # Find the range of dates in Lluvias data
    start_date = Lluvias.objects.order_by('fecha').first().fecha if Lluvias.objects.exists() else date.today()
    end_date = Lluvias.objects.order_by('-fecha').first().fecha if Lluvias.objects.exists() else date.today()

    # Generate a list of all dates within the range
    total_days = (end_date - start_date).days + 1
    all_dates = [start_date + timedelta(days=day) for day in range(total_days)]

    # Fetch the rainfall data
    lluvias_data = {lluvia.fecha: lluvia.lectura_de_lluvia for lluvia in Lluvias.objects.all()}

    # Prepare data for plotting
    fechas = all_dates
    lecturas = [lluvias_data.get(fecha, 0) for fecha in all_dates]  # Get the rainfall or 0 if not present

    # Create a figure and a bar graph
    fig, ax = plt.subplots()
    ax.bar(fechas, lecturas, color='blue')
    ax.set(xlabel='Fecha', ylabel='Lectura de Lluvia (in)',
           title='Lluvia por Fecha')
    ax.xaxis_date()  # Interpret the x-axis values as dates

    # Save the generated figure to a virtual file
    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)

    # Send buffer in a http response
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    buffer.close()

    return response

def show_graph(request):
    return render(request, 'display_graph.html')


def create_receta(request):
    if request.method == 'POST':
        form = RecetasForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            # Generate receta_nombre
            trigger = receta.trigger_actividad_asociado.nombre_de_actividad
            cosecha = receta.cosecha_asociada.nombre_de_cosecha
            receta.receta_nombre = f"Receta {trigger} {cosecha}"
            receta.save()
            return redirect('create-receta')  # Redirect to a success page or list view
    else:
        form = RecetasForm()
    return render(request, 'create_receta.html', {'form': form})


def tareas_calendar_feed(request):
    planned_tareas = Tareas.objects.filter(planned=True).exclude(fecha_planificada=None)

    events = [
        {
            'title': tarea.nombre_de_actividad.nombre_de_actividad if tarea.nombre_de_actividad else 'Unnamed Activity',  # Get a string property from Actividades            
            'start': tarea.fecha_planificada.isoformat() if tarea.fecha_planificada else None,
            'end': tarea.fecha_planificada.isoformat() if tarea.fecha_planificada else None,
            # Add other FullCalendar event properties as needed
        }
        for tarea in planned_tareas
    ]

    # JsonResponse can handle this list of dictionaries without further modification
    return JsonResponse(events, safe=False, encoder=DjangoJSONEncoder)



from django.db.models import Count, Sum
from django.shortcuts import render
import json
from .models import Tareas
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder


def tareas_dashboard(request):
    # Bar Chart: Count of tasks logged for each predio, broken down by tipo_de_actividad
    tasks_by_predio = Tareas.objects.values('predio', 'nombre_de_actividad__tipo_de_actividad__tipo_de_actividad').annotate(count=Count('tareas_id')).order_by('predio')

    # Bar Chart: Amount of gallons per predio
    gallons_by_predio = Tareas.objects.values('predio').annotate(total_gallons=Sum('cantidad_agua_galones')).order_by('predio')

    # Pie Chart: Amount of tasks by nombre_de_cosecha
    tasks_by_cosecha = Tareas.objects.values('nombre_de_cosecha__nombre_de_cosecha').annotate(count=Count('tareas_id')).order_by('nombre_de_cosecha')

    # Bar Chart: Sum of cantidad_cosecha_unidades by date
    cosecha_by_date = Tareas.objects.annotate(date=TruncDay('fecha_completada')).values('date').annotate(total_units=Sum('cantidad_cosecha_unidades')).order_by('date')

    context = {
        'tasks_by_predio': json.dumps(list(tasks_by_predio), cls=DjangoJSONEncoder),
        'gallons_by_predio': json.dumps(list(gallons_by_predio), cls=DjangoJSONEncoder),
        'tasks_by_cosecha': json.dumps(list(tasks_by_cosecha), cls=DjangoJSONEncoder),
        'cosecha_by_date': json.dumps(list(cosecha_by_date), cls=DjangoJSONEncoder),
    }

    return render(request, 'dashboards.html', context)


def show_task(request):
    tareas_id = request.GET.get('tarea_id')
    tarea_detail = Tareas.objects.get(tareas_id=tareas_id)

    # form = UpdateTaskForm(instance=tarea_id)


    context = {
        "tarea_id": tareas_id,
        "tarea": tarea_detail,
        # "form": form
    }
    return render(request, 'show_task.html', context)

from django.shortcuts import render, redirect, get_object_or_404

# def update_tarea(request, tarea_id):
#     tarea = get_object_or_404(Tareas, tareas_id=tarea_id)  # Using tareas_id from your model
    
#     tipo_actividad_id = None  # Initialize as None to handle cases where no tipo_de_actividad is associated

#     if tarea.nombre_de_actividad and tarea.nombre_de_actividad.tipo_de_actividad:
#         tipo_actividad_id = tarea.nombre_de_actividad.tipo_de_actividad.tipo_act_id  # Correctly accessing the primary key
    
    
#     if request.method == 'POST':
#         form = DynamicTaskForm(request.POST, instance=tarea, tipo_actividad_id=tipo_actividad_id)
#         if form.is_valid():
#             form.save()
#             return redirect('tareas_list_done')  # Redirect to a confirmation or list page
#     else:
#         form = DynamicTaskForm(instance=tarea, tipo_actividad_id=tipo_actividad_id)

#     return render(request, 'update_tarea.html', {'form': form, 'tarea': tarea})


def update_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, tareas_id=tarea_id)
    tipo_actividad_id = tarea.nombre_de_actividad.tipo_de_actividad.tipo_act_id if tarea.nombre_de_actividad else None

    if request.method == 'POST':
        form = DynamicTaskForm(request.POST, instance=tarea, tipo_actividad_id=tipo_actividad_id)
        if form.is_valid():
            saved_tarea = form.save()

            # Update or create custom field data
            info_fields = InfoPorActividad.objects.filter(tipo_de_actividad_id=tipo_actividad_id)
            for field in info_fields:
                field_value = form.cleaned_data.get(field.data_name)
                Data_Por_Tarea.objects.update_or_create(
                    tarea=saved_tarea,
                    info_por_actividad=field,
                    defaults={'value': field_value}
                )

            return redirect('tareas_list_done')
    else:
        form = DynamicTaskForm(instance=tarea, tipo_actividad_id=tipo_actividad_id)

    return render(request, 'update_tarea.html', {'form': form, 'tarea': tarea})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # user_id = form.cleaned_data['id']
            # user_id = instance.id

            # Set the user as not active
            instance.is_active = False
            form.save()
            return redirect('/login')
    
    else:
        form = UserRegisterForm()

        context = {
        "form": form 
    }
    

    return render(request, 'register.html', {'form': form})



def error_404(request, exception):
        return render(request,'404.html')

def error_500(request,  exception):
        return render(request,'500.html')

def error_403(request,  exception):
        return render(request,'404.html')

def error_400(request,  exception):
        return render(request,'404.html')

from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from django.db.models import Sum


class ProductSales(ReportView):

    report_model = Tareas
    date_field = "fecha_completada"
    group_by = "nombre_de_actividad__nombre_de_actividad"

    columns = [
        "nombre_de_actividad",
        ComputationField.create(
            method=Sum, field="value", name="value__sum", verbose_name="Total sold $"
        ),
    ]

    # Charts
    chart_settings = [
        Chart(
            "Total sold $",
            Chart.BAR,
            data_source=["value__sum"],
            title_source=["nombre_de_actividad"],
        ),
    ]

from slick_reporting.views import ReportView
from django.db.models import Count
from slick_reporting.fields import ComputationField

class ActividadesCountReport(ReportView):
    report_model = Tareas
    group_by = "nombre_de_actividad"
    date_field = "fecha_completada"

    
    columns = [
        "nombre_de_actividad",
        ComputationField.create(
            method=Count, field="tareas_id", name="count", verbose_name="Count of Actividades"
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        # You can apply any additional filters or queryset modifications here if needed.
        return queryset



    chart_settings = [
        Chart(
            "Cantidad de Actividades",
            Chart.BAR,
            data_source=["count"],
            title_source=["nombre_de_actividad"],
        )
        
    ]

class GalonesReport(ReportView):
    report_model = Tareas
    date_field = "fecha_completada"
    group_by='predio__nombre_de_predio'
    
    columns = [
        ComputationField.create(
            method=Sum, field="cantidad_agua_galones", name="cantidad_agua_galones_sum"
        ),
        "predio__nombre_de_predio",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter records where planned is False
        queryset = queryset.exclude(fecha_completada__isnull=True, planned=False)
        # You can apply any additional filters or queryset modifications here if needed.
        return queryset
    

    chart_settings = [
        Chart(
            "Cantidad de Galones por Predio",
            Chart.BAR,
            data_source=["cantidad_agua_galones_sum"],
            title_source=["predio__nombre_de_predio"],
        )
        
    ]

from slick_reporting.views import Chart

class CosechaReportUnits(ReportView):
    report_model = Tareas
    date_field = "fecha_completada"
    group_by = "nombre_de_cosecha__nombre_de_cosecha"

    columns = [
        "fecha_completada",
        ComputationField.create(
            method=Sum, field="cantidad_cosecha_unidades", name="cantidad_cosecha_unidades_sum"
        ),
        "nombre_de_cosecha__nombre_de_cosecha"
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter out rows where fecha_completada is null and planned is false
        queryset = queryset.exclude(fecha_completada__isnull=True, planned=False)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    chart_settings = [
        Chart(
            "Cantidad de Cosecha por Fecha",
            Chart.BAR,
            data_source=["cantidad_cosecha_unidades_sum"],
            title_source=["nombre_de_cosecha__nombre_de_cosecha"],
        )
        
    ]


class CosechaReportLbs(ReportView):
    report_model = Tareas
    date_field = "fecha_completada"
    group_by = "nombre_de_cosecha__nombre_de_cosecha"

    columns = [
        "fecha_completada",
        ComputationField.create(
            method=Sum, field="cantidad_cosecha_lbs", name="cantidad_cosecha_libras_sum"
        ),
        "nombre_de_cosecha__nombre_de_cosecha"
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter out rows where fecha_completada is null and planned is false
        queryset = queryset.exclude(fecha_completada__isnull=True, planned=False)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    chart_settings = [
        Chart(
            "Cantidad de Cosecha por Fecha",
            Chart.BAR,
            data_source=["cantidad_cosecha_libras_sum"],
            title_source=["nombre_de_cosecha__nombre_de_cosecha"],
        )
        
    ]




class InjertosReport(ReportView):
    report_model = Tareas
    date_field = "fecha_completada"
    group_by = "nombre_de_cosecha__nombre_de_cosecha"

    columns = [
        "fecha_completada",
        ComputationField.create(
            method=Sum, field="numero_de_injertos", name="numero_de_injertos_sum"
        ),
        "nombre_de_cosecha__nombre_de_cosecha"
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter out rows where fecha_completada is null and planned is false
        queryset = queryset.exclude(fecha_completada__isnull=True, planned=False)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    chart_settings = [
        Chart(
            "Cantidad de Cosecha por Fecha",
            Chart.BAR,
            data_source=["numero_de_injertos_sum"],
            title_source=["nombre_de_cosecha__nombre_de_cosecha"],
        )
        
    ]



def info_repo(request):
    documentos = doc_repo.objects.all() 
    return render(request, 'info_repo.html', {'documentos': documentos})



def calendar_view(request):
    # Fetch events from your Tareas model
    events = Tareas.objects.all()  # You may need to adjust this query to filter events
    
    return render(request, 'calendar.html', {'events': events})



# def document_activity(request):
#     if request.method == 'POST':
#         # Use the same parameter name as used in the GET request
#         form = DynamicTaskForm(request.POST, tipo_actividad_id=request.POST.get('tipo_de_actividad_id'))
#         if form.is_valid():
#             tarea = form.save(commit=False)
#             tarea.save()

#             # Fetch custom fields based on tipo_de_actividad_id from the POST data
#             info_fields = InfoPorActividad.objects.filter(tipo_de_actividad_id=request.POST.get('tipo_de_actividad_id'))
#             for field in info_fields:
#                 Data_Por_Tarea.objects.create(
#                     tarea=tarea,
#                     info_por_actividad=field,
#                     value=form.cleaned_data.get(field.data_name)
#                 )

#             return redirect('tareas_list_done')
#     else:
#         # Fetch the ID from the GET request
#         tipo_actividad_id = request.GET.get('tipo_de_actividad_id')
#         form = DynamicTaskForm(tipo_actividad_id=tipo_actividad_id)

#     return render(request, 'add_tarea_done.html', {'form': form})


# def get_custom_fields(request):
#     tipo_actividad_id = request.GET.get('tipo_de_actividad_id')
#     fields = InfoPorActividad.objects.filter(tipo_de_actividad_id=tipo_actividad_id)
#     html_form = ""

#     for field in fields:
#         if field.data_type == 'string':
#             html_form += f'<div class="form-group"><label>{field.data_name}</label><input type="text" name="{field.data_name}" class="form-control"></div>'
#         elif field.data_type == 'integer':
#             html_form += f'<div class="form-group"><label>{field.data_name}</label><input type="number" name="{field.data_name}" class="form-control"></div>'

#     return JsonResponse({'html_form': html_form})

def select_theme(request):
    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            tipo_de_actividad_id = form.cleaned_data['theme'].tipo_act_id
            return redirect('document_activity', tipo_de_actividad_id=tipo_de_actividad_id)
    else:
        form = ThemeSelectionForm()

    context = {
        'form': form,
        'show_submit': "False",
        'Choose_Tipo_de_Actividad': 'True'
    }
    return render(request, 'select_theme.html', context)



def document_activity(request, tipo_de_actividad_id):
    if request.method == 'POST':
        form = DynamicTaskForm(request.POST, tipo_actividad_id=tipo_de_actividad_id)
        if form.is_valid():
            tarea = form.save()


            # Get all custom fields related to this tipo_de_actividad
            info_fields = InfoPorActividad.objects.filter(tipo_de_actividad_id=tipo_de_actividad_id)
            for field in info_fields:
                # Retrieve the value submitted in the form for this custom field
                field_value = form.cleaned_data.get(field.data_name)

                # Create and save the Data_Por_Tarea instance
                Data_Por_Tarea.objects.create(
                    tarea_asociada=tarea,  # Pass the Tareas instance directly
                    info_por_actividad=field,
                    value=str(field_value)  # Convert the value to string to store in TextField
                )

            return redirect('tareas_list_done')  # Redirect to a success URL or task list
    else:
        form = DynamicTaskForm(tipo_actividad_id=tipo_de_actividad_id)

    return render(request, 'add_tarea_done.html', {'form': form})

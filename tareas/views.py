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
                days_interval = recipe.cadence / recipe.dias if recipe.dias and recipe.cadence else 1

                for i in range(recipe.cadence):
                    fecha_planificada = tarea.fecha_planificada + timedelta(days=i * days_interval)

                    new_task = Tareas(
                        nombre_de_actividad=recipe.actividades_a_crear,
                        nombre_de_cosecha=planned_cosecha,
                        predio=tarea.predio,
                        fecha_planificada=fecha_planificada,
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



# def create_tarea(request):
#     if request.method == 'POST':
#         theme_form = ThemeSelectionForm(request.POST)
#         if theme_form.is_valid():
#             selected_theme = theme_form.cleaned_data['theme']
#             # Logic to determine which task form to show
#             if selected_theme.tipo_de_actividad == 'Siembra':
#                 task_form = SiembraForm(request.POST)
#             elif selected_theme.tipo_de_actividad == 'Cosecha':
#                 task_form = CosechaForm(request.POST)
#             elif selected_theme.tipo_de_actividad == 'Riego':
#                 task_form = RiegoForm(request.POST)
#             elif selected_theme.tipo_de_actividad == 'Injertos':
#                 task_form = InjertosForm(request.POST)
#             if task_form.is_valid():
#                 task_form.save()
#                 return redirect('add_tarea_done')
#     else:
#         theme_form = ThemeSelectionForm()
#         task_form = None  # Initialize with None

#     return render(request, 'add_tarea_done.html', {'theme_form': theme_form, 'task_form': task_form})



# def select_theme(request):
#     if request.method == 'POST':
#         theme_form = ThemeSelectionForm(request.POST)
#         if theme_form.is_valid():
#             selected_theme = theme_form.cleaned_data['theme']
#         return redirect('document_activity', theme_id=selected_theme.tipo_act_id)
    
#     else:
#         theme_form = ThemeSelectionForm()

#     return render(request, 'select_theme.html', {'form': theme_form}, )



def select_theme(request):
    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            tipo_de_actividad_id = form.cleaned_data['theme'].tipo_act_id
            return redirect('/document_activity/?tipo_de_actividad_id={}'.format(tipo_de_actividad_id))
    else:
        form = ThemeSelectionForm()

    context = {
        'form': form,
        'show_submit': "False",
        'Choose_Tipo_de_Actividad': 'True'
    }
    return render(request, 'select_theme.html', context)


# def document_activity(request):
#     activity_form = None
#     theme_id = request.GET.get('theme_id')

#     try:
#         selected_theme = Tipo_de_Actividad.objects.get(tipo_act_id=theme_id)
#         print("Selected Theme ID:", selected_theme.tipo_act_id)  # Debug print
#     except Tipo_de_Actividad.DoesNotExist:
#         return redirect('select_theme')

#     if selected_theme.tipo_act_id == 1:
#         activity_form = SiembraForm(request.POST or None)
#     elif selected_theme.tipo_act_id == 2:
#         activity_form = CosechaForm(request.POST or None)
#     elif selected_theme.tipo_act_id == 3:
#         activity_form = RiegoForm(request.POST or None)
#     elif selected_theme.tipo_act_id == 4:
#         activity_form = InjertosForm(request.POST or None)

#     # Debug print to check which form is selected
#     print("Selected form:", type(activity_form).__name__)

#     if request.method == 'POST' and activity_form and activity_form.is_valid():
#         activity_form.save()
#         return redirect('home.html')  # Replace with your success URL

#     # If no form is matched, or if it's a GET request
#     if activity_form is not None:
#         return render(request, 'documenta_activity/<int:theme_id>/', {'form': activity_form})
#     else:
#         # Handle the case where no form matches the selected theme
#         return HttpResponse("No form available for the selected theme.", status=404)


def document_activity(request):
    activity_form = None
    theme_id = request.GET.get('tipo_de_actividad_id')  # Retrieve from GET parameters

    try:
        selected_theme = Tipo_de_Actividad.objects.get(tipo_act_id=theme_id)
    except Tipo_de_Actividad.DoesNotExist:
        return redirect('select_theme')

    if selected_theme.tipo_act_id == 2:
        activity_form = SiembraForm(request.POST or None)
    elif selected_theme.tipo_act_id == 6:
        activity_form = CosechaForm(request.POST or None)
    elif selected_theme.tipo_act_id == 5:
        activity_form = RiegoForm(request.POST or None)
    elif selected_theme.tipo_act_id == 6:
        activity_form = InjertosForm(request.POST or None)
    elif selected_theme.tipo_act_id == 8:
        activity_form = InjertosForm(request.POST or None)
    else: 
        activity_form = TareasForm(request.POST or None)

    if request.method == 'POST' and activity_form and activity_form.is_valid():
        activity_form.save()
        return redirect('home')  # Use URL name here

    if activity_form is not None:
        context = {
            'form': activity_form,
            'selected_theme_name': selected_theme.tipo_de_actividad,  # Pass the theme name to the template
        }
        return render(request, 'add_tarea_done.html', context)
    else:
        return HttpResponse("No form available for the selected theme.", status=404)






def done_add_tarea(request):
    if request.method == 'POST':
        form = DoneTareasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tareas_list_done')  # Redirect to a page listing all Tareas
    else:
        form = DoneTareasForm()
    return render(request, 'add_tarea_done.html', {'form': form})


# from django.shortcuts import render
# from .models import Lluvias
# from django.db.models.functions import TruncDay
# from django.db.models import Sum
# import json

# def lluvias_chart(request):
#     # Query Lluvias data
#     lluvias_data = list(
#         Lluvias.objects
#         .annotate(day=TruncDay('fecha'))
#         .values('day')
#         .annotate(sum=Sum('lectura_de_lluvia'))
#         .order_by('day')
#     )

#     for entry in lluvias_data:
#         entry['day'] = entry['day'].strftime('%Y-%m-%d')
#         entry['sum'] = float(entry['sum'])  # Ensure the sum is a float

#     context = {
#         'lluvias_data': json.dumps(lluvias_data),
#     }

#     return render(request, 'dashboard.html', context)


from django.http import JsonResponse
from .models import Tareas
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

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
    tarea_id = request.GET.get('tarea_id')
    tarea_detail = Tareas.objects.get(tareas_id=tarea_id)

    # form = UpdateTaskForm(instance=tarea_id)


    context = {
        "tarea_id": tarea_id,
        "tarea": tarea_detail,
        # "form": form
    }
    return render(request, 'show_task.html', context)



def update_tarea(request):
    tarea_id = request.GET.get('tarea_id')
    selected_theme = tarea_id.nombre_de_actividad.tipo_de_actividad

    if selected_theme.tipo_act_id == 2:
        form_class = SiembraForm
    elif selected_theme.tipo_act_id == 6:
        form_class = CosechaForm
    elif selected_theme.tipo_act_id == 5:
        form_class = RiegoForm
    elif selected_theme.tipo_act_id == 8:
        form_class = InjertosForm
    else:
        form_class = TareasForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=tarea_id)
        if form.is_valid():
            form.save()
            return redirect('show_task')  # Redirect to a success page or list
    else:
        form = form_class(instance=tarea_id)

    return render(request,'/update_tarea/?tarea_id={}'.format(tarea_id), {'form': form, 'tarea': tarea_id})


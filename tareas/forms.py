from django import forms
from .models import *

class LluviasForm(forms.ModelForm):
    class Meta:
        model = Lluvias
        fields = ['fecha', 'lectura_de_lluvia', 'descripcion']

class PlannedTareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['predio','nombre_de_cosecha', 'nombre_de_actividad', 'fecha_planificada']
        widgets = {
            'fecha_planificada': forms.DateInput(attrs={'type': 'date'}),
        }


class RecetasForm(forms.ModelForm):
    class Meta:
        model = Recetas
        exclude = ['receta_nombre']  # Exclude receta_nombre from the form



class ThemeSelectionForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Tipo_de_Actividad.objects.all(),
        label="Que quieres documentar?",
        empty_label="Actividades",
        to_field_name="tipo_de_actividad"  # Assuming this is the identifier for your theme
    )


class DoneTareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = '__all__'  # Or specify specific fields if needed
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(DoneTareasForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False



class SiembraForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'cantidad_siembra', 'unidades_siembra', 'tiempo_de_actividad', 'notas']  # Fields relevant to planting
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

def __init__(self, *args, **kwargs):
    super(SiembraForm, self).__init__(*args, **kwargs)
    filtered_activities = Actividades.objects.filter(tipo_de_actividad=2)
    print("Filtered activities: ", filtered_activities)  # Debug print
    self.fields['nombre_de_actividad'].queryset = filtered_activities

class CosechaForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'cantidad_cosecha_unidades', 'cantidad_cosecha_lbs', 'tiempo_de_actividad', 'notas']  # Fields relevant to harvesting
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

def __init__(self, *args, **kwargs):
    super(SiembraForm, self).__init__(*args, **kwargs)
    filtered_activities = Actividades.objects.filter(tipo_de_actividad=6)
    print("Filtered activities: ", filtered_activities)  # Debug print
    self.fields['nombre_de_actividad'].queryset = filtered_activities

class RiegoForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada',  'cantidad_agua_galones', 'cantidad_agua_tiempo', 'tiempo_de_actividad', 'notas'] # Fields relevant to planting

        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }
class InjertosForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada','numero_de_injertos','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['fecha_completada']
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

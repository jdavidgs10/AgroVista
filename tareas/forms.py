from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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



# class DoneTareasForm(forms.ModelForm):
    
#     unidades_siembra_choices = [
#         ('Oz', 'Oz'),
#         ('Libras', 'Libras'),
#     ]
    
#     unidades_siembra = forms.ChoiceField(choices=unidades_siembra_choices, required=True, label='Unidades de Siembra')

#     class Meta:
#         model = Tareas
#         fields = '__all__'  # Or specify specific fields if needed
#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(DoneTareasForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].required = False



# class SiembraForm(forms.ModelForm):
#     unidades_siembra_choices = [
#         ('', ''),
#         ('Unidad', 'Unidad'),
#         ('Libras', 'Libras'),
#     ]
    
#     unidades_siembra = forms.ChoiceField(choices=unidades_siembra_choices, required=True, label='Unidades de Siembra')

#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'cantidad_siembra', 'unidades_siembra', 'tiempo_de_actividad', 'notas']  # Fields relevant to planting
#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#             'cantidad_siembra': forms.TextInput(attrs={'placeholder': 'Solo valores numéricos', 'title': 'Solo valores numéricos'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(SiembraForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

# class CosechaForm(forms.ModelForm):
#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'cantidad_cosecha_unidades', 'cantidad_cosecha_lbs', 'tiempo_de_actividad', 'notas']  # Fields relevant to harvesting
#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(CosechaForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

# class RiegoForm(forms.ModelForm):
#     origen_agua = [
#         ('', ''),
#         ('Pozo', 'Pozo'),
#         ('Quebrada', 'Quebrada'),
#         ('Potable', 'Potable'),

#     ]
    
#     origen_agua = forms.ChoiceField(choices=origen_agua, required=True, label='Origen del Agua')

    
#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'origen_agua', 'cantidad_agua_tiempo', 'cantidad_agua_galones', 'notas'] # Fields relevant to planting

#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(RiegoForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

# class InjertosForm(forms.ModelForm):
#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada','numero_de_injertos','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(InjertosForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

# class PlaguicidaForm(forms.ModelForm):
#     tipo_de_plaguicida = [
#         ('', ''),
#         ('Fungicida', 'Fungicida'),
#         ('Yerbicida', 'Yerbicida'),
#         ('Nematicida', 'Nematicida'),
#         ('Insecticida', 'Insecticida'),

#     ]
#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'tipo_de_plaguicida','producto_utilizado','cantidad_producto','cantidad_agua_plaguicida_utilizada','razon_de_utilizar_producto','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(PlaguicidaForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities


# class AbonamientoForm(forms.ModelForm):
#     unidades_fertilizacion = [
#         ('', ''),
#         ('Oz', 'Oz'),
#         ('Libras', 'Libras'),
#     ]
    
#     unidades_fertilizacion = forms.ChoiceField(choices=unidades_fertilizacion, required=True, label='Unidades de Abono')
    
#     tipo_abono = [
#         ('', ''),
#         ('Foliar', 'Foliar'),
#         ('Granular', 'Gralunar'),

#     ]
    
#     tipo_de_abono = forms.ChoiceField(choices=tipo_abono, required=True, label='Tipo de Abono')


#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada','producto_utilizado','cantidad_producto','unidades_fertilizacion','tipo_de_abono','razon_de_utilizar_producto','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }


#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(AbonamientoForm, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

# class SemillaPrepFrom(forms.ModelForm):
#     tipo_semilla_choices = [
#         ('Oz', 'Oz'),
#         ('Libras', 'Libras'),
#     ]
    
#     tipo_semilla = forms.ChoiceField(choices=tipo_semilla_choices, required=True, label='Tipo de Semilla')

#     class Meta:
#         model = Tareas
#         fields = ['nombre_de_actividad','nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada','tipo_semilla','procedencia_de_semilla','cantidad_principal','cantidad_final','tiempo_de_actividad', 'notas' ]  # Fields relevant to harvesting

#         widgets = {
#             'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id')
#         super(SemillaPrepFrom, self).__init__(*args, **kwargs)
#         filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
#         self.fields['nombre_de_actividad'].queryset = filtered_activities

class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre_de_actividad', 'nombre_de_cosecha', 'predio', 'empleado', 'fecha_completada', 'tiempo_de_actividad', 'notas']
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        tipo_de_actividad_id = kwargs.pop('tipo_de_actividad_id', None)  # Use None as default if 'tipo_de_actividad_id' not provided
        super(TareasForm, self).__init__(*args, **kwargs)
        
        if tipo_de_actividad_id:
            filtered_activities = Actividades.objects.filter(tipo_de_actividad=tipo_de_actividad_id)
            self.fields['nombre_de_actividad'].queryset = filtered_activities
        else:
            # Here, decide on how you want to handle the case when tipo_de_actividad_id is not provided.
            # For example, you can leave the queryset unfiltered or filter it based on some default criteria.
            self.fields['nombre_de_actividad'].queryset = Actividades.objects.all()

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['fecha_completada']
        widgets = {
            'fecha_completada': forms.DateInput(attrs={'type': 'date'}),
        }



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']


class ThemeSelectionForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Tipo_de_Actividad.objects.all(),
        label="Que quieres documentar?",
        empty_label="Actividades",
        to_field_name="tipo_de_actividad"  # Assuming this is the identifier for your theme
    )
class DynamicTaskForm(forms.ModelForm):
    class Meta:
        model = Tareas
        exclude = ['fecha_completada', 'planned']  # Exclude fields not handled by the form directly

    def __init__(self, *args, **kwargs):
        tipo_actividad_id = kwargs.pop('tipo_actividad_id', None)
        super(DynamicTaskForm, self).__init__(*args, **kwargs)

        if tipo_actividad_id:
            info_fields = InfoPorActividad.objects.filter(tipo_de_actividad_id=tipo_actividad_id)
            for field in info_fields:
                field_class = {
                    'string': forms.CharField,
                    'integer': forms.IntegerField,
                    'date': forms.DateField
                }.get(field.data_type, forms.CharField)  # Default to CharField class if type is unknown

                # Now instantiate the field class with the required parameters
                self.fields[field.data_name] = field_class(required=False)
                if field.data_type == 'date':
                    self.fields[field.data_name].widget = forms.widgets.DateInput(attrs={'type': 'date'})

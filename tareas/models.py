from django.db import models


class Empleados(models.Model):
    empleado_id = models.AutoField('Empleado', primary_key=True)
    nombre = models.CharField(max_length=100, null=True)  # String field for the first name
    apellido = models.CharField(max_length=100, null=True)  # String field for the last name
    paga = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Currency field

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Predios(models.Model):
    predio_id = models.AutoField('Predios', primary_key=True)
    nombre_de_predio = models.CharField(max_length=200, null=True)  # String field for the name of the predio
    tipo_de_suelo = models.CharField(max_length=200, null=True)  # String field for the type of soil
    tamaño_de_predio = models.IntegerField(null=True)  # Integer field for the size of the predio in hectares

    def __str__(self):
        return self.nombre_de_predio
    

class Actividades(models.Model):
    actividades_id = models.AutoField('Actividades', primary_key=True)
    nombre_de_actividad = models.CharField(max_length=200, null=True)  # String field for the name of the activity
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description
    tiempo_requerido = models.IntegerField(null=True)  # Integer field for the time required per hectare
    tipo_de_actividad = models.ForeignKey('Tipo_de_Actividad', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre_de_actividad
    
class Cosechas(models.Model):
    cosecha_id = models.AutoField('Cosechas', primary_key=True)
    nombre_de_cosecha = models.CharField(max_length=200, null=True)  # String field for the name of the harvest
    descripcion = models.TextField(null=True)  # Text field for the description

    def __str__(self):
        return self.nombre_de_cosecha
    
class Recetas(models.Model):
    receta_id = models.AutoField('Recetas', primary_key=True)
    receta_nombre=models.TextField(null=True)
    cosecha_asociada = models.ForeignKey('Cosechas', on_delete=models.CASCADE)
    trigger_actividad_asociado = models.ForeignKey('Actividades', related_name='trigger_actividad', on_delete=models.CASCADE)
    actividades_a_crear = models.ForeignKey('Actividades', related_name='actividades_a_crear', on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    cadence = models.IntegerField(null=True)
    dias = models.IntegerField(null=True)

    def __str__(self):
        return f"Receta para {self.cosecha_asociada.nombre_de_cosecha}"

class Tareas(models.Model):
    tareas_id = models.AutoField('tareas', primary_key=True)
    nombre_de_actividad = models.ForeignKey('Actividades', on_delete=models.CASCADE, related_name='actividad_nombre', null=True)
    nombre_de_cosecha = models.ForeignKey('Cosechas', on_delete=models.CASCADE, null=True)
    predio = models.ForeignKey('Predios', on_delete=models.CASCADE, null=True)
    empleado = models.ForeignKey('Empleados', on_delete=models.CASCADE, null=True)
    tiempo_de_actividad = models.IntegerField(null=True)
    notas = models.TextField(null=True)
    fecha_planificada = models.DateField(null=True)
    fecha_completada = models.DateField(null=True, blank=True)
    planned = models.BooleanField(null=True)
    numero_de_injertos = models.IntegerField(null=True)
    cantidad_agua_galones = models.IntegerField(null=True, blank=True)
    cantidad_agua_tiempo = models.IntegerField(null=True)
    origen_agua = models.TextField(null=True)
    cantidad_siembra = models.IntegerField(null=True)
    unidades_siembra = models.CharField(max_length=50, null=True)  # Assuming a predefined set of units
    cantidad_cosecha_unidades = models.IntegerField(null=True)
    cantidad_cosecha_lbs = models.IntegerField(null=True)
    producto_utilizado = models.ForeignKey('Productos', on_delete=models.CASCADE, related_name='producto_utilizado', null=True)
    cantidad_producto = models.IntegerField(null=True)
    cantidad_agua_plaguicida_utilizada=models.IntegerField(null=True)
    razon_de_utilizar_producto=models.TextField(null=True)
    unidades_fertilizacion = models.CharField(max_length=100,null=True)
    id_agroptima=models.IntegerField(null=True)

    # def __str__(self):
    #     return self.nombre_de_actividad



class Lluvias(models.Model):
    lluvias_id = models.AutoField('Lluvias', primary_key=True)
    fecha = models.DateField(null=True)  # Date field for the date of the rainfall
    lectura_de_lluvia = models.FloatField(null=True)  # Integer field for the rainfall measurement
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description

    def __str__(self):
        return f"Lluvia el {self.fecha}"


class Productos(models.Model):
    producto_id = models.AutoField('Productos', primary_key=True)
    nombre_de_producto = models.CharField(max_length=200,null=True)  # String field for the product name
    tipo_de_producto = models.CharField(max_length=200, null=True)  # String field for the product type
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Currency field for the cost
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description

    def __str__(self):
        return self.nombre_de_producto


class Tipo_de_Actividad(models.Model):
    tipo_act_id = models.AutoField('Theme', primary_key=True)
    tipo_de_actividad = models.CharField(max_length=200, null=True)  # String field for the product type
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description
 
    def __str__(self):
        return self.tipo_de_actividad
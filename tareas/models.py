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
        return f"{self.nombre_de_predio}"

    
class Actividades(models.Model):
    actividades_id = models.AutoField('Actividades', primary_key=True)
    nombre_de_actividad = models.CharField(max_length=200, null=True)
    descripcion = models.TextField(null=True, blank=True)
    tiempo_requerido = models.IntegerField(null=True)
    tipo_de_actividad = models.ForeignKey('Tipo_de_Actividad', on_delete=models.CASCADE, null=True)
    tipo_producto_asociado = models.CharField(max_length=200, null=True)  # Store type, not FK

    def get_associated_products(self):
        return Productos.objects.filter(tipo_de_producto=self.tipo_producto_asociado)

    def __str__(self):
        return f"{self.nombre_de_actividad}"
    
    
class Cosechas(models.Model):
    cosecha_id = models.AutoField('Cosechas', primary_key=True)
    nombre_de_cosecha = models.CharField(max_length=200, null=True)  # String field for the name of the harvest
    descripcion = models.TextField(null=True)  # Text field for the description

    def __str__(self):
        return f"{self.nombre_de_cosecha}"
    
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
        return f"  {self.actividades_a_crear.nombre_de_actividad} {self.trigger_actividad_asociado.nombre_de_actividad} {self.cosecha_asociada.nombre_de_cosecha}"


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
    producto_asociado = models.ForeignKey('Productos', on_delete=models.CASCADE, null=True)

    

    def __str__(self):
        return f"{self.nombre_de_actividad}"




class Lluvias(models.Model):
    lluvias_id = models.AutoField('Lluvias', primary_key=True)
    fecha = models.DateField(null=True)  # Date field for the date of the rainfall
    lectura_de_lluvia = models.FloatField(null=True)  # Integer field for the rainfall measurement
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description

    def __str__(self):
        return f"Lluvia el {self.fecha}"


class Productos(models.Model):
    producto_id = models.AutoField('Productos', primary_key=True)
    nombre_de_producto = models.CharField(max_length=200, null=True)
    tipo_de_producto = models.CharField(max_length=200, null=True, unique=True)  # Ensure uniqueness if needed
    plaguicida_check = models.BooleanField(null=True)
    abonamiento_check = models.BooleanField(null=True)
    tipo_de_plaguicida = models.CharField(max_length=200, null=True)
    tipo_de_abonamiento = models.CharField(max_length=200, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self): 
        return f"{self.nombre_de_producto}"



class Tipo_de_Actividad(models.Model):
    tipo_act_id = models.AutoField('Theme', primary_key=True)
    tipo_de_actividad = models.CharField(max_length=200, null=True)  # String field for the product type
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description
 
    def __str__(self):
        return f"{self.tipo_de_actividad}"
    

class doc_repo(models.Model):
    document_id = models.AutoField('Documento', primary_key=True)
    nombre_documento = models.CharField(max_length=200, null=True)  # String field for the product type
    cosecha_asociada = models.ForeignKey('Cosechas', on_delete=models.CASCADE, null=True)
    producto_asociado = models.ForeignKey('Productos', on_delete=models.CASCADE, null=True)
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description
    url_documento = models.URLField(max_length = 200) 

    def __str__(self):
        return f"  {self.nombre_documento} {self.cosecha_asociada.nombre_de_cosecha} {self.producto_asociado.nombre_de_producto}"
    

class Indice_Calor(models.Model):
    indice_id = models.AutoField('Indice', primary_key=True)
    fecha = models.DateField(null=True)  # Date field for the date of the rainfall
    lectura_de_temperatura = models.FloatField(null=True)  # Integer field for the rainfall measurement
    lectura_de_humedad = models.FloatField(null=True)  # Integer field for the rainfall measurement
    indice_de_calor = models.FloatField(null=True)  # Integer field for the rainfall measurement
    descripcion = models.TextField(null=True, blank=True)  # Text field for the description


class InfoPorActividad(models.Model):
    tipo_de_actividad = models.ForeignKey(Tipo_de_Actividad, on_delete=models.CASCADE)
    data_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)  # Could be 'string', 'integer', etc.

    def __str__(self):
        return f"{self.data_name} {self.tipo_de_actividad}"
    

class Data_Por_Tarea(models.Model):
    data_id= models.AutoField('Datos_Tarea', primary_key=True)
    tarea_asociada = models.ForeignKey(Tareas, on_delete=models.CASCADE)
    info_por_actividad = models.ForeignKey(InfoPorActividad, on_delete=models.CASCADE)
    value = models.TextField()  # Store all values as text; interpret based on data_type in InfoPorActividad

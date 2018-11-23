from django.db import models

# Create your models here.

class Empleado(models.Model):
	cedula = models.CharField(max_length=10)
	curp = models.CharField(max_length=18)
	nombre = models.CharField(max_length=255)
	apellidop = models.CharField(max_length=255)
	apellidom = models.CharField(max_length=255)
	sexo = models.CharField(max_length=1, choices=[('m', 'Mujer'), ('h', 'Hombre')])
	fechanac = models.DateField()
	salario = models.FloatField()
	supervisor = models.ForeignKey('Empleado', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return "%s %s %s" % (self.nombre, self.apellidop, self.apellidom)

class Familiar(models.Model):

	PARENTESCOS = [
		('padre', 'Padre'),
		('madre', 'Madre'),
		('hijo', 'Hijo(a)'),
		('esposo', 'Esposo(a)'),
		('nieto', 'Nieto(a)'),
		('hermano', 'Hermano(a)'),
		('abuelo', 'Abuelo(a)'),
		('tio', 'Tio(a)'),
		('primo', 'Primo(a)'),
		('otro', 'Otro'),
	]

	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	curp = models.CharField(max_length=18)
	nombre = models.CharField(max_length=255)
	apellidop = models.CharField(max_length=255)
	apellidom = models.CharField(max_length=255)
	sexo = models.CharField(max_length=1, choices=[('m', 'Mujer'), ('h', 'Hombre')])
	parentesco = models.CharField(max_length=255, choices=PARENTESCOS)

	def __str__(self):
		return "%s %s %s" % (self.nombre, self.apellidop, self.apellidom)	

class Departamento(models.Model):
	nombre = models.CharField(max_length=255)
	
	def __str__(self):
		return self.nombre	

class Proyecto(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

class Maquinaria(models.Model):
	ESTADOS = [
		('1', 'Disponible'),
		('2', 'Ocupado'),
	]
	descripcion = models.CharField(max_length=255)
	estatus = models.CharField(max_length=255, choices=ESTADOS)
	
	def __str__(self):
		return self.descripcion	

class TrabajaEn(models.Model):
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	horas = models.IntegerField()

	def __str__(self):
		return self.empleado

class Jefe(models.Model):
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
	fechaads = models.DateField()

	def __str__(self):
		return self.empleado

class Asignado(models.Model):
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
	fechaads = models.DateField()

	def __str__(self):
		return self.empleado

class mAsignada(models.Model):
	ESTADOS = [
		('1', 'Disponible'),
		('2', 'Ocupado'),
	]
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE)
	fechaa = models.DateField()
	fechae = models.DateField()
	estatus = models.CharField(max_length=255, choices=ESTADOS)

	def __str__(self):
		return self.proyecto

class Estado(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

class Municipio(models.Model):
	nombre = models.CharField(max_length=255)
	
	def __str__(self):
		return self.nombre

class Direccion(models.Model):
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	calle = models.CharField(max_length=255)
	colonia = models.CharField(max_length=255)
	localidad = models.CharField(max_length=255)
	cp = models.CharField(max_length=5)
	estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
	municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.calle

from django.contrib import admin
from .models import Empleado, Familiar, Departamento, Proyecto, Maquinaria, TrabajaEn, Jefe, Asignado, mAsignada, Estado, Municipio, Direccion
# Register your models here.
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'apellidop', 'apellidom')

@admin.register(Familiar)
class FamiliarAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'apellidop', 'apellidom', 'empleado')

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'departamento')

@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
	list_display = ('id', 'descripcion')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
	list_display = ('id', 'calle', 'colonia', 'cp', 'estado', 'municipio')

@admin.register(TrabajaEn)
class TrabajaEnAdmin(admin.ModelAdmin):
	list_display = ('id', 'empleado', 'proyecto', 'horas')

@admin.register(Jefe)
class JefeAdmin(admin.ModelAdmin):
	list_display = ('id', 'empleado', 'departamento', 'fechaads')

@admin.register(Asignado)
class AsignadoAdmin(admin.ModelAdmin):
	list_display = ('id', 'empleado', 'departamento', 'fechaads')

@admin.register(mAsignada)
class mAsignadaAdmin(admin.ModelAdmin):
	list_display = ('id', 'proyecto', 'maquinaria', 'fechaa', 'fechae', 'estatus')
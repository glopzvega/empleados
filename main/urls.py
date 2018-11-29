from django.urls import path
from . import views

app_name = "empl"

urlpatterns = [
    path('', views.empleados, name='index'),
    path('get/', views.obtener_empleados, name='get_empleados'),
    path('detalle/<int:id>/', views.empleado, name='detail_empleado'),
    path('update/<int:id>/', views.update_empleado, name='update_empleado'),
    path('save/', views.save_empleado, name='save_empleado'),
    path('delete/<int:id>/', views.delete_empleado, name='delete_empleado'),

#   Departamentos
    path('departamentos/', views.departamentos, name='deptos'),
    path('departamentos/detalle/<int:id>/', views.departamento, name='detail_depto'),
    path('departamentos/update/<int:id>/', views.update_departamento, name='update_depto'),
    path('departamentos/delete/<int:id>/', views.delete_departamento, name='delete_depto'),
    path('departamentos/save/', views.save_departamento, name='save_depto'),

#   Maquinas
    path('maquinarias/', views.maquinarias, name='maquinas'),
    path('maquinarias/detalle/<int:id>/', views.maquina, name='detail_maquina'),
    path('maquinarias/update/<int:id>/', views.update_maquina, name='update_maquina'),
    path('maquinarias/delete/<int:id>/', views.delete_maquina, name='delete_maquina'),
    path('maquinarias/save/', views.save_maquina, name='save_maquina'),

#   Proyectos
    path('proyectos/', views.proyectos, name='proyectos'),
    path('proyectos/detalle/<int:id>/', views.proyecto, name='detail_proyecto'),
    path('proyectos/update/<int:id>/', views.update_proyecto, name='update_proyecto'),
    path('proyectos/delete/<int:id>/', views.delete_proyecto, name='delete_proyecto'),
    path('proyectos/save/', views.save_proyecto, name='save_proyecto'),

#   TrabajaEn
    path('trabajaen/delete/<int:empleado_id>/', views.remove_trabajaen, name='remove_trabajaen'),

#   Familiar
    path('familiares/delete/<int:empleado_id>/', views.remove_familiar, name='remove_familiar'),

#   Reportes
    path('reporte/', views.reporte, name='reporte'),
    path('reporte/proyectos/', views.reporte_proyectos, name='reporte_proyectos'),
    path('reporte/departamentos/', views.reporte_departamentos, name='reporte_departamentos'),
]
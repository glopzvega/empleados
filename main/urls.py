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
]
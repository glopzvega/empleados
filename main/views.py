from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from . import models as m
import json
# Create your views here.

def response(data):
	if data:
		return JsonResponse({"success" : True, "data" : data})	
	return JsonResponse({"success" : False, "data" : []})	

def empleados(request):
	return render(request, 'main/empleados.html', {})

def empleado(request, id):
	empleado = get_object_or_404(m.Empleado, pk=id)
	empleado.salario = "%.2f" % empleado.salario or 0.00
	empleado.sexo = 'Hombre' if empleado.sexo == 'h' else 'Mujer'
	jsone = {
				"id" : empleado.id,
				"nombre" : empleado.nombre,
				"apellidop" : empleado.apellidop,
				"apellidom" : empleado.apellidom,
				"cedula" : empleado.cedula,
				"curp" : empleado.curp,
				"sexo" : empleado.sexo,
				"fechanac" : str(empleado.fechanac),
				"salario" : empleado.salario,
				"supervisor" : empleado.supervisor or '',
			}
	ctx = {
		"e" : empleado,
		"json" : json.dumps(jsone), 
	}
	return render(request, 'main/empleado.html', ctx)

def update_empleado(request, id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "key" in datajson and "value" in datajson:
			empleado = get_object_or_404(m.Empleado, pk=id)
			setattr(empleado, datajson["key"], datajson["value"])			
			empleado.save()			
			return JsonResponse({"success" : True})
	return JsonResponse({"success" : False})

def save_empleado(request):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "nombre" in datajson and "apellidop" in datajson and "apellidom" in datajson and "cedula" in datajson and "curp" in datajson and "sexo" in datajson and "fechanac" in datajson:
			empleado = m.Empleado.objects.create(**datajson)
			# empleado = m.Empleado(nombre=datajson["nombre"], apellidop=datajson["apellidop"], apellidom=datajson["apellidom"], cedula=datajson["cedula"], curp=datajson["curp"], fechanac=datajson["fechanac"], sexo=datajson["sexo"])
			empleado.save()
			datajson["id"] = empleado.id
			return JsonResponse({"success" : True, "data" : datajson})
	return JsonResponse({"success" : False})

def delete_empleado(request, id):
	empleado = get_object_or_404(m.Empleado, pk=id)
	# empleado.delete();
	return JsonResponse({"success" : True})

def obtener_empleados(request):
	empleados = m.Empleado.objects.all().order_by('nombre')
	data = []
	if empleados:
		for e in empleados:
			data.append({
				"id" : e.id,
				"nombre" : e.nombre,
				"apellidop" : e.apellidop,
				"apellidom" : e.apellidom,
				"cedula" : e.cedula,
				"curp" : e.curp,
				"sexo" : e.sexo,
				"fechanac" : e.fechanac,
				"salario" : "%.2f" % e.salario or 0.00,
				"supervisor" : e.supervisor or '',
			})
	return response(data)
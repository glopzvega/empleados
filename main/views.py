from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from . import models as m
import json
from datetime import datetime
# Create your views here.
def response(data):
	if data:
		return JsonResponse({"success" : True, "data" : data})	
	return JsonResponse({"success" : False, "data" : []})	

def reporte(request):
	empleados = m.Empleado.objects.all()
	for e in empleados:
		e.proyectos = m.TrabajaEn.objects.filter(empleado=e)
		e.departamentos = m.Asignado.objects.filter(empleado=e)
		e.familiares = m.Familiar.objects.filter(empleado=e)
	ctx = {
		"data" : empleados,
		"qty" : len(empleados)
	}
	return render(request, 'main/reporte.html', ctx)

def reporte_proyectos(request):
	proyectos = m.Proyecto.objects.all()
	for p in proyectos:
		p.empleados = m.TrabajaEn.objects.filter(proyecto=p)
		p.maquinas = m.mAsignada.objects.filter(proyecto=p)
	ctx = {
		"data" : proyectos,
		"qty" : len(proyectos)
	}
	return render(request, 'main/reporte_proyectos.html', ctx)

def reporte_departamentos(request):
	departamentos = m.Departamento.objects.all()
	for d in departamentos:
		d.proyectos = m.Proyecto.objects.filter(departamento=d)
		d.empleados = m.Asignado.objects.filter(departamento=d)
		d.jefes = m.Jefe.objects.filter(departamento=d)
	ctx = {
		"data" : departamentos,
		"qty" : len(departamentos)
	}
	return render(request, 'main/reporte_departamentos.html', ctx)

def empleados(request):
	return render(request, 'main/empleados.html', {})

def empleado(request, id):
	empleado = get_object_or_404(m.Empleado, pk=id)
	empleado.salario = "%.2f" % empleado.salario or 0.00
	# empleado.sexo = 'Hombre' if empleado.sexo == 'h' else 'Mujer'
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
				"supervisor" : ""
			}
	if empleado.supervisor:
		sup = empleado.supervisor
		jsone["supervisor"] = {
					"id" : sup.id,
					"full_name" : ("%s %s %s") % (sup.nombre, sup.apellidop, sup.apellidom),
					"nombre" : sup.nombre,
					"apellidop" : sup.apellidop,
					"apellidom" : sup.apellidom,
					"cedula" : sup.cedula,
					"curp" : sup.curp,
					"sexo" : sup.sexo,
					"fechanac" : str(sup.fechanac),
					"salario" : sup.salario,
					"supervisor" : ""
				} 
	familiares = m.Familiar.objects.filter(empleado=empleado).order_by('nombre')
	jsonf = []
	for e in familiares:
		jsonf.append({			
			"id" : e.id,
			"curp" : e.curp,
			"nombre" : e.nombre,
			"apellidop" : e.apellidop,
			"apellidom" : e.apellidom,
			"sexo" : e.sexo,
			"parentesco" : e.parentesco,
			})
	asignados = m.Asignado.objects.filter(empleado=empleado);
	jsona = []
	for e in asignados:
		jsona.append({			
			"id" : e.id,			
			"fechaads" : str(e.fechaads),
			"departamento" : {
					"id" : e.departamento.id,
					"nombre" : e.departamento.nombre,
				}
			})
	trabajaen = m.TrabajaEn.objects.filter(empleado=empleado)
	jsont = []
	for e in trabajaen:
		jsont.append({			
			"id" : e.id,			
			"horas" : e.horas,
			"proyecto" : {
				"id" : e.proyecto.id,
				"nombre" : e.proyecto.nombre,
				# "descripcion" : e.proyecto.descripcion,
				"departamento" : {
						"id" : e.proyecto.departamento.id,
						"nombre" : e.proyecto.departamento.nombre,
					}
				}
			})
	
	deptos = m.Departamento.objects.all().order_by('nombre')
	lista = []
	for d in deptos:
		lista.append({
			"id" : d.id,
			"nombre" : d.nombre,
			})

	proyectos = m.Proyecto.objects.all().order_by('nombre')
	listap = []
	for p in proyectos:
		listap.append({
			"id" : p.id,
			"nombre" : p.nombre,
			})
	empleados = get_empleados_list()
	ctx = {
		"e" : empleado,
		"json" : json.dumps(jsone), 
		"familiares" : json.dumps(jsonf), 
		"departamentos" : json.dumps(jsona), 
		"deptos_list" : json.dumps(lista), 
		"proyectos" : json.dumps(jsont), 
		"proyectos_list" : json.dumps(listap), 
		"empleados_list" : json.dumps(empleados), 
	}
	return render(request, 'main/empleado.html', ctx)

def update_empleado(request, id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		print("#####")
		print(datajson)
		if "key" in datajson and "value" in datajson:
			empleado = get_object_or_404(m.Empleado, pk=id)
			value = datajson["value"]
			if datajson['key'] == 'departamento' and value:
				depto = get_object_or_404(m.Departamento, pk=value)
				asignaciones = m.Asignado.objects.filter(empleado=empleado)
				asignaciones.delete()
				fecha = datetime.now().strftime("%Y-%m-%d")
				nueva = m.Asignado(empleado=empleado, departamento=depto, fechaads=fecha)
				nueva.save()				
				return JsonResponse({"success" : True, "data" : {"departamento" : {"id" : depto.id, "nombre" : depto.nombre}, "fechaads" : fecha }})
			elif datajson['key'] == 'proyecto' and value:
				proyecto = get_object_or_404(m.Proyecto, pk=value)
				trabajaen = m.TrabajaEn.objects.filter(empleado=empleado).filter(proyecto=proyecto)
				if not trabajaen:
					nuevoproyecto = m.TrabajaEn(empleado=empleado, proyecto=proyecto, horas=0)
					nuevoproyecto.save()
					return JsonResponse({"success" : True, "data" : {"id" : nuevoproyecto.id, "horas" : 0, "proyecto" : {"id" : proyecto.id, "nombre" : proyecto.nombre}}})
			elif datajson['key'] == 'familiar' and value:				
				datajson["value"]["empleado_id"] = empleado.id
				familiar = m.Familiar.objects.create(**datajson["value"])				
				# familiar.save()
				return JsonResponse({"success" : True, "data" : datajson["value"]})
			elif datajson['key'] == 'supervisor' and value:				
				sup = get_object_or_404(m.Empleado, pk=int(value))
				empleado.supervisor= sup;
				empleado.save()
				return JsonResponse({"success" : True, "data" : datajson["value"]})			
			else:
				setattr(empleado, datajson["key"], value)			
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
	empleado.delete();
	return JsonResponse({"success" : True})

def get_empleados_list():
	empleados = m.Empleado.objects.all().order_by('nombre')
	data = []
	if empleados:
		for e in empleados:
			supervisor = ""
			if e.supervisor:
				supervisor =  {
					"id" : e.supervisor.id,
					"nombre" : "%s %s %s" % (e.supervisor.nombre, e.supervisor.apellidop, e.supervisor.apellidom),
				}
			data.append({
				"id" : e.id,
				"full_name" : ("%s %s %s") % (e.nombre, e.apellidop, e.apellidom),
				"nombre" : e.nombre,
				"apellidop" : e.apellidop,
				"apellidom" : e.apellidom,
				"cedula" : e.cedula,
				"curp" : e.curp,
				"sexo" : e.sexo,
				"fechanac" : str(e.fechanac),
				"salario" : "%.2f" % e.salario or 0.00,
				"supervisor" : supervisor			
			})
	return data

def obtener_empleados(request):	
	data = get_empleados_list()
	return response(data)

#### DEPARTAMENTOS ####

def departamentos(request):
	data = m.Departamento.objects.all().order_by('nombre')
	lista = []
	for d in data:
		lista.append({
			"id" : d.id,
			"nombre" : d.nombre
			})
	empleados = get_empleados_list()
	print(empleados)
	ctx = {
		"data" : json.dumps(lista),
		"empleados" : json.dumps(empleados)
	}
	return render(request, "main/departamentos.html", ctx)

def departamento(request, id):
	depto = get_object_or_404(m.Departamento, pk=id)
	jsone = {
				"id" : depto.id,
				"nombre" : depto.nombre,
				"jefe" : {}			
			}
	jefes = m.Jefe.objects.filter(departamento=depto)
	if jefes:
		emp = jefes[0].empleado
		jsone["jefe"] = {						
						"id" : jefes[0].empleado.id,
						"nombre" : "%s %s %s" % (emp.nombre, emp.apellidop, emp.apellidom),
						"apellidop" : jefes[0].empleado.apellidop,
						"apellidom" : jefes[0].empleado.apellidom,
						"cedula" : jefes[0].empleado.cedula,
						"curp" : jefes[0].empleado.curp,
						"sexo" : jefes[0].empleado.sexo,
						"fechanac" : str(jefes[0].empleado.fechanac),
						"salario" : "%.2f" % jefes[0].empleado.salario or 0.00,
						# "supervisor" : jefes[0].empleado.supervisor or '',						
					}
	jefes = m.Empleado.objects.all().order_by("nombre")
	jsonj = []
	for j in jefes:
		jsonj.append({
					"id" : j.id,
					"nombre" : "%s %s %s" % (j.nombre, j.apellidop, j.apellidom),					
					"apellidop" : j.apellidop,
					"apellidom" : j.apellidom,
					"cedula" : j.cedula,
					"curp" : j.curp,
					"sexo" : j.sexo,
					"fechanac" : str(j.fechanac),
					"salario" : "%.2f" % j.salario or 0.00,
					# "supervisor" : j.supervisor or '',
				}
			)	

	proyectos = m.Proyecto.objects.filter(departamento=depto)	
	jsonp = []	
	for p in proyectos:
		jsonp.append({
			"id" : p.id,
			"nombre" : p.nombre,
			# "descripcion" : p.descripcion,
			})
	empleados = m.Asignado.objects.filter(departamento=depto)
	jsonm = []
	for e in empleados:
		jsonm.append({
			"id" : e.empleado.id,
			"nombre" : "%s %s %s" % (e.empleado.nombre, e.empleado.apellidop, e.empleado.apellidom),
			# "apellidop" : m.empleado.apellidop,
			# "apellidom" : m.empleado.apellidom,
			})
			
	ctx = {
		"e" : depto,
		"json" : json.dumps(jsone), 
		"jefes" : json.dumps(jsonj), 
		"proyectos" : json.dumps(jsonp), 
		"empleados" : json.dumps(jsonm), 
	}
	return render(request, 'main/departamento.html', ctx)

def update_departamento(request, id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "key" in datajson and "value" in datajson:
			depto = get_object_or_404(m.Departamento, pk=id)
			value = datajson["value"]
			if datajson["key"] == "jefe":
				empleado = get_object_or_404(m.Empleado, pk=int(value))
				jefes = m.Jefe.objects.filter(departamento=depto)
				if jefes:
					jefes[0].empleado = empleado
					jefes[0].fechaads = datetime.now().strftime("%Y-%m-%d")
					jefes[0].save()
			else:
				setattr(depto, datajson["key"], datajson["value"])			
				depto.save()			
			return JsonResponse({"success" : True})
	return JsonResponse({"success" : False})

def delete_departamento(request, id):
	depto = get_object_or_404(m.Departamento, pk=id)
	depto.delete();
	return JsonResponse({"success" : True})

def save_departamento(request):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "nombre" in datajson and datajson["nombre"] and "jefe" in datajson and datajson["jefe"]:
			jefeid = int(datajson['jefe'])
			empleado = get_object_or_404(m.Empleado, pk=jefeid)
			depto = m.Departamento(nombre=datajson['nombre'])
			# depto = m.Departamento.objects.create(**datajson)			
			depto.save()
			if depto.id:
				datajson["id"] = depto.id
				fecha = datetime.now().strftime("%Y-%m-%d")
				newjefe = m.Jefe(departamento=depto, empleado=empleado, fechaads=fecha)
				newjefe.save()
				return JsonResponse({"success" : True, "data" : datajson})
	return JsonResponse({"success" : False})

#### MAQUINARIA ####

def maquinarias(request):
	data = m.Maquinaria.objects.all().order_by('descripcion')
	lista = []
	for d in data:
		lista.append({
			"id" : d.id,
			"nombre" : d.descripcion,
			"estatus" : d.estatus,
			})
	ctx = {
		"data" : json.dumps(lista)
	}
	return render(request, "main/maquinarias.html", ctx)

def maquina(request, id):
	data = get_object_or_404(m.Maquinaria, pk=id)	
	jsone = {
				"id" : data.id,
				"descripcion" : data.descripcion,				
				"estatus" : data.estatus,				
			}
	maquinas = m.mAsignada.objects.filter(maquinaria=data)
	jsonm = []
	if maquinas:
		for e in maquinas:
			jsonm.append({
				"id" : e.proyecto.id,
				"nombre" : e.proyecto.nombre,
				"fecha" : str(e.fechaa),
				})

	proyectos = m.Proyecto.objects.all().order_by('nombre')
	jsonp = []
	if proyectos:
		for e in proyectos:
			jsonp.append({
				"id" : e.id,
				"nombre" : e.nombre,
				})

	ctx = {
		"e" : data,
		"json" : json.dumps(jsone), 
		"proyectos_list" : json.dumps(jsonp), 
		"proyectos" : json.dumps(jsonm), 
	}
	return render(request, 'main/maquinaria.html', ctx)

def update_maquina(request, id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "key" in datajson and "value" in datajson:
			data = get_object_or_404(m.Maquinaria, pk=id)
			value = datajson["value"]
			if datajson["key"] == "proyecto" and value:
				proyecto = get_object_or_404(m.Proyecto, pk=int(value))
				asignadas = m.mAsignada.objects.filter(maquinaria=data)
				asignadas.delete()
				nueva = m.mAsignada(maquinaria=data, proyecto=proyecto)
				nueva.save()				
				return JsonResponse({"success" : True, "data" : {"id" : nueva.proyecto.id, "nombre" : nueva.proyecto.nombre, "fecha" : str(nueva.fechaa)}})
			else:
				setattr(data, datajson["key"], value)			
				data.save()			
			return JsonResponse({"success" : True})
	return JsonResponse({"success" : False})

def delete_maquina(request, id):
	data = get_object_or_404(m.Maquinaria, pk=id)
	data.delete();
	return JsonResponse({"success" : True})

def save_maquina(request):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "descripcion" in datajson and datajson["descripcion"]:
			datajson["estatus"] = "1"
			data = m.Maquinaria.objects.create(**datajson)			
			data.save()
			datajson["id"] = data.id
			datajson["nombre"] = data.descripcion
			return JsonResponse({"success" : True, "data" : datajson})
	return JsonResponse({"success" : False})

#### PROYECTO ####

def proyectos(request):
	data = m.Proyecto.objects.all().order_by('descripcion')
	lista = []
	for d in data:
		lista.append({
			"id" : d.id,
			"nombre" : d.nombre,
			"descripcion" : d.descripcion,
			"departamento" : {
				"id" : d.departamento.id,
				"nombre" : d.departamento.nombre,
			},
			})
	rows = m.Departamento.objects.all().order_by('nombre')
	deptos = []
	for r in rows:
		deptos.append({
			"id" : r.id,
			"nombre" : r.nombre
			})
	ctx = {
		"data" : json.dumps(lista),
		"deptos" : json.dumps(deptos),
	}
	return render(request, "main/proyectos.html", ctx)

def proyecto(request, id):
	data = get_object_or_404(m.Proyecto, pk=id)	
	jsone = {
				"id" : data.id,
				"nombre" : data.nombre,				
				"descripcion" : data.descripcion,				
				"departamento" : {
					"id" : data.departamento.id,
					"nombre" : data.departamento.nombre,
				},				
			}
	deptos = m.Departamento.objects.all().order_by('nombre')
	jsond = []
	for d in deptos:
		obj = {
			"id" : d.id,
			"nombre" : d.nombre
			}
		jsond.append(obj)

	rows = m.TrabajaEn.objects.filter(proyecto=data)
	jsonm = []
	for e in rows:
		jsonm.append({
			"id" : e.empleado.id,
			"nombre" : "%s %s %s" % (e.empleado.nombre, e.empleado.apellidop, e.empleado.apellidom),
			"horas" : e.horas
			})
	ctx = {
		"e" : data,
		"json" : json.dumps(jsone), 
		"deptos" : json.dumps({"data" : jsond}),
		"empleados" : json.dumps(jsonm),
	}
	return render(request, 'main/proyecto.html', ctx)

def update_proyecto(request, id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "key" in datajson and "value" in datajson:
			data = get_object_or_404(m.Proyecto, pk=id)
			value = datajson["value"]
			if datajson["key"] == 'departamento':
				value = get_object_or_404(m.Departamento, pk=value)
			print("###")
			print(datajson["key"])
			print(value)
			setattr(data, datajson["key"], value)
			data.save()			
			return JsonResponse({"success" : True})
	return JsonResponse({"success" : False})

def delete_proyecto(request, id):
	data = get_object_or_404(m.Proyecto, pk=id)
	data.delete();
	return JsonResponse({"success" : True})

def save_proyecto(request):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		if "nombre" in datajson and datajson["nombre"] and "departamento" in datajson and datajson["departamento"]:
			depto = get_object_or_404(m.Departamento, pk=int(datajson["departamento"]))
			data = m.Proyecto(nombre=datajson["nombre"], departamento=depto)
			if "descripcion" in datajson and datajson["descripcion"]:
				data.descripcion = datajson["descripcion"]				
			data.save()			
			datajson["id"] = data.id
			datajson["departamento"] = {"id" : depto.id, "nombre" : depto.nombre}
			return JsonResponse({"success" : True, "data" : datajson})
	return JsonResponse({"success" : False})

def remove_trabajaen(request, empleado_id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		# empleado = get_object_or_404(m.Empleado, pk=empleado_id)
		if 'proyecto_ids' in datajson and datajson['proyecto_ids']:
			for proyecto_id in datajson['proyecto_ids']:
				proyecto = get_object_or_404(m.TrabajaEn, pk=int(proyecto_id))				
				if proyecto:
					proyecto.delete()
					return JsonResponse({"success" : True})	
	return JsonResponse({"success" : False})

def remove_familiar(request, empleado_id):
	if request.method == 'POST':
		datajson = json.loads(request.body.decode('utf-8'))
		# empleado = get_object_or_404(m.Empleado, pk=empleado_id)
		if 'familiar_ids' in datajson and datajson['familiar_ids']:
			for familiar_id in datajson['familiar_ids']:
				familiar = get_object_or_404(m.Familiar, pk=int(familiar_id))				
				if familiar:
					familiar.delete()
					return JsonResponse({"success" : True})	
	return JsonResponse({"success" : False})	
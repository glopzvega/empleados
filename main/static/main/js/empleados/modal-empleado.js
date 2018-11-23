Vue.component('modal-empleado', {
	data : function(){
		return {
			empleado : {
				nombre : "",
				apellidop : "",
				apellidom : "",
				cedula : "",
				curp : "",
				fechanac : "",
				sexo : "h",
				salario : "0",
			}
		}
	},
	props : ['empleados'],
	methods : {
		save : function(){
			let self = this;
			params = {
				method : 'POST',
				credentials : "same-origin",
				headers : {		
					'Accept': 'application/json',			
					'Content-Type': 'application/json',
					'X-CSRFToken': token
				},
				body : JSON.stringify(this.empleado),
			}
			fetch(this.$parent.host + `/save/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					if(res.success)
					{
						alert("Se ha guardado correctamente.");
						self.empleados.push(res.data);
						$("#modal-empleado").modal("hide");
					}					
				})
		}
	},
	template : `
		<form @submit.prevent="save">
		<div id="modal-empleado" class="modal" tabindex="-1" role="dialog">
		  <div class="modal-dialog modal-lg" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
		        <h5 class="modal-title">Nuevo Empleado</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="nombre">Nombre:</label>
		        		<input type="text" id="nombre" v-model="empleado.nombre" class="form-control">
		        		<br />
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-6">
		        		<label for="apellidop">Apellido Paterno:</label>
		        		<input type="text" id="apellidop" v-model="empleado.apellidop" class="form-control">
		        		<br />		        		
		        	</div>
		        	<div class="col-6">
		        		<label for="apellidom">Apellido Materno:</label>
		        		<input type="text" id="apellidom" v-model="empleado.apellidom" class="form-control">
		        		<br />		        		
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-6">
		        		<label for="cedula">Cedula:</label>
		        		<input type="text" id="cedula" v-model="empleado.cedula" class="form-control">
		        		<br />		        		
		        	</div>
		        	<div class="col-6">
		        		<label for="curp">CURP:</label>
		        		<input type="text" id="curp" v-model="empleado.curp" class="form-control">
		        		<br />		        		
		        	</div>
		        </div>
				<div class="row">
		        	<div class="col-6">
		        		<label for="fechanac">Fecha de Nacimiento:</label>
		        		<input type="date" id="fechanac" v-model="empleado.fechanac" class="form-control">
		        		<br />		        		
		        	</div>
		        	<div class="col-6">
						<label for="sexo">Sexo:</label>
		        		<select id="sexo" class="form-control" v-model="empleado.sexo">
							<option value="h">Hombre</option>
							<option value="m">Mujer</option>
		        		</select>
		        		<br />		        		
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-6">
						<label for="salario">Salario $:</label>
		        		<input type="number" step=".1" min="0" class="form-control" v-model="empleado.salario"/>
		        		<br />		        		
		        	</div>        	
		        </div>
		      </div>
		      <div class="modal-footer">
		        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancelar</button>
		        <button type="submit" class="btn btn-primary">Guardar</button>
		      </div>
		    </div>
		  </div>
		</div>
		</form>
	`
})
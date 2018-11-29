Vue.component('modal-depto', {
	data : function(){
		return {
			depto : {
				nombre : "",
				jefe : ""			
			}
		}
	},
	delimiters : ['[[', ']]'],
	props : ['departamentos', 'empleados'],
	methods : {
		save : function(){
			let self = this;

			if(this.nombre == "" || this.jefe == ""){
				alert("Los datos so requeridos");
				return false
			}

			params = {
				method : 'POST',
				credentials : "same-origin",
				headers : {		
					'Accept': 'application/json',			
					'Content-Type': 'application/json',
					'X-CSRFToken': token
				},
				body : JSON.stringify(this.depto),
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
						self.departamentos.push(res.data);
						$("#modal-depto").modal("hide");
					}					
				})
		}
	},
	template : `
		<form @submit.prevent="save">
		<div id="modal-depto" class="modal" tabindex="-1" role="dialog">
		  <div class="modal-dialog" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
		        <h5 class="modal-title">Nuevo Departamento</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="nombre">Nombre:</label>
		        		<input type="text" id="nombre" v-model="depto.nombre" class="form-control">
		        		<br />
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-12">
		        		<label for="jefe">Jefe de Departamento:</label>
		        		<select id="jefe" v-model="depto.jefe" class="form-control">
							<option value="">Seleccione un registro</option>
							<option v-for="e in empleados" :value="e.id">[[ e.nombre ]] [[ e.apellidop ]] [[ e.apellidom ]]</option>
		        		</select>
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
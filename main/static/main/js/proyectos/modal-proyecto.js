Vue.component('modal-proyecto', {
	data : function(){
		return {
			proyecto : {
				nombre : "",
				descripcion : "",
				departamento : ""			
			}
		}
	},
	props : ['departamentos', 'proyectos'],
	methods : {
		save : function(){
			let self = this;

			if(this.proyecto.nombre == "" || this.proyecto.departamento == "")
			{
				alert("Debes de completar los datos")
				return false;
			}

			params = {
				method : 'POST',
				credentials : "same-origin",
				headers : {		
					'Accept': 'application/json',			
					'Content-Type': 'application/json',
					'X-CSRFToken': token
				},
				body : JSON.stringify(this.proyecto),
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
						self.proyectos.push(res.data);
						$("#modal-proyecto").modal("hide");
					}					
				})
		}
	},
	delimiters : ['[[', ']]'],	
	template : `
		<form @submit.prevent="save">
		<div id="modal-proyecto" class="modal" tabindex="-1" role="dialog">
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
		        		<input type="text" id="nombre" v-model="proyecto.nombre" class="form-control">
		        		<br />
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-12">
		        		<label for="descripcion">Descripcion:</label>
		        		<input type="text" id="descripcion" v-model="proyecto.descripcion" class="form-control">
		        		<br />
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-12">
		        		<label for="departamento">Departamento:</label>
		        		<select id="departamento" class="form-control" v-model="proyecto.departamento">
							<option value="">Selecciona un departamento</option>
							<option v-for="depto in departamentos" :value="depto.id">[[ depto.nombre ]]</option>
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
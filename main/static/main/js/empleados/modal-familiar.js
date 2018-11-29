Vue.component('modal-familiar', {
	data : function(){
		return {
			familiar : {
				nombre : "",
				apellidop : "",
				apellidom : "",				
				curp : "",				
				sexo : "h",				
				parentesco : "",				
			},
			parentescos : [
				['padre', 'Padre'],
				['madre', 'Madre'],
				['hijo', 'Hijo(a)'],
				['esposo', 'Esposo(a)'],
				['nieto', 'Nieto(a)'],
				['hermano', 'Hermano(a)'],
				['abuelo', 'Abuelo(a)'],
				['tio', 'Tio(a)'],
				['primo', 'Primo(a)'],
				['otro', 'Otro']
			]
		}
	},
	delimiters : ['[[', ']]'],	
	props : ['empleado', 'familiares'],
	methods : {
		save : function(){
			let self = this;

			if(this.familiar.nombre == "" || this.familiar.apellidop == "" || this.familiar.apellidom == "" || this.familiar.curp == "" || this.familiar.parentesco == "")
			{
				alert("Todos los datos son requeridos");
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
				body : JSON.stringify({'key' : 'familiar', 'value' : this.familiar}),
			}
			fetch(this.$parent.host + `/update/${this.empleado.id}/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					if(res.success)
					{
						alert("Se ha guardado correctamente.");
						self.familiares.push(self.familiar);
						$("#modal-familiar").modal("hide");
					}					
				})
		}
	},
	template : `
		<form @submit.prevent="save">
		<div id="modal-familiar" class="modal" tabindex="-1" role="dialog">
		  <div class="modal-dialog" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
		        <h5 class="modal-title">Nuevo Familiar</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="nombre">Nombre:</label>
		        		<input type="text" id="nombre" v-model="familiar.nombre" class="form-control">
		        		<br />
		        	</div>
		        </div>
		        <div class="row">
		        	<div class="col-6">
		        		<label for="apellidop">Apellido Paterno:</label>
		        		<input type="text" id="apellidop" v-model="familiar.apellidop" class="form-control">
		        		<br />		        		
		        	</div>
		        	<div class="col-6">
		        		<label for="apellidom">Apellido Materno:</label>
		        		<input type="text" id="apellidom" v-model="familiar.apellidom" class="form-control">
		        		<br />		        		
		        	</div>
		        </div>
		        <div class="row">		        	
		        	<div class="col-12">
		        		<label for="curp">CURP:</label>
		        		<input type="text" id="curp" v-model="familiar.curp" class="form-control">
		        		<br />		        		
		        	</div>
		        </div>
				<div class="row">		        	
		        	<div class="col-6">
						<label for="sexo">Sexo:</label>
		        		<select id="sexo" class="form-control" v-model="familiar.sexo">
							<option value="h">Hombre</option>
							<option value="m">Mujer</option>
		        		</select>
		        		<br />		        		
		        	</div>
		        	<div class="col-6">		        		
		        		<label for="parentesco">Parentesco:</label>
						<select id="parentesco" v-model="familiar.parentesco" class="form-control">
							<option value="">Seleccione una opción</option>
							<option v-for="p in parentescos" :value="p[0]">
							[[ p[1] ]]
							</option>
						</select>
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
Vue.component('modal-proyecto', {
	data : function(){
		return {
			select_id : ""
		}
	},
	delimiters : ['[[', ']]'],
	props : ['proyectos', 'maquina', 'masignada'],	
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
				body : JSON.stringify({"key" : "proyecto", "value" : this.select_id.id}),
			}
			fetch(this.$parent.host + `/maquinarias/update/${this.maquina.id}/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					if(res.success)
					{
						alert("Se ha asignado correctamente.");						
						if (res.data)
						{
							// self.masignada = [];
							self.masignada.push(res.data);
							self.masignada.splice(0, 1);
						}

						$("#modal-proyecto").modal("hide");
					}					
				})
		}
	},
	template : `
		<form @submit.prevent="save">
		<div id="modal-proyecto" class="modal" tabindex="-1" role="dialog">
		  <div class="modal-dialog" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
		        <h5 class="modal-title">Nuevo Proyecto</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="nombre">Proyecto:</label>
		        		<select id="proyecto_id" v-model="select_id" class="form-control">
							<option value="">Selecciona el proyecto</option>
							<option v-for="item in proyectos" :value="item">
								[[item.nombre]]
							</option>
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
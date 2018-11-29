Vue.component('modal-maquina', {
	data : function(){
		return {
			maquina : {
				descripcion : "",				
			}
		}
	},
	props : ['maquinas'],
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
				body : JSON.stringify(this.maquina),
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
						self.maquinas.push(res.data);
						$("#modal-maquina").modal("hide");
					}					
				})
		}
	},
	template : `
		<form @submit.prevent="save">
		<div id="modal-maquina" class="modal" tabindex="-1" role="dialog">
		  <div class="modal-dialog" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
		        <h5 class="modal-title">Nueva Máquina</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="descripcion">Nombre:</label>
		        		<input type="text" id="descripcion" v-model="maquina.descripcion" class="form-control">
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
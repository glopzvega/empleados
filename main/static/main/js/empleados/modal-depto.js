Vue.component('modal-depto', {
	data : function(){
		return {
			select_id : {}
		}
	},
	delimiters : ['[[', ']]'],
	props : ['departamentos', 'empleado', 'depto_id'],
	computed : {
		deptoId : {
			get : function(){
				return this.depto_id;
			},
			set : function(newValue){
				this.select_id = newValue;
				console.log(this.select_id);
			}
		},
	},
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
				body : JSON.stringify({"key" : "departamento", "value" : this.select_id.id}),
			}
			fetch(this.$parent.host + `/update/${this.empleado.id}/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					if(res.success)
					{
						alert("Se ha asignado correctamente.");
						self.depto_id.id = res.data.departamento.id
						self.depto_id.nombre = res.data.departamento.nombre
						// self.departamentos[0].departamento = this.select_id;
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
		        <h5 class="modal-title">Nuevo Empleado</h5>
		        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
		          <span aria-hidden="true">&times;</span>
		        </button>
		      </div>
		      <div class="modal-body">
		        <div class="row">
		        	<div class="col-12">
		        		<label for="nombre">Departamento:</label>
		        		<select id="depto_id" v-model="deptoId" class="form-control">
							<option v-for="item in departamentos" :value="item">
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
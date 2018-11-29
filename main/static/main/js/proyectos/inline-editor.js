Vue.component('inline-editor', {
	data : function(){
		return {			
			editables : [],
		}
	},
	delimiters : ['[[', ']]'],
	props : ['clave', 'row'],		
	computed : {
		getData : function(){
			return this.row[this.clave];
		},	
		isVisible : function(){
			let index = this.editables.indexOf(this.clave);
			if (index >= 0)
				return true;
			return false;
		},		
	},
	methods : {
		editar : function(){
			let self = this;
			let index = this.editables.indexOf(this.clave);
			if (index < 0)
				this.editables.push(this.clave);
			setTimeout(function(){
				document.getElementById(self.clave).select();
				$('[data-toggle="tooltip"]').tooltip()
			}, 100)		
		},		
		cancel : function(){
			let index = this.editables.indexOf(this.clave);
			this.editables.splice(index, 1);
			$('[data-toggle="tooltip"]').tooltip('hide')
		},
		save : function(e){	
			let self = this;
			let clave = this.clave;
			let valor = this.row[this.clave];

			if(valor == "")
			{
				alert("Debe introducir un valor.")					
				document.getElementById(clave).focus();
				console.log(e)
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
				body : JSON.stringify({ key : clave,  value : valor }),
			}
			fetch(this.$parent.host + `/update/${this.row.id}/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					let index = this.editables.indexOf(this.clave);
					this.editables.splice(index, 1);
					$('[data-toggle="tooltip"]').tooltip('hide')
				})
		}
	},
	template : `
		<div>
			<div class="row" v-show="!isVisible">
				<div class="col-12">
					<h4 @click="editar" class="editable text-muted"> 
					[[ getData ]] </h4>
				</div>
			</div>
			<div class="row" v-if="isVisible">
				<div class="col-10">
					<input @keyup.enter="save" @keyup.esc="cancel" title="Presiona Enter para guardar" data-toggle="tooltip" :id="clave" type="text" class="form-control" v-model="row[clave]">
				</div>
				<div class="col-2">
					<a @click.prevent="save" href="" class="btn btn-success" title="Guardar" data-toggle="tooltip">
						<i class="fas fa-check"></i>
					</a>
					<a @click.prevent="cancel" href="" class="btn btn-secondary" title="Cancelar" data-toggle="tooltip">
						<i class="fas fa-ban"></i>
					</a>
				</div>									
			</div>
			<br>
		</div>
	`
})
Vue.component('inline-editor', {
	data : function(){
		return {			
			editables : [],
			original : '',
		}
	},
	delimiters : ['[[', ']]'],
	// props : ['clave', 'row', 'tipo', 'input'],
	props : {
		row : Object,
		clave : String,
		string : {
			type : String,
			default : '',
		},
		text : {
			type : String,
			default : '',
		},
		field : {
			type : String,
			default : '',
		},
		tipo : {
			type : String,
			default : 'h4'
		},
		input : {
			type : String,
			default : 'text',
		},
		options : Array,		
	},	
	computed : {
		getData : function(){
			if(this.string != '')
			{
				return this.string;
			}
			else if(this.field != '')
			{				
				console.log(this.row[this.clave][this.field])
				return this.row[this.clave][this.field]
			}
			return this.row[this.clave];
		},
		isVisible : function(){
			let index = this.editables.indexOf(this.clave);
			if (index >= 0)
				return true;
			return false;
		},	
		getUrl : function(){
			return this.$parent.host + this.$parent.module;
		}	
	},
	methods : {
		getTipo : function(tipo)
		{
			return this.tipo == tipo;
		},
		getInput : function(input)
		{
			return this.input == input;
		},
		getOption : function(id)
		{
			let self = this;
			let option = '';
			this.options.forEach(function(value){
				if(value.id == id)
				{
					option = value.nombre;
					// if(self.text != '')
					// 	option = self.text;
					return false;
				}
			})
			return option;
		},
		getOptionSelected : function(){
			console.log("########")
			console.log(this.row[this.clave]["id"])
			return this.row[this.clave]["id"];
		},
		editar : function(){
			let self = this;
			this.original = this.row[this.clave];
			let index = this.editables.indexOf(this.clave);
			if (index < 0)
				this.editables.push(this.clave);
			setTimeout(function(){
				if(self.input != 'select' && self.input != 'select_list')
				{
					document.getElementById(self.clave).select();
				}
				// else if(self.input == 'select')
				// {
				// 	let ideselect = self.row[self.clave]["id"];
				// 	// document.getElementById(self.clave).val(ideselect);	
				// }
				$('[data-toggle="tooltip"]').tooltip()
			}, 100)		
		},		
		cancel : function(){
			let index = this.editables.indexOf(this.clave);
			this.row[this.clave] = this.original;
			this.editables.splice(index, 1);
			$('[data-toggle="tooltip"]').tooltip('hide')
		},
		save : function(e){	
			let self = this;
			let clave = this.clave;
			let valor = this.row[this.clave];

			if(this.input == 'select')
			{
				valor = this.row[this.clave]["id"];
			}

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
			fetch(this.getUrl + `/update/${this.row.id}/`, params)
				.then(function(res){
					return res.json();
				})
				.then(function(res){
					console.log(res)
					let index = self.editables.indexOf(self.clave);
					self.editables.splice(index, 1);
					$('[data-toggle="tooltip"]').tooltip('hide')
				})
		}
	},
	template : `
		<div>
			<div class="row" v-show="!isVisible">
				<div class="col-12">
					<h4 @click="editar" v-if="getTipo('h4')" class="editable text-muted"> 
					[[ getData ]] </h4>					
					<p @click="editar" v-if="getTipo('p')" class="editable text-muted"> 
					[[ getData ]] </p>
				</div>
			</div>
			<div class="row" v-if="isVisible">
				<div class="col-10">
					<input :id="clave" v-model="row[clave]" v-if="getInput('text')" @keyup.enter="save" @keyup.esc="cancel" title="Presiona Enter para guardar" data-toggle="tooltip" type="text" class="form-control">
					<input :id="clave" v-model="row[clave]" v-if="getInput('number')" @keyup.enter="save" @keyup.esc="cancel" title="Presiona Enter para guardar" data-toggle="tooltip" type="number" class="form-control">
					<input :id="clave" v-model="row[clave]" v-if="getInput('date')" @keyup.enter="save" @keyup.esc="cancel" title="Presiona Enter para guardar" data-toggle="tooltip" type="date" class="form-control">
					<textarea :id="clave" v-if="getInput('textarea')" rows="5" class="form-control" v-model="row[clave]"></textarea>					
					
					<select :id="clave" v-model="row[clave]" v-if="getInput('select')" @keyup.enter="save" @keyup.esc="cancel" class="form-control">
						<option v-for="o in options" :value="o">[[ getOption(o.id) ]]</option>
					</select>					
					
					<select :id="clave" v-model="row[clave]" v-if="getInput('select_list')" @keyup.enter="save" @keyup.esc="cancel" class="form-control">
						<option v-for="o in options" :value="o.id">[[ getOption(o.id) ]]</option>
					</select>
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
(function() {
  var app = angular.module('myApp');
	
  
  
  app.controller('TodoController', ['$http', '$interval', function($http, $interval){
	var t = this;
	this.todos = [];
	this.newTodo = {};
	this.selectedTodo = {};
	
	this.reload = function(){
		$http.get("/todo-json").success(function(data){
			t.todos = data;
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};
	//initialize
	this.reload();
	
	//periodically update elements
    // $interval(t.reload, 3000);
	

	this.addTodo = function(){
		$('#add_todo_madal').modal('hide');
		$http.post("/todo-json", t.newTodo).success(function(data){
			t.todos.push(data);
			t.newTodo = {};
			$.toaster({ priority : 'success', title : 'Success', message : 'Todo added'});
		}).error(function(data) {
			$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	this.deleteTodo = function(todo){
		$http.delete("/todo-json/" + todo.id).success(function(data){
			t.todos.splice(t.todos.indexOf(todo),1); //delete an item in array
			$.toaster({ priority : 'success', title : 'Success', message : 'Todo deleted'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	//setup attributes in modal 
	this.showUpdateTodo = function(todo){
		t.selectedTodo = jQuery.extend(true, {}, todo); //clone object
		$('#update_todo_madal').modal('show');
	};
	
	this.updateTodo = function(){
		$('#update_todo_madal').modal('hide');
		$http.put("/todo-json/" + t.selectedTodo.id, t.selectedTodo).success(function(data){
			for (var i = 0; i < t.todos.length; i++){
			    if (t.todos[i].id == t.selectedTodo.id)
			        t.todos[i] = data; //replace an item in array
			}
			$.toaster({ priority : 'success', title : 'Success', message : 'Todo updated'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
  }]);

})();

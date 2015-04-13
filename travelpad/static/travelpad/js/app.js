(function() {
  var app = angular.module('itinerary', []);
	
  app.config(['$httpProvider', function($httpProvider) {
	  //set csrftoken
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);	
  	
  app.controller('ParticipantController', ['$http', function($http){
	var ctrl = this;
	ctrl.participants = [];
	$http.get("/participant-json").success(function(data){
		ctrl.participants = data;
	});
	
	
  }]);
  
  app.controller('TodoController', ['$http', function($http){
	var ctrl = this;
	ctrl.todos = [];
	ctrl.newTodo = {};
	ctrl.selectedTodo = {};
	$http.get("/todo-json").success(function(data){
		ctrl.todos = data;
	}).error(function(data) {
    	bootstrap_alert.error(data.errors);
    });

	this.addTodo = function(){
		$('#add_todo_madal').modal('hide');
		$http.post("/todo-json", ctrl.newTodo).success(function(data){
			ctrl.todos.push(data);
			ctrl.newTodo = {};
			bootstrap_alert.success("Todo added");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
	this.deleteTodo = function(todo){
		$http.delete("/todo-json/" + todo.id).success(function(data){
			ctrl.todos.splice(ctrl.todos.indexOf(todo),1); //delete an item in array
			bootstrap_alert.success("Todo deleted");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
	this.showUpdateTodo = function(todo){
		ctrl.selectedTodo = jQuery.extend(true, {}, todo);
		$('#update_todo_madal').modal('show');
	};
	
	this.updateTodo = function(){
		// console.log('updateTodo');
		$('#update_todo_madal').modal('hide');
		$http.put("/todo-json/" + ctrl.selectedTodo.id, ctrl.selectedTodo).success(function(data){
			// ctrl.todos[ctrl.selectedIdx] = data; //replace an item in array
			for (var i = 0; i < ctrl.todos.length; i++){
			    if (ctrl.todos[i].id == ctrl.selectedTodo.id)
			        ctrl.todos[i] = data;
			}
			bootstrap_alert.success("Todo updated");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
  }]);

})();

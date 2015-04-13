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
	$http.get("/todo-json").success(function(data){
		ctrl.todos = data;
	}).error(function(data) {
    	bootstrap_alert.error(data.errors);
    });

	this.addTodo = function(){
		$('#add_todo_madal').modal('hide');
		$http.post("/todo-json", ctrl.newTodo).success(function(data){
			ctrl.todos.push(ctrl.newTodo);
			ctrl.newTodo = {};
			bootstrap_alert.success("Todo added");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
	this.deleteTodo = function(index, id){
		$http.delete("/todo-json/" + id).success(function(data){
			ctrl.todos.splice(index,1); //delete an item in array
			bootstrap_alert.success("Todo deleted");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
	this.showUpdateTodo = function(index, todo){
		ctrl.newTodo = todo;
		ctrl.newTodo.index = index;
		$('#update_todo_madal').modal('show');
	};
	
	this.updateTodo = function(index, id){
		$('#update_todo_madal').modal('hide');
		$http.put("/todo-json/" + id, ctrl.newTodo).success(function(data){
			ctrl.todos[index] = newTodo; //replace an item in array
			bootstrap_alert.success("Todo updated");
		}).error(function(data) {
    		bootstrap_alert.error(data.errors);
    	});
	};
	
  }]);

})();

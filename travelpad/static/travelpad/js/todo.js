(function() {
  var app = angular.module('itinerary-todo', []);

  app.controller('TodoController', ['$http', function($http){
	var ctrl = this;
	ctrl.todos = [{"task":"test"}];
	ctrl.newTodo = {};
	ctrl.test = "test"
	console.log(ctrl.todos);
	// $http.get("/todo-json").success(function(data){
// 		ctrl.todos = data;
// 		console.log(ctrl.todos);
// 		console.log(ctrl.todos[0].task);
// 	});

	this.addTodo = function(product){
		$http.post("/todo-json").success(function(data){
			ctrl.todos.push(ctrl.newTodo);
			ctrl.newTodo = {};
		});
	};
	
	this.deleteTodo = function(product){
		// $http.delete("/todo-json").success(function(data){
// 			ctrl.todos.push(ctrl.newTodo);
// 			ctrl.newTodo = {};
// 		});
	};
	
  }]);

})();
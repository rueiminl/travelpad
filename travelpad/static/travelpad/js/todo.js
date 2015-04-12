(function() {
  var app = angular.module('itinerary-todo', []);

  app.controller('TodoController', ['$http', function($http){
	var ctrl = this;
	ctrl.todos = [];
	ctrl.newTodo = {};
	
	$http.get("/todo-json").success(function(data){
		ctrl.todos = data;
	});

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
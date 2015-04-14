(function() {
  var app = angular.module('myApp');
	
  
  
  app.controller('CostController', ['$http', '$interval', function($http, $interval){
	var t = this;
	this.costs = [];
	
	this.reload = function(){
		$http.get("/costs").success(function(data){
			t.costs = data;
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};
	//initialize
	this.reload();
	
	//periodically update elements
    $interval(t.reload, 3000);
  }]);

})();

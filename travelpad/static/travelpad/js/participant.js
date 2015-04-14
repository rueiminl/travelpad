(function() {
  var app = angular.module('myApp');
	
  	
  app.controller('ParticipantController', ['$http', function($http){
	var t = this;
	this.participants = [];
	$http.get("/participant-json").success(function(data){
		t.participants = data;
	});
	
  }]);
 

})();

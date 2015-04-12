(function() {
  var app = angular.module('itinerary', ['itinerary-todo']);

  app.controller('ParticipantController', function(){
    this.products = gems;
  });
  
  app.controller('ItineraryController', ['$http', function(){
	var itinerary = this;
	itinerary.participants = [];
	$http.get("/participant").success(function(data){
		itinerary.participants = data;
	});
	
	
  }]);

})();

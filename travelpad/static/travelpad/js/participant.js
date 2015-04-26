(function() {
  var app = angular.module('myApp');  	
	
  app.controller('ParticipantController', ['$http', function($http){
	var p = this;
	this.participants = [];
	this.postData = {};
	this.reload = function() {
		$http.get("/participant-json").success(function(data){
			p.participants = data;
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};

	this.getuser = function(){
		$http.get("/costs-user").success(function(data){
			p.user = data;
		})
	};

	this.getuser();

	this.invite = function() {
		$http({
			url: "/participant-json",
			method: "POST",
			data: $.param({username:$('#username').val(), type:'add'}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data){
			if (data.success == "false") {
				$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
			}
			else {
				p.participants.push(data.participant)
			}
		});
	};
	this.delete = function(username) {
		if (confirm("Are you sure you want to kick out the user from this itinerary? It might break his/her heart...") == false)
			return;
		$http({
			url: "/participant-json",
			method: "POST",
			data: $.param({username:username, type:'del'}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data){
			if (data.success == "false") {
				$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
			}
			else {
				for (i in p.participants) {
					if (p.participants[i].username == username) {
						p.participants.splice(i, 1);
						break;
					}
				}
			}
		});
	};
	// initialize
	this.reload();
  }]);
})();

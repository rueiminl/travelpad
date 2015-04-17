(function() {
  var app = angular.module('myApp');
	
  
  
  app.controller('CostController', ['$http', '$interval', function($http, $interval){
	var t = this;
	this.costs = [];
	
	this.reload = function(){
		$http.get("/costs").success(function(data){
			t.costs = data;
            console.log(data[0].owner.id);
            console.log(data[0].participant[0]);
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};
	//initialize
	this.reload();
	
	//periodically update elements
    //$interval(t.reload, 3000);
    
    //setup attributes in modal 
	this.editCost = function(cost){
		t.selectedCost = jQuery.extend(true, {}, cost); //clone object
		$('#edit_cost_madal').modal('show');
	};
    
    this.updateCost = function(){
        $('#edit_cost_madal').modal('hide');
        $http.put("/costs/" + t.selectedCost.id, t.selectedCost).success(function(data){
            for (var i = 0; i < t.costs.length; i++){
                if (t.costs[i].id == t.selectedCost.id)
                    t.costs[i] = data; //replace an item in array
            }
            $.toaster({ priority : 'success', title : 'Success', message : 'Cost updated'});
        }).error(function(data) {
            $.toaster({ priority : 'danger', title : 'Error', message : data.errors});
        });
    };
  }]);

})();

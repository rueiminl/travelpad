(function() {
  var app = angular.module('myApp');

  
  
  app.controller('CostController', ['$http', '$interval', '$scope', function($http, $interval, $scope){
	var t = this;
	this.costs = [];
    this.newCost = {};
    this.selectedCost = {};
    this.calculating = true;
	
	this.reload = function(){
		$http.get("/costs").success(function(data){
			t.costs = data;
            t.updateMyCost();
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};
    
    this.getuser = function(){
		$http.get("/costs-user").success(function(data){
			t.user = data;
		})
	};
	//initialize
	this.getuser();
    this.reload();
	
	//periodically update elements
    $interval(t.reload, 5000);
    
    //setup attributes in modal 
    this.addCost = function(){
		$('#add_cost_madal').modal('hide');
		$http.post("/costs", t.newCost).success(function(data){
			t.costs.push(data);
			t.newCost = {};
			$.toaster({ priority : 'success', title : 'Success', message : 'Expense added'});
		}).error(function(data) {
			$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
        this.reload();
        $scope.addCostForm.$setPristine();
	};
    
	this.editCost = function(cost){
		t.selectedCost = jQuery.extend(true, {}, cost); //clone object
		$('#edit_cost_madal').modal('show');
	};
    
    this.deleteCost = function(cost){
        $('#edit_cost_madal').modal('hide');
        if (confirm("Are you sure you want to delete this event?") == true){
            $http.delete("/costs/" + t.selectedCost.id).success(function(data){
                t.costs.splice(t.costs.indexOf(cost),1); //delete an item in array
                $.toaster({ priority : 'success', title : 'Success', message : 'Cost deleted'});
            }).error(function(data) {
                $.toaster({ priority : 'danger', title : 'Error', message : data.errors});
            });
        }
        this.reload()
	};
    
    this.backcolor = function(cost){
        if (cost.status == "Paid")
            return "paid";
        else if (cost.owner && t.user && cost.owner.username==t.user.username)
            return "unpaid";
        else{
            for (var i = 0; i < cost.participant.length; i++){
                if (t.user.username==cost.participant[i].username)
                    return "unpaid";
            }
            return "normal";
        }
	};
    
    this.updateCost = function(){
        $('#edit_cost_madal').modal('hide');
        $http.put("/costs/" + t.selectedCost.id, t.selectedCost).success(function(data){
            for (var i = 0; i < t.costs.length; i++){
                if (t.costs[i].id == t.selectedCost.id)
                    t.costs[i] = data; //replace an item in array
            }
            $.toaster({ priority : 'success', title : 'Success', message : 'Expense updated'});
        }).error(function(data) {
            $.toaster({ priority : 'danger', title : 'Error', message : data.errors});
        });
        this.reload()
    };
    
    this.updateMyCost = function(){
        if (t.user && t.costs){
            t.myCost = 0;
            t.unpaidCost = 0;
            t.receiveCost = 0;
            for (var i = 0; i < t.costs.length; i++){
                if (t.user.username == t.costs[i].owner.username && t.costs[i].status == "Unpaid")
                    t.receiveCost += t.costs[i].amount;
                for (var j = 0; j < t.costs[i].participant.length; j++){
                    if (t.user.username == t.costs[i].participant[j].username){
                        if (t.costs[i].isall == false){
                            t.myCost += t.costs[i].amount;
                            if (t.costs[i].status == "Unpaid"){
                                t.unpaidCost += t.costs[i].amount;
                            }
                        }
                        else{
                            t.myCost += t.costs[i].amount/t.costs[i].participant.length;
                            if (t.costs[i].status == "Unpaid"){
                                t.unpaidCost += t.costs[i].amount/t.costs[i].participant.length;
                            }
                        }
                        break;
                    }
                }
            }
            t.calculating = false;
        }
        else{
            t.calculating = true;
        }
    };

  }]);
})();

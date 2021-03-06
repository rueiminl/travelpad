(function() {
  var app = angular.module('myApp');
	
  app.controller('MessageController', ['$http', '$interval', '$scope', function($http, $interval, $scope){
	var t = this;
	this.messages = [];
	this.newMessage = {};
	
	this.reload = function(){
		$http.get("/message-json").success(function(data){
			// t.messages = data;
			var idMap = t.messages.map(function(message){
				return message.id;
			});
			for (var i = 0; i < data.length; i++){
				if(idMap.indexOf(data[i].id) == -1){
					data[i].newReply = {related_message: data[i].id};
					t.messages.push(data[i]);
				}else{
					for (var j = 0; j < t.messages.length; j++){
					    if (t.messages[j].id == data[i].id && t.messages[j].timestamp < data[i].timestamp){
					    	data[i].newReply = {related_message: data[i].id};
							t.messages[j] = data[i]; //replace an item in array
					    }
					}
				}
			}
			// for (var i = 0; i < t.messages.length; i++){
// 				t.messages[i].newReply = {related_message: t.messages[i].id};
// 			}
			// console.log(data);
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
	};
	//initialize
	this.reload();
	
	
	//periodically update elements
    $interval(t.reload, 3000);
	

	this.addMessage = function(){
		$http.post("/message-json", t.newMessage).success(function(data){
			data.newReply = {related_message: data.id};
			data.editMode = false;
			t.messages.push(data);
			t.newMessage = {};
			$.toaster({ priority : 'success', title : 'Success', message : 'Message posted.'});
		}).error(function(data) {
			$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	this.deleteMessage = function(message){
		$http.delete("/message-json/" + message.id).success(function(data){
			t.messages.splice(t.messages.indexOf(message),1); //delete an item in array
			$.toaster({ priority : 'success', title : 'Success', message : 'Message deleted'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	this.toggleEditMessage = function(message){
		message.editMode = !message.editMode;
		if(message.editMode){
			message.editContent = message.content;
		}
	}
	
	this.updateMessage = function(message){
		message.editMode = false;
		$http.put("/message-json/" + message.id, message).success(function(data){
			message.content = message.editContent;
			$.toaster({ priority : 'success', title : 'Success', message : 'Message updated'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	/**
	* Reply
	*/
	this.addReply = function(message){
		// message.newReply.related_message = message.id;
		console.log(message.newReply);
		$http.post("/reply-json", message.newReply).success(function(data){
			message.replies.push(data);
			message.newReply = {related_message: message.id}; //reset
			// t.newReply = {};
			$.toaster({ priority : 'success', title : 'Success', message : 'Reply posted.'});
		}).error(function(data) {
			$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	this.deleteReply = function(message, reply){
		$http.delete("/reply-json/" + reply.id).success(function(data){
			message.replies.splice(message.replies.indexOf(reply),1); //delete an item in array
			message.newReply = {related_message: message.id}; //reset
			$.toaster({ priority : 'success', title : 'Success', message : 'Reply deleted'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	
	this.toggleEditReply = function(reply){
		reply.editMode = !reply.editMode;
		if(reply.editMode){
			reply.editContent = reply.content;
		}
	}
	
	this.updateReply = function(reply){
		reply.editMode = false;
		$http.put("/reply-json/" + reply.id, reply).success(function(data){
			reply.content = reply.editContent;
			$.toaster({ priority : 'success', title : 'Success', message : 'Reply updated'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	//TODO: not working
	$scope.reset = function() {
		  $scope.form.$setPristine();
	}
	
	
	
  }]);
  	
	//ref: JavaScript Pretty Date, http://ejohn.org/blog/javascript-pretty-date/
	app.filter('prettyDate', function() {
		return function(time) {
			var date = new Date((time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
				diff = (((new Date()).getTime() - date.getTime()) / 1000),
				day_diff = Math.floor(diff / 86400);
			
				if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
					return;
			
				return day_diff == 0 && (
				diff < 60 && "just now" ||
				diff < 120 && "1 minute ago" ||
				diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
				diff < 7200 && "1 hour ago" ||
				diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
			day_diff == 1 && "Yesterday" ||
			day_diff < 7 && day_diff + " days ago" ||
			day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
		}

		// // If jQuery is included in the page, adds a jQuery plugin to handle it as well
// 		if ( typeof jQuery != "undefined" )
// 			jQuery.fn.prettyDate = function(){
// 				return this.each(function(){
// 					var date = prettyDate(this.title);
// 					if ( date )
// 						jQuery(this).text( date );
// 				});
//   			};
	});
	
  app.directive('time', 
    [
      '$timeout',
      '$filter',
      function($timeout, $filter) {

        return function(scope, element, attrs) {
          var time = attrs.time;
          var intervalLength = 1000 * 60; // 60 seconds
          var filter = $filter('prettyDate');

          function updateTime() {
            element.text(filter(time));
          }

          function updateLater() {
            timeoutId = $timeout(function() {
              updateTime();
              updateLater();
            }, intervalLength);
          }

          element.bind('$destroy', function() {
            $timeout.cancel(timeoutId);
          });

          updateTime();
          updateLater();
        };

      }  
    ]
  );

})();

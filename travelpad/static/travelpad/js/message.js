(function() {
  var app = angular.module('myApp');
	
  app.controller('MessageController', ['$http', '$interval', function($http, $interval){
	var t = this;
	this.messages = [];
	this.newMessage = {};
	// this.newReply = {};
	
	this.reload = function(){
		$http.get("/message-json").success(function(data){
			t.messages = data;
			for (var i = 0; i < t.messages.length; i++){
				t.messages[i].newReply = {related_message: t.messages[i].id};
			}
			console.log(data);
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
	
	this.addReply = function(message){
		console.log(message);
		// message.newReply.related_message = message.id;
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
			$.toaster({ priority : 'success', title : 'Success', message : 'Reply deleted'});
		}).error(function(data) {
    		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
    	});
	};
	
	// this.updateMessage = function(){
// 		$http.put("/message-json/" + t.selectedTodo.id, t.selectedTodo).success(function(data){
// 			for (var i = 0; i < t.messages.length; i++){
// 			    if (t.todos[i].id == t.selectedTodo.id)
// 			        t.todos[i] = data; //replace an item in array
// 			}
// 			$.toaster({ priority : 'success', title : 'Success', message : 'Message updated'});
// 		}).error(function(data) {
//     		$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
//     	});
// 	};
	
  }]);

})();

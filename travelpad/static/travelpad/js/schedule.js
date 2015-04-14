(function() {
	var app = angular.module('myApp');
	
  	
	app.controller('ScheduleController', ['$http', function($http){
		var t = this;
		this.itinerary = {};
		this.events = [];
		
		$http.get("/itinerary-json").success(function(data){
			console.log(data);
			t.itinerary = data;
			
			//init calendar
			$('#calendar').fullCalendar({
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'agendaWeek,agendaDay'
				},
				defaultView:'agendaWeek',
				allDaySlot: false,
				defaultDate: data.start_date,//'2015-03-23',
				selectable: true,
				selectHelper: true,
				select: function(start, end) {
					//TODO: add events
					// var title = prompt('Event Title:');
// 					var eventData;
// 					if (title) {
// 						eventData = {
// 							title: title,
// 							start: start,
// 							end: end
// 						};
// 						$('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
// 					}
					showeventmodal("", start.format("YYYY-MM-DD"), start.format("hh:mm"), end.format("YYYY-MM-DD"), end.format("hh:mm"))
					$('#calendar').fullCalendar('unselect');
				},
				editable: true,
				eventLimit: true, // allow "more" link when too many events
				events: '/get-calendar-events-json/' + data.id,
				eventClick: function(calEvent, jsEvent, view) {
					editevent(calEvent.id);
					$('#calendar').fullCalendar('unselect');
				    // alert('Event: ' + calEvent.title);
// 				        alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
// 				        alert('View: ' + view.name);
//
// 				        // change the border color just for fun
// 				        $(this).css('border-color', 'red');

				},
				eventDrop: function(event, delta, revertFunc) {

				        alert(event.title + " was dropped on " + event.start.format());

				        if (!confirm("Are you sure about this change?")) {
				            revertFunc();
				        }

				},
				eventResize: function(event, delta, revertFunc) {

				        alert(event.title + " end is now " + event.end.format());

				        if (!confirm("is this okay?")) {
				            revertFunc();
				        }

				},
			});
			
			//init map
			//Retrieves events that FullCalendar has in memory.
			// $('#calendar').fullCalendar('clientEvents' [,  ] ) -> Array 
			
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
		
		
  	}]);
 

})();

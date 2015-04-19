(function() {
	var app = angular.module('myApp');
	
  	
	app.controller('ScheduleController', ['$http', function($http){
		var t = this;
		this.itinerary = {};
		this.events = [];
		
		this.refetchEvent = function(){
			$('#calendar').fullCalendar( 'refetchEvents' );
			
		};
		
		$http.get("/itinerary-json").success(function(data){
			// console.log(data);
			t.itinerary = data;
			
			//init calendar
			$('#calendar').fullCalendar({
				header: {
					left: 'prev,next',
					center: 'title',
					right: 'agendaWeek,agendaDay'
				},
				contentHeight:'auto', //disable scroll bar
				defaultView:'agendaWeek',
				allDaySlot: false,
				defaultDate: data.start_date,//'2015-03-23',
				selectable: true,
				selectHelper: true,
				select: function(start, end) {
					showeventmodal("", start.format("YYYY-MM-DD"), start.format("HH:mm"), end.format("YYYY-MM-DD"), end.format("HH:mm"))
					$('#calendar').fullCalendar('unselect');
				},
				editable: true,
				eventLimit: true, // allow "more" link when too many events
				events: '/get-calendar-events-json/' + data.id,
				eventClick: function(calEvent, jsEvent, view) {
					if(calEvent.className=='transportation'){
						edittransport(calEvent.id);
					}else{
						editevent(calEvent.id);
					}
				},
				eventDrop: function(event, delta, revertFunc) {
					alert(
					            event.title + " was moved " +
					            dayDelta + " days and " +
					            minuteDelta + " minutes."
					        );
					if (!confirm("Are you sure about this change?")) {
					            revertFunc();
					        }
					console.log('eventDrop');
					// editeventtime(id, event.start.format("YYYY-MM-DD"), event.start.format("HH:mm"),
// 						event.end.format("YYYY-MM-DD"), event.end.format("HH:mm"),
// 					function(){
// 						$.toaster({ priority : 'success', title : 'Success', message : 'Event time updated.'});
// 					},function(){
// 						revertFunc();
// 						$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
// 					});
				},
				eventResize: function(event, delta, revertFunc) {
					editeventtime(id, event.start.format("YYYY-MM-DD"), event.start.format("HH:mm"), 
						event.end.format("YYYY-MM-DD"), event.end.format("HH:mm"),
					function(){
						$.toaster({ priority : 'success', title : 'Success', message : 'Event time updated.'});
					},function(){
						revertFunc();
						$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
					});
				},
				eventOverlap: function(stillEvent, movingEvent) {
					// event other than transportation cannot overlap
					return stillEvent.className=='transportation' || movingEvent.className=='transportation'||
							stillEvent.className=='background' || movingEvent.className=='background';
				},
				eventAfterAllRender: (function(){
					return function( view){
						//refresh map view whenever calendar is rendering
						// Retrieves events that FullCalendar has in memory.
						var mapEvents = $('#calendar').fullCalendar('clientEvents', function(evt) {					
							if(evt.className!='background' && evt.className!='transportation'){
								// console.log(evt);
								var startDate = moment(new Date(evt.startdate));
								var endDate = moment(new Date(evt.enddate));
								// console.log(startDate.format("YYYY-MM-DD"));
// 								console.log(endDate.format("YYYY-MM-DD"));
								return !(startDate >= view.intervalEnd || endDate < view.intervalStart);
							}
							return false;
							
						});
						console.log(mapEvents.length + ' map events');
						setAllMarkers(mapEvents);
						
					}
				}()),
			}); // end init calendar
			
			// //TODO:init map
// 			focusCenter();
			
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
		
		
  	}]);
 

})();

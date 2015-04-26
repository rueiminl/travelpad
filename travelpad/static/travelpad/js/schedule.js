(function() {
	var app = angular.module('myApp');
	
	Array.prototype.contains = function(element){
	    return this.indexOf(element) > -1;
	};
  	
	app.controller('ScheduleController', ['$http', '$interval', function($http, $interval){
		var t = this;
		this.itinerary = {};
		this.events = [];
		this.dateTitle;
		this.collapseDesc = true;
		
		this.calendar = {
			prev: function(){
				$('#calendar').fullCalendar('prev');
			},
			next: function(){
				$('#calendar').fullCalendar('next');
			},
			changeWeekView: function(){
				$('#calendar').fullCalendar('changeView', 'agendaWeek');
			},
			changeDayView: function(){
				$('#calendar').fullCalendar('changeView', 'agendaDay');
			},
			isWeekView: function(){
				var view = $('#calendar').fullCalendar('getView');
				return view.name == 'agendaWeek'
			},
		};
		
		//TODO
		this.getShortString = function(str){
			console.log(str);
			if(str.length > 80){
				return str.substring(0,80) + "...";
			}else{
				return str;
			}
		};
		
	
		$http.get("/itinerary-json").success(function(data){
			console.log(data);
			t.itinerary = data;			
			
			/* initialize the calendar
			-----------------------------------------------------------------*/
			$('#calendar').fullCalendar({
				header: {
					left: '',//'prev,next',
					center: '',//'title',
					right: '',//'agendaWeek,agendaDay'
				},
				contentHeight:'auto', //disable scroll bar
				defaultView:'agendaWeek',
				allDaySlot: false,
				defaultDate: data.start_date,//'2015-03-23',
				selectable: true,
				selectHelper: true,
				select: function(start, end) {
					showeventmodal("", start.format("YYYY-MM-DD"), start.format("HH:mm"), end.format("YYYY-MM-DD"), end.format("HH:mm"), 
						function(){
							$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
							$.toaster({ priority : 'success', title : 'Success', message : 'Event added.'});
						}, function(){
							$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event error.'});
						});
					// $('#calendar').fullCalendar('unselect');
				},
				editable: true,
				eventLimit: true, // allow "more" link when too many events
				events: '/get-calendar-events-json/' + data.id,
				viewRender:function(view, element){
					t.dateTitle = view.title;
				},
				eventClick: function(calEvent, jsEvent, view) {
					if(calEvent.className.contains('transportation')){
						edittransport(calEvent.id, function(){
							$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
							$.toaster({ priority : 'success', title : 'Success', message : 'Event updated.'});
						}, function(){
							$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event error.'});
						});
					}else{
						editevent(calEvent.id, function(){
							$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
							$.toaster({ priority : 'success', title : 'Success', message : 'Event updated.'});
						}, function(){
							$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event error.'});
						});
					}
				},
				eventDrop: function(event, delta, revertFunc) {
					if (confirm("Are you sure about this change?")){
						editeventtime(event.id, event.start.format("YYYY-MM-DD"), event.start.format("HH:mm"),
							event.end.format("YYYY-MM-DD"), event.end.format("HH:mm"),
						function(){
							$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
							$.toaster({ priority : 'success', title : 'Success', message : 'Event time updated.'});
						},function(){
							revertFunc();
							$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event time error.'});
						});
					}else{
						revertFunc();
					}
				},
				eventResize: function(event, delta, revertFunc) {
					if (confirm("Are you sure about this change?")){
						editeventtime(event.id, event.start.format("YYYY-MM-DD"), event.start.format("HH:mm"),
							event.end.format("YYYY-MM-DD"), event.end.format("HH:mm"),
						function(){
							$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
							$.toaster({ priority : 'success', title : 'Success', message : 'Event time updated.'});
						},function(){
							revertFunc();
							$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event time error.'});
						});
					}else{
						revertFunc();
					}
				},
				eventOverlap: function(stillEvent, movingEvent) {
					// event other than transportation cannot overlap
					return stillEvent.className.contains('transportation') || movingEvent.className.contains('transportation')||
							stillEvent.className=='background' || movingEvent.className=='background';
				},
				eventAfterAllRender: (function(){
					return function( view){
						// //refresh map view whenever calendar is rendering
						// Retrieves events that FullCalendar has in memory.
						var mapEvents = $('#calendar').fullCalendar('clientEvents', function(evt) {
							if(evt.className!='background' && !evt.className.contains('transportation')){
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
			
			
			// $interval(function(){
// 				$('#calendar').fullCalendar('refetchEvents');
// 			}, 3000);
			
			// init map
			setCity(data.place.latitude, data.place.longitude);
			
		}).error(function(data) {
	    	$.toaster({ priority : 'danger', title : 'Error', message : data.errors});
	    });
		
		
		this.addEvent = function(){
			showeventmodal("", "", "", "", "",
				function(){
					$('#calendar').fullCalendar('refetchEvents'); //refresh related transportation
					$.toaster({ priority : 'success', title : 'Success', message : 'Event updated.'});
				}, function(){
					$.toaster({ priority : 'danger', title : 'Error', message : 'Update Event error.'});
			});
		};
		
  	}]);
	
	app.controller('TabController', function(){
		this.tab = 1;

		this.setTab = function(newValue){
			//resize Google map every time the map show up
			if(newValue==2){
				resizeMap();
			} 
			this.tab = newValue;
		};

		this.isSet = function(tabName){
			return this.tab === tabName;
		};
	});
 

})();		

var s_callback = function(){console.log("this is s_callback");};
var e_callback = function(){console.log("this is e_callback");};

(function() {
  var app = angular.module('myApp');

  
  
  app.controller('EventController', ['$scope', '$http', '$interval', function($scope, $http, $interval){
	var t = this;
	this.events = [];
    this.newAttraction = {};
    this.newHotel = {};
    this.newTransport = {};
    this.newRestaurant = {};
    this.selectedEvent = {};
    this.currenttab = "Attraction";
    this.error = [];
    
    this.setPropose = function(){
        this.button="Propose";
    };
    this.setSave = function(){
        this.button="Save";
    };
	
    this.ready = function(){
      console.log("running ready");
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=places&signed_in=true&language=en-us&callback=initialize_event';
      document.body.appendChild(script);
      $("#mybutton").click( function()
        {
            //showeventmodal("title","2015-03-25","13:15","2015-03-25","14:15")
            showeventmodal("","","","","")
        }
      );
      $("#mybutton2").click( function()
        {
            var ss_callback = function(){console.log("this is ss_callback");};
            var ee_callback = function(){console.log("this is ee_callback");};
            editevent(107,ss_callback,ee_callback);
        }
      );
      $("#mybutton3").click( function()
        {
            var ss_callback = function(){console.log("this is ss_callback");};
            var ee_callback = function(){console.log("this is ee_callback");};
            edittransport(1,ss_callback,ee_callback);
        }
      );
      $("#mybutton4").click( function()
        {
            var a = function(){console.log("this is a");};
            var b = function(){console.log("this is b");};
            editeventtime(2, "2015-03-24","16:15","2015-03-24","17:15", a, b);
        }
      );
      $("#deletebtn").click( function()
        {
            deleteevent();
        }
      );

      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $('#tabName').val($('.nav-tabs .active').text());
      });
       $("#eventModal").on('hidden.bs.modal', function () {
            $(this).find('form')[0].reset();
            $('#map-eventcanvas').show();
            $('#map-eventcanvas2').show();
            $('#map-eventcanvas3').show();
            $('#map-eventcanvas4').show();
            $('#pac-input').show();
            $('#pac-input2').show();
            $('#pac-input3').show();
            $('#pac-input4').show();
            $('#tabBar').show();
            $('#placelabel_a').text("");
            $('#placetext_a').text("");
            $('#placelabel_h').text("");
            $('#placetext_h').text("");
            $('#placelabel_t').text("");
            $('#placetext_t').text("");
            $('#placelabel_r').text("");
            $('#placetext_r').text("");
            $('#placetext_r').text("");
            $('#deletebtn').hide();
            $('#eventId').val("");
            $('#coordinate').val("");
            $('#placeId').val("");
            $('#placeName').val("");
            $('#tabName').val("");
            $('#map-eventcanvas3').hide();
            $('.nav-tabs a[href="#Transportation"]').hide();
            $('.nav-tabs a[href="#Attraction"]').tab('show');
            
            $scope.$apply(function () {
                t.error = [];
            });
       });
       
       $("#Event_Form").submit(function(e)
        {
            e.preventDefault(); //STOP default action
            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            postData.push({name: "button",value: t.button});
            $.ajax(
            {
                url : formURL,
                type: "POST",
                data : postData,
                success: function(response, status, xhr){ 
                    var ct = xhr.getResponseHeader("content-type") || "";
                    if (ct.indexOf('html') > -1) {
                        var newDoc = document.open("text/html", "replace");
                        newDoc.write(response);
                        /*$(response).find("script").each(function(i) {
                            eval($(this).text());
                        });*/
                        newDoc.close();
                    }
                    if (ct.indexOf('json') > -1) {
                        console.log("success");
                        console.log(response);
                        if (response.errors){
                            t.error = [];
                            $scope.$apply(function () {
                                for (ee in response.errors){
                                    t.error.push(response.errors[ee]);
                                }
                            });
                        }
                        else{
                            if (response.trans_up && response.trans_up.length > 0){
                                var a = function(ids,arr){
                                    console.log("www");
                                    console.log(arr);
                                    $.ajax({
                                        url: "./updatetransport",
                                        data: {
                                            ids: ids,
                                            arr: arr,
                                        },
                                        type:'POST',
                                        dataType: 'json',
                                        success: function(response, status, xhr){ 
                                            console.log("update transport success");
                                        },
                                        error: function(response, status, xhr){ 
                                            console.log("update transport fail");
                                        }
                                    });
                                    
                                };
                                var b = function(ids,arr){
                                    console.log("www");
                                    console.log(arr);
                                    $.ajax({
                                        url: "./updatetransport",
                                        data: {
                                            ids: ids,
                                            arr: arr,
                                        },
                                        type:'POST',
                                        dataType: 'json',
                                        success: function(response, status, xhr){ 
                                            console.log("update transport success");
                                            s_callback();
                                        },
                                        error: function(response, status, xhr){ 
                                            console.log("update transport fail");
                                        }
                                    });
                                    
                                };
                                for (var i = 0; i < response.trans_up.length-1; i++){
                                    getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],a,e_callback);
                                }
                                getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],b,e_callback);
                            }
                            $('#eventModal').modal('hide');
                            $.toaster({ priority : 'success', title : 'Success', message : 'New event added'});                      
                        }
                    } 
                },
                error: function(items) 
                {
                    console.log("error");
                    var newDoc = document.open("text/html", "replace");
                    newDoc.write(items);
                    newDoc.close();
                }
            });
        });
        
       $('#map-eventcanvas3').hide();
       $('.nav-tabs a[href="#Transportation"]').hide();
       
       //$('#datetimepicker1').datetimepicker();
	};
	//initialize
	this.ready();
   

  }]);
})();

// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.
      function initialize_event() {
        initialize_attraction();
        initialize_hotel();
        initialize_transportation();
        initialize_restaurant();
      }
      var searchBox1;
      
      function initialize_attraction() {

        var markers = [];
        var map = new google.maps.Map(document.getElementById('map-eventcanvas'), {
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(-33.8902, 151.1759),
            new google.maps.LatLng(-33.8474, 151.2631));
        map.fitBounds(defaultBounds);

        // Create the search box and link it to the UI element.
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('pac-input'));
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        searchBox1 = new google.maps.places.SearchBox(
          /** @type {HTMLInputElement} */(input));

        // [START region_getplaces]
        // Listen for the event fired when the user selects an item from the
        // pick list. Retrieve the matching places for that item.
        google.maps.event.addListener(searchBox1, 'places_changed', function() {
          var places = searchBox1.getPlaces();

          if (places.length == 0) {
            return;
          }
          if(places.length > 1){
            document.getElementById("testMsg").innerHTML = "You can not submit more than one place, be more specified!"
            return;
          }
          for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
          }

          // For each place, get the icon, place name, and location.
          markers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {
            var image = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };
            // Create a marker for each place.
            var marker = new google.maps.Marker({
              map: map,
              icon: image,
              title: place.name,
              position: place.geometry.location
            });
            document.getElementById("coordinate").value = place.geometry.location;
            document.getElementById("placeId").value = place.place_id;
            document.getElementById("placeName").value = place.name;
            markers.push(marker);

            bounds.extend(place.geometry.location);
          }

          map.fitBounds(bounds);
        });
        // [END region_getplaces]

        // Bias the SearchBox results towards places that are within the bounds of the
        // current map's viewport.
        google.maps.event.addListener(map, 'bounds_changed', function() {
          var bounds = map.getBounds();
          searchBox1.setBounds(bounds);
        });
        var idleListener = google.maps.event.addListener(map, 'mousemove', function() {
          google.maps.event.trigger(map, 'resize');
          //google.maps.event.removeListener(idleListener);
        });
      }
      
      function initialize_hotel() {
        var markers = [];
        var map = new google.maps.Map(document.getElementById('map-eventcanvas2'), {
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(-33.8902, 151.1759),
            new google.maps.LatLng(-33.8474, 151.2631));
        map.fitBounds(defaultBounds);

        // Create the search box and link it to the UI element.
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('pac-input2'));
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        var searchBox = new google.maps.places.SearchBox(
          /** @type {HTMLInputElement} */(input));

        // [START region_getplaces]
        // Listen for the event fired when the user selects an item from the
        // pick list. Retrieve the matching places for that item.
        google.maps.event.addListener(searchBox, 'places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
          if(places.length > 1){
            document.getElementById("testMsg").innerHTML = "You can not submit more than one place, be more specified!"
            return;
          }
          for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
          }

          // For each place, get the icon, place name, and location.
          markers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {
            var image = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };
            // Create a marker for each place.
            var marker = new google.maps.Marker({
              map: map,
              icon: image,
              title: place.name,
              position: place.geometry.location
            });
            document.getElementById("coordinate").value = place.geometry.location;
            document.getElementById("placeId").value = place.place_id;
            document.getElementById("placeName").value = place.name;
            markers.push(marker);

            bounds.extend(place.geometry.location);
          }

          map.fitBounds(bounds);
        });
        // [END region_getplaces]

        // Bias the SearchBox results towards places that are within the bounds of the
        // current map's viewport.
        google.maps.event.addListener(map, 'bounds_changed', function() {
          var bounds = map.getBounds();
          searchBox.setBounds(bounds);
        });
        var idleListener = google.maps.event.addListener(map, 'mousemove', function() {
          google.maps.event.trigger(map, 'resize');
          //google.maps.event.removeListener(idleListener);
        });
      }
      
      function initialize_transportation() {
        var markers = [];
        var map = new google.maps.Map(document.getElementById('map-eventcanvas3'), {
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(-33.8902, 151.1759),
            new google.maps.LatLng(-33.8474, 151.2631));
        map.fitBounds(defaultBounds);

        // Create the search box and link it to the UI element.
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('pac-input3'));
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        var searchBox = new google.maps.places.SearchBox(
          /** @type {HTMLInputElement} */(input));

        // [START region_getplaces]
        // Listen for the event fired when the user selects an item from the
        // pick list. Retrieve the matching places for that item.
        google.maps.event.addListener(searchBox, 'places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
          if(places.length > 1){
            document.getElementById("testMsg").innerHTML = "You can not submit more than one place, be more specified!"
            return;
          }
          for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
          }

          // For each place, get the icon, place name, and location.
          markers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {
            var image = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };
            // Create a marker for each place.
            var marker = new google.maps.Marker({
              map: map,
              icon: image,
              title: place.name,
              position: place.geometry.location
            });
            document.getElementById("coordinate").value = place.geometry.location;
            document.getElementById("placeId").value = place.place_id;
            document.getElementById("placeName").value = place.name;
            markers.push(marker);

            bounds.extend(place.geometry.location);
          }

          map.fitBounds(bounds);
        });
        // [END region_getplaces]

        // Bias the SearchBox results towards places that are within the bounds of the
        // current map's viewport.
        google.maps.event.addListener(map, 'bounds_changed', function() {
          var bounds = map.getBounds();
          searchBox.setBounds(bounds);
        });
        var idleListener = google.maps.event.addListener(map, 'mousemove', function() {
          google.maps.event.trigger(map, 'resize');
          //google.maps.event.removeListener(idleListener);
        });
      }
      
      function initialize_restaurant() {
        var markers = [];
        var map = new google.maps.Map(document.getElementById('map-eventcanvas4'), {
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var defaultBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(-33.8902, 151.1759),
            new google.maps.LatLng(-33.8474, 151.2631));
        map.fitBounds(defaultBounds);

        // Create the search box and link it to the UI element.
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('pac-input4'));
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        var searchBox = new google.maps.places.SearchBox(
          /** @type {HTMLInputElement} */(input));

        // [START region_getplaces]
        // Listen for the event fired when the user selects an item from the
        // pick list. Retrieve the matching places for that item.
        google.maps.event.addListener(searchBox, 'places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
          if(places.length > 1){
            document.getElementById("testMsg").innerHTML = "You can not submit more than one place, be more specified!"
            return;
          }
          for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
            
          }

          // For each place, get the icon, place name, and location.
          markers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {
            var image = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };
            // Create a marker for each place.
            var marker = new google.maps.Marker({
              map: map,
              icon: image,
              title: place.name,
              position: place.geometry.location
            });
            document.getElementById("coordinate").value = place.geometry.location;
            document.getElementById("placeId").value = place.place_id;
            document.getElementById("placeName").value = place.name;
            markers.push(marker);

            bounds.extend(place.geometry.location);
          }

          map.fitBounds(bounds);
        });
        // [END region_getplaces]

        // Bias the SearchBox results towards places that are within the bounds of the
        // current map's viewport.
        google.maps.event.addListener(map, 'bounds_changed', function() {
          var bounds = map.getBounds();
          searchBox.setBounds(bounds);
        });
        var idleListener = google.maps.event.addListener(map, 'mousemove', function() {
          google.maps.event.trigger(map, 'resize');
          //google.maps.event.removeListener(idleListener);
        });
      }
      
      function editevent(id, success_callback, error_callback) {
      s_callback = success_callback;
      e_callback = error_callback;
    $.ajax({
        url: "./getevent",
        data: {
            eid: id,
        },
        type:'POST',
        dataType: 'json',
        success: function(items){
            $('#eventModal').modal('show');
            var fix
            if (items.data.type == "attraction"){
                $('.nav-tabs a[href="#Attraction"]').tab('show');
                fix = "a";
            }
            else if (items.data.type == "hotel"){
                $('.nav-tabs a[href="#Hotel"]').tab('show');
                fix = "h";
            }
            else if (items.data.type == "transportation"){
                $('.nav-tabs a[href="#Transportation"]').tab('show');
                fix = "t";
            }
            else{
                $('.nav-tabs a[href="#Restaurant"]').tab('show');
                fix = "r";
            }
            $('#tabName').val($('.nav-tabs .active').text());
            $('#tabBar').hide();
            
            $('#id_' + fix + '_-title').val(items.data.title);
            $('#id_' + fix + '_-start_date').val(items.data.startdate);
            $('#id_' + fix + '_-start_time').val(items.data.starttime);
            $('#id_' + fix + '_-end_date').val(items.data.enddate);
            $('#id_' + fix + '_-end_time').val(items.data.endtime);
            $('#placelabel_' + fix).text("Place:");
            $('#placetext_' + fix).text(items.data.place.name);
            $('#id_' + fix + '_-note').val(items.data.note);
            $('#map-eventcanvas').hide();
            $('#map-eventcanvas2').hide();
            $('#map-eventcanvas3').hide();
            $('#map-eventcanvas4').hide();
            $('#pac-input').hide();
            $('#pac-input2').hide();
            $('#pac-input3').hide();
            $('#pac-input4').hide();
            $('#eventId').val(items.data.id);
            $('#deletebtn').show();

        }
    });
};

function editeventtime(id, sdate, stime, edate, etime, success_callback,error_callback) {
    $.ajax({
        url: "./editeventtime_json",
        data: {
            eid: id,
            sdate: sdate,
            edate: edate,
            stime: stime,
            etime: etime,
        },
        type:'POST',
        dataType: 'json',
        success: function(response, status, xhr){ 
            console.log("cuss");
            console.log(response);
            if (response.trans_up && response.trans_up.length > 0){
                var a = function(ids,arr){
                    console.log("www");
                    console.log(arr);
                    $.ajax({
                        url: "./updatetransport",
                        data: {
                            ids: ids,
                            arr: arr,
                        },
                        type:'POST',
                        dataType: 'json',
                        success: function(response, status, xhr){ 
                            console.log("update transport success");
                        },
                        error: function(response, status, xhr){ 
                            console.log("update transport fail");
                        }
                    });
                    
                };
                var b = function(ids,arr){
                    console.log("www");
                    console.log(arr);
                    $.ajax({
                        url: "./updatetransport",
                        data: {
                            ids: ids,
                            arr: arr,
                        },
                        type:'POST',
                        dataType: 'json',
                        success: function(response, status, xhr){ 
                            console.log("update transport success");
                            success_callback();
                        },
                        error: function(response, status, xhr){ 
                            console.log("update transport fail");
                        }
                    });
                    
                };
                for (var i = 0; i < response.trans_up.length-1; i++){
                    getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],a,error_callback);
                }
                getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],b,error_callback);
            }
        },
        error: error_callback,
    });
};

function edittransport(id, success_callback, error_callback) {
    s_callback = success_callback;
    e_callback = error_callback;
    $.ajax({
        url: "./gettransport",
        data: {
            eid: id,
        },
        type:'POST',
        dataType: 'json',
        success: function(items){
            $('#eventModal').modal('show');
            var fix = "t";
            $('.nav-tabs a[href="#Transportation"]').show();
            $('.nav-tabs a[href="#Transportation"]').tab('show');
            $('#tabName').val($('.nav-tabs .active').text());
            $('#tabBar').hide();
            
            $('#id_' + fix + '_-title').val("Transportation Route");
            $('#id_' + fix + '_-start_date').val(items.data.startdate);
            $('#id_' + fix + '_-start_time').val(items.data.starttime);
            $('#id_' + fix + '_-end_date').val(items.data.enddate);
            $('#id_' + fix + '_-end_time').val(items.data.endtime);
            $('#placelabel_' + fix).text("From:");
            $('#placetext_' + fix).text(items.data.source);
            $('#placelabel2_' + fix).text("To:");
            $('#placetext2_' + fix).text(items.data.destination);
            $('#id_' + fix + '_-note').val(items.data.note);
            $('#id_' + fix + '_-format').val(items.data.type);
            $('#eventId').val(items.data.id);
            $('#map-eventcanvas3').hide();

        }
    });
};


function deleteevent() {
    id = $('#eventId').val();
    if (confirm("Are you sure you want to delete this event?") == true) {
        $.ajax({
            url: "/deleteevent_json",
            data: {
                eid: id,
            },
            type:'POST',
            success: function(response, status, xhr){ 
               console.log("deleted");
               console.log(response);
               $('#eventModal').modal('hide');
               if (response.trans_up && response.trans_up.length > 0){
                    var a = function(ids,arr){
                        console.log("www");
                        console.log(arr);
                        $.ajax({
                            url: "./updatetransport",
                            data: {
                                ids: ids,
                                arr: arr,
                            },
                            type:'POST',
                            dataType: 'json',
                            success: function(response, status, xhr){ 
                                console.log("update transport success");
                            },
                            error: function(response, status, xhr){ 
                                console.log("update transport fail");
                            }
                        });
                        
                    };
                    var b = function(ids,arr){
                        console.log("www");
                        console.log(arr);
                        $.ajax({
                            url: "./updatetransport",
                            data: {
                                ids: ids,
                                arr: arr,
                            },
                            type:'POST',
                            dataType: 'json',
                            success: function(response, status, xhr){ 
                                console.log("update transport success");
                                s_callback();
                            },
                            error: function(response, status, xhr){ 
                                console.log("update transport fail");
                            }
                        });
                        
                    };
                    for (var i = 0; i < response.trans_up.length-1; i++){
                        getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],a,e_callback);
                    }
                    getTime2(response.trans_up[i].id, [[response.pevent_up[i].place.latitude,response.pevent_up[i].place.longitude]], [[response.nevent_up[i].place.latitude,response.nevent_up[i].place.longitude]],[response.trans_up[i].type],[response.trans_up[i].start],b,e_callback);
                }
               $.toaster({ priority : 'success', title : 'Success', message : 'Event deleted'});    
               //$(location).attr('href',"./schedule");
            }
        });
    }
}
    
function showeventmodal(title, sdate, stime, edate, etime, success_callback,error_callback) {
    s_callback = success_callback;
    e_callback = error_callback;
    $('#eventModal').modal('show');
    $('#id_a_-title').val(title);
    $('#id_h_-title').val(title);
    $('#id_t_-title').val(title);
    $('#id_r_-title').val(title);
    
    $('#id_a_-start_date').val(sdate);
    $('#id_h_-start_date').val(sdate);
    $('#id_t_-start_date').val(sdate);
    $('#id_r_-start_date').val(sdate);
    
    $('#id_a_-start_time').val(stime);
    $('#id_h_-start_time').val(stime);
    $('#id_t_-start_time').val(stime);
    $('#id_r_-start_time').val(stime);
    
    $('#id_a_-end_date').val(edate);
    $('#id_h_-end_date').val(edate);
    $('#id_t_-end_date').val(edate);
    $('#id_r_-end_date').val(edate);
    
    $('#id_a_-end_time').val(etime);
    $('#id_h_-end_time').val(etime);
    $('#id_t_-end_time').val(etime);
    $('#id_r_-end_time').val(etime);
    
    $('.nav-tabs a[href="#Attraction"]').tab('show');
    
    //$('#pac-input').val("TTTP");
    //google.maps.event.trigger(searchBox1, 'places_changed');

}
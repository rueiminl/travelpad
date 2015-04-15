// Functions:
//  1. initialize(): create a google map object and initiallize all kinds of states.
//  2. focusCenter(latitude, longitude): Focus the google map view with latitude and longitude
//  3. setAllMarkers(placeArrTmp): create marker and route of particular time slots. Data is passed by JSON Value
//  4. getTime(src, dest, mode): get the time from src to dest via mode (transportation mode)
//  5. getCityItinerary(): For the start of itinerary, get the city's latLng via google autocomplete.



var directionsService = new google.maps.DirectionsService();
var map;
var placeArr = [];
var markers = [];
var countNum = 0;
var mapOptions;
var flightPaths = [];
var directionsDisplays = [];
var zoomVar = 12;
var centerVar;
var autocomplete;
function initialize() {
    //deleteMarkers();
    directionsDisplay = new google.maps.DirectionsRenderer();
    placeArrTmp = [[40.442492, -79.94255299999998], [40.444353, -79.96083499999997]];
    placeArr = [];
    markers = [];
   // for(var i=0; i<arr.length; i++){
   //   placeArr.push(new google.maps.LatLng(arr[i][0], arr[i][1]));
    //}
    //{% for place in places %}
    //    placeArr.push(new google.maps.LatLng("{{place.latitude}}", "{{place.longitude}}"));
    //{% endfor %}
    
    //var myLatlng = new google.maps.LatLng(document.getElementById("lat").getAttribute("value"), document.getElementById("lng").getAttribute("value"));
    var myLatlng = new google.maps.LatLng(40.442492, -79.94255299999998);
    centerVar = myLatlng;
    mapOptions = {
        center: centerVar,
        zoom: zoomVar, 
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);
    setAllMarkers(placeArrTmp);
    
}

function getCityItinerary(){
  var input = (document.getElementById('autocomplete'));
  var options = {
    types: ['(cities)']
  };
  autocomplete = new google.maps.places.Autocomplete(input, options);
  var place = autocomplete.getPlace();
  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      return;
    }
    document.getElementById("abc").innerHTML = place.geometry.location;
  });
}

function detectBrowser() {
  var useragent = navigator.userAgent;
  var mapdiv = document.getElementById("map_canvas");

  if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
    mapdiv.style.width = '100%';
    mapdiv.style.height = '100%';
  } else {
    mapdiv.style.width = '600px';
    mapdiv.style.height = '800px';
  }
}

function getTime(src, dest, mode){
  var request = {
      origin: src,
      destination: dest,
      travelMode: google.maps.TravelMode[mode]
  };
  directionsService.route(request, function(response, status) {
    var summaryPanel = document.getElementById('directions_panel');
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      //summaryPanel.innerHTML = '';
      var routeSegment = index;
      summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
      summaryPanel.innerHTML += route.legs[0].start_address + ' to ';
      summaryPanel.innerHTML += route.legs[0].end_address + '<br>';
      summaryPanel.innerHTML += route.legs[0].distance.text + '<br>';
      summaryPanel.innerHTML += route.legs[0].duration.text + '<br><br>';
      summaryPanel.innerHTML += route.legs[0].duration.value + '<br>';
    }
    else{
      summaryPanel.innerHTML += 'No such route' + '<br><br>';
    }
  });

}

function calcRoute(src, dest, mode, index) {
  var directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplays.push(directionsDisplay);
  directionsDisplay.setMap(map);
  directionsDisplay.setOptions({ suppressMarkers: true });
  var request = {
      origin: src,
      destination: dest,
      // Note that Javascript allows us to access the constant
      // using square brackets and a string value as its
      // "property."
      travelMode: google.maps.TravelMode[mode]
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      var summaryPanel = document.getElementById('directions_panel');
      //summaryPanel.innerHTML = '';
      var routeSegment = index;
      summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
      summaryPanel.innerHTML += route.legs[0].start_address + ' to ';
      summaryPanel.innerHTML += route.legs[0].end_address + '<br>';
      summaryPanel.innerHTML += route.legs[0].distance.text + '<br>';
      summaryPanel.innerHTML += route.legs[0].duration.text + '<br><br>';
    }
    else{
      flightPath = new google.maps.Polyline({
        path: [src, dest],
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });
      flightPath.setMap(map);
      flightPaths.push(flightPath);
    }
  });
}

function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function clearMarkers(){
  setAllMap(null);
  markers = [];
  for(var i=0; i<flightPaths.length; i++){
    flightPaths[i].setMap(null);
  }
  for(var i=0; i<directionsDisplays.length; i++){
    directionsDisplays[i].setMap(null);
  }
  flightPaths = [];
  directionsDisplays = [];
  document.getElementById("directions_panel").innerHTML = "";
}   

function focusCenter(latitude, longitude){
  //var myLatlng = new google.maps.LatLng(focusLatLng[0], focusLatLng[1]);
  var myLatlng = new google.maps.LatLng(latitude, longitude);
  map.setCenter(myLatlng);
}   

// Set new places
// JSON format for placeArrTmp:
// {"placeInfos": [
//  {
//    place_latitude:
//    place_longitude:  
//    place_name:
//  },
//  {
//    place_latitude:
//    place_longitude:  
//    place_name:
//  }
// ]
// }
// [{ transportation:{..}, place:{...} }, {transportation...}    ...]

function setAllMarkers(placeArrTmp){
  clearMarkers();
  if(placeArrTmp == null || placeArrTmp.length == 0)
      return;
  var myPlace = JSON.parse(placeArrTmp);

  for(var i=0; i<myPlace.length; i++){
    var placeInfo = myPlace[i].place;
    placeArr.push(new google.maps.LatLng(placeInfo.place_latitude, placeInfo.place_longitude));
  }

  //for(i=0; i<placeArrTmp.length; i++){
  //  placeArr.push(new google.maps.LatLng(placeArrTmp[i][0], placeArrTmp[i][1]));
  //}
  // start point
  var start = placeArr[0];
  var marker = new google.maps.Marker({
        position: placeArr[0],
        map: map,
        title: 'start'
  });

  markers.push(marker);
  var infowindow = new google.maps.InfoWindow({
    content: "Start"
  });
  infowindow.open(map,marker);

  // middle points
  for(index=1; index<placeArr.length ; index++){
      calcRoute(start, placeArr[index], "DRIVING", index);

      marker = new google.maps.Marker({
        position: placeArr[index],
        map: map,
        title: 'Location'
      });
      infowindow = new google.maps.InfoWindow({
        content: (index+1).toString()
      });
      infowindow.open(map,marker);
      start = placeArr[index];
      markers.push(marker);
  }
  
} 


google.maps.event.addDomListener(window, 'load', initialize);

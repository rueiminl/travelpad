// Functions:
//  1. initialize(): create a google map object and initiallize all kinds of states.
//  2. focusCenter(latitude, longitude): Focus the google map view with latitude and longitude
//  3. setAllMarkers(placeArrTmp): create marker and route of particular time slots. Data is passed by JSON Value
//  4. call resizeMap() --> When the "map" buttom is pressed. 
//  5. getTime(src, dest, mode): get the time from src to dest via mode (transportation mode)
//  6. getCityItinerary(): For the start of itinerary, get the city's latLng via google autocomplete.
//  7. setCity(latitude, longitude): set itinerary city center;



var directionsService = new google.maps.DirectionsService();
var directionsDisplay;
var map;
// Places's latitude and longitude
var placeArr = [];
// Places's location name
var placeNameArr = [];
// start time from source
var startTimes = [];
// transportation modes from source
var transportTypes = [];
// marker sets on google map
var markers = [];
var countNum = 0;
var mapOptions ;
var flightPaths = [];
var directionsDisplays = [];
var zoomVar = 12;
var centerVar;
var autocomplete;
var cityCenter = [40.442492, -79.94255299999998];
function initialize() {
    //deleteMarkers();
    directionsDisplay = new google.maps.DirectionsRenderer();
    placeArrTmp = [];
    placeArr = [];
    markers = [];
    var myLatlng = new google.maps.LatLng(cityCenter[0], cityCenter[1]);
    centerVar = myLatlng;
    mapOptions = {
        center: centerVar,
        zoom: zoomVar, 
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);
    google.maps.event.addListener(map, 'idle', function() {
       google.maps.event.trigger(map, 'resize');
    });
    //var obj = [{transporation:{start: ""}, place:{id: 1, latitude:40.442492, longitude:-79.94255299999998, name: "CMU"}}];
    //setAllMarkers(obj);
    //focusCenter(-25.363882, 131.044922);
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

function calcRoute(src, dest, mode, index, startTime) {
  if(mode == "car")
    mode = "driving";
  var directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplays.push(directionsDisplay);
  directionsDisplay.setMap(map);
  //directionsDisplay.setPanel(document.getElementById('directions-panel'));
  directionsDisplay.setOptions({ suppressMarkers: true });
  var t = new Date(startTime);
  console.log("src:" + src + ", dest: " + dest + ", mode: " + mode);
  var request = {
      origin: src,
      destination: dest,
      travelMode: google.maps.TravelMode[mode.toUpperCase()],
      transitOptions: {
        departureTime: t
      }
    };
  /* 
  if(mode == "TRANSIT"){
    request = {
      origin: src,
      destination: dest,
      travelMode: google.maps.TravelMode[mode],
      transitOptions: {
        departureTime: new Date(t.getTime())
      }
    };
  }
  else{
    request = {
      origin: src,
      destination: dest,
      travelMode: google.maps.TravelMode["DRIVING"]
    };
  }
  */
  var directionsService = new google.maps.DirectionsService();
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
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
  placeNameArr = [];
  transportTypes = [];
  startTimes = [];
  //document.getElementById("directions_panel").innerHTML = "";
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
  initialize();
  clearMarkers();
  console.log(placeArrTmp);
  //alert("clearMarkers");  

  if(placeArrTmp == null || placeArrTmp.length == 0)
      return;

  //var myPlace = JSON.parse(placeArrTmp[0]);
  for(var i=0; i<placeArrTmp.length; i++){
    var myPlace = placeArrTmp[i];
    var placeInfo = myPlace.place;
    var transportationInfo = myPlace.transportation;
    placeArr.push(new google.maps.LatLng(placeInfo.latitude, placeInfo.longitude));
    placeNameArr.push(placeInfo.name);
    //alert(placeInfo.name);
    if(transportationInfo == null){
      transportTypes.push(null);
      startTimes.push(null);
    }
    else{
      transportTypes.push(transportationInfo.type);
      startTimes.push(transportationInfo.start);
    }
  }

  for(var i=0; i<transportTypes.length; i++)
    console.log(transportTypes[i]);

  // start point
  var start = placeArr[0];
  var marker = new google.maps.Marker({
        position: placeArr[0],
        map: map,
        title: 'start'
  });

  markers.push(marker);
  var infowindow = new google.maps.InfoWindow({
    content: "<div><b>Start: </b>" + placeNameArr[0] + "</div>"
  });
  infowindow.open(map,marker);

  if(transportTypes[0] != undefined)
    addMarker(marker, infowindow, false, 0);
  //addMarker(marker, infowindow);

  // middle points
  for(var index=1; index<placeArr.length ; index++){
      var last = true;
      console.log(index + ": " + placeNameArr[index-1] + " -> " + placeNameArr[index]);
      if(transportTypes[index-1] != undefined){
        calcRoute(placeArr[index-1], placeArr[index], transportTypes[index-1], index, startTimes[index-1]);
      }
      if(transportTypes[index] != undefined){
        last = false;
      }
      marker = new google.maps.Marker({
        position: placeArr[index],
        map: map,
        title: 'Location'
      });
      infowindow = new google.maps.InfoWindow({
        content: "<div><b>" + (index+1).toString() + ".</b>" + placeNameArr[index] + "</div>"
      });
      addMarker(marker, infowindow, last, index);
      //infowindow.open(map,marker);
      start = placeArr[index];
      markers.push(marker);
  }
} 

function resizeMap(){
  google.maps.event.addListener(map, 'idle', function() {
      google.maps.event.trigger(map, 'resize');
  });
  map.setZoom(3);
  if(placeArr.length != 0)
    map.setCenter(placeArr[0]);
  else
    map.setCenter();
}

function addMarker(marker, infowindow, last, index){
  google.maps.event.addListener(marker, 'click', function() {
        document.getElementById('directions-panel').innerHTML = "";
        infowindow.open(map, marker);
        if(last == false){
          tmpInfo = new google.maps.InfoWindow({
            content: "<div><b>" + (index+2).toString() + ".</b>" + placeNameArr[index+1] + "</div>"
          });
          tmpInfo.open(map, markers[index+1]);

          var tmpDisplay = new google.maps.DirectionsRenderer();
          tmpDisplay.setPanel(document.getElementById('directions-panel'));
          var request = {
            origin: placeArr[index],
            destination: placeArr[index+1],
            travelMode: google.maps.TravelMode[transportTypes[index].toUpperCase()],
            transitOptions: {
              departureTime: new Date(startTimes[index])
            }
          };
          var tmpService = new google.maps.DirectionsService();
          tmpService.route(request, function(response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
              tmpDisplay.setDirections(response);
            }
            else{
              document.getElementById('directions-panel').innerHTML = "No Route between these two place";
            }
          });
        }
  });
}

function setCity(latitude, longitude){
  cityCenter = [latitude, longitude];
}

//google.maps.event.addDomListener(window, 'load', initialize);

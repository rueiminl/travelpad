<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?v=3"></script>
<script type="text/javascript">
var directionsService = new google.maps.DirectionsService();
var map;
var placeArr = [];
var markers = [];
var countNum = 0;
function initialize(arr) {
    //deleteMarkers();
    directionsDisplay = new google.maps.DirectionsRenderer();
    placeArr = [];
    markers = [];
    for(var i=0; i<arr.length; i++){
      placeArr.push(new google.maps.LatLng(arr[i][0], arr[i][1]));
    }
    //{% for place in places %}
    //    placeArr.push(new google.maps.LatLng("{{place.latitude}}", "{{place.longitude}}"));
    //{% endfor %}

    var myLatlng = new google.maps.LatLng(document.getElementById("lat").getAttribute("value"), document.getElementById("lng").getAttribute("value"));
    var mapOptions = {
        center: myLatlng,
        zoom: 8, 
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);

    if(placeArr.length == 0){
        return;
    }
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
    for(index=1; index<placeArr.length; index++){
        calcRoute(start, placeArr[index], "DRIVING", index);

        marker = new google.maps.Marker({
          position: placeArr[index],
          map: map,
          title: 'Location'
        });
        infowindow = new google.maps.InfoWindow({
          content: index.toString()
        });
        infowindow.open(map,marker);
        start = placeArr[index];
        markers.push(marker);
    }
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

function calcRoute(src, dest, mode, index) {
  var directionsDisplay = new google.maps.DirectionsRenderer();
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
      var flightPath = new google.maps.Polyline({
        path: [src, dest],
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });
      flightPath.setMap(map);
    }
  });
}         


google.maps.event.addDomListener(window, 'load', initialize);

</script>
function getTime(src, dest, mode){
  var srcPlace = new google.maps.LatLng(src[0], src[1]);
  var destPlace = new google.maps.LatLng(dest[0], dest[1]);
  var request = {
      origin: srcPlace,
      destination: destPlace,
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
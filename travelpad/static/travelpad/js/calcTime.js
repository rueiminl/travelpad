
/*
function getTime(src, dest, mode){
  var srcPlace = new google.maps.LatLng(src[0], src[1]);
  var destPlace = new google.maps.LatLng(dest[0], dest[1]);
  var request = {
      origin: srcPlace,
      destination: destPlace,
      travelMode: google.maps.TravelMode[mode],
      transitOptions: {
        departureTime: new Date(t.getTime())
      }
  };
  var directionsService = new google.maps.DirectionsService();
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
*/

function getTime2(ids, src, dest, mode, time, callback, errorhandle){
  var arr = [];
  var directionsService = new google.maps.DirectionsService();
  for(var i=0; i<src.length; i++){
    var srcPlace = new google.maps.LatLng(src[i][0], src[i][1]);
    var destPlace = new google.maps.LatLng(dest[i][0], dest[i][1]);
    var timeTrans = new Date(time[i]);
    var request = {
      origin: srcPlace,
      destination: destPlace,
      travelMode: google.maps.TravelMode[mode[i].toUpperCase()],
      transitOptions: {
        departureTime: timeTrans
      }
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        var route = response.routes[0];
        arr.push(route.legs[0].duration.value);
        callback(ids, arr[0]);
      }
      else{
        if (status == google.maps.GeocoderStatus.OVER_QUERY_LIMIT) {
            setTimeout(function() {getTime2(ids, src, dest, mode, time, callback, errorhandle)}, 2000);     
        }
        else{
            console.log(response);
            console.log(status);
            errorhandle();
            arr.push(-1);
        }
      }
    });
  }
}
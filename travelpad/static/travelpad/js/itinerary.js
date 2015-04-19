var autocomplete;

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
    // place.geometry.location.lat() : latitude
    // place.geometry.location.lng() : longitude
    // place.name: place name
    // place.place_id: place id
    document.getElementById("abc").innerHTML = place.geometry.location.lat() + place.geometry.location.lng() + place.name + place.place_id;

  });
}
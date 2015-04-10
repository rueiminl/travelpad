from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^itineraries$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
    url(r'^update_itinerary$', 'travelpad.views_itineraries.update_itinerary', name='update_itinerary'),
    url(r'^update_itinerary/(?P<id>\d+)$', 'travelpad.views_itineraries.update_itinerary', name='update_itinerary'),
    url(r'^get_itinerary_photo$', 'travelpad.views_itineraries.get_itinerary_photo', name='get_itinerary_photo'),
    url(r'^get_itinerary_photo/(?P<id>\d+)$', 'travelpad.views_itineraries.get_itinerary_photo', name='get_itinerary_photo'),
    url(r'^get_itineraryform_json$', 'travelpad.views_itineraries.get_itineraryform_json', name='get_itineraryform_json'),
    url(r'^get_itineraryform_json/(?P<id>\d+)$', 'travelpad.views_itineraries.get_itineraryform_json', name='get_itineraryform_json'),
)

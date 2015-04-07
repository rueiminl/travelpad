from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^itinerary$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
    url(r'^itinerary/(?P<id>\d+)$', 'travelpad.views_itineraries.itinerary', name='itinerary'),
    url(r'^itineraries$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
)

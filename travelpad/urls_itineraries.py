from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^itinerary$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
    url(r'^itinerary/(?P<id>\d+)$', 'travelpad.views_itineraries.itinerary', name='itinerary'),
    url(r'^itineraries$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
    url(r'^update_itinerary_page/(?P<id>\d+)$', 'travelpad.views_itineraries.update_itinerary_page', name='update_itinerary_page'),
    url(r'^update_itinerary/(?P<id>\d+)$', 'travelpad.views_itineraries.update_itinerary', name='update_itinerary'),
)

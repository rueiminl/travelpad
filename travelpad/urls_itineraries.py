from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^itineraries$', 'travelpad.views_itineraries.itineraries', name='itineraries'),
    url(r'^add_itinerary_page$', 'travelpad.views_itineraries.add_itinerary_page', name='add_itinerary_page'),
    url(r'^update_itinerary_page/(?P<id>\d+)$', 'travelpad.views_itineraries.update_itinerary_page', name='update_itinerary_page'),
    url(r'^add_itinerary$', 'travelpad.views_itineraries.add_itinerary', name='add_itinerary'),
    url(r'^update_itinerary/(?P<id>\d+)$', 'travelpad.views_itineraries.update_itinerary', name='update_itinerary'),
)

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',

    url(r'^calendar$', 'travelpad.views_itinerary.calendar', name='calendar'),
    url(r'^get-calendar-events-json/(?P<itinerary_id>\d+)$', 'travelpad.views_itinerary.get_calendar_events_json', name = 'get-calendar-events-json'),
    
    url(r'^demo$', 'travelpad.views_itinerary.demo', name='demo'),
)

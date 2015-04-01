from django.conf.urls import patterns, include, url
urlpatterns = patterns('',

    url(r'^calendar$', 'travelpad.views_itinerary.calendar', name='calendar'),
    url(r'^get-calendar-events-json/(?P<itinerary_id>\d+)$', 'travelpad.views_itinerary.get_calendar_events_json', name = 'get-calendar-events-json'),
    
    url(r'^demo$', 'travelpad.views_itinerary.demo', name='demo'),
    
    url(r'^todo$', 'travelpad.views_itinerary.todo', name = 'todo'),
    url(r'^add-todo$', 'travelpad.views_itinerary.add_todo', name = 'add-todo'),
    
    url(r'^feed/(?P<itinerary_id>\d+)$', 'travelpad.views_itinerary.feed', name = 'feed'),
    url(r'^add-message$', 'travelpad.views_itinerary.add_message', name = 'add-message'),
    url(r'^add-reply$', 'travelpad.views_itinerary.add_reply', name = 'add-reply'),
    url(r'^get-message-json$', 'travelpad.views_itinerary.get_message_json', name = 'get-message-json'),
)

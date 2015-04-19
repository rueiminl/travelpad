from django.conf.urls import patterns, include, url
urlpatterns = patterns('',

    url(r'^demo$', 'travelpad.views_itinerary.demo', name='demo'),
    
    
    # Itinerary
    url(r'^itinerary/(?P<itinerary_id>\d+)$', 'travelpad.views_itinerary.itinerary', name = 'itinerary'),
    
    # Schedule
    url(r'^schedule$', 'travelpad.views_itinerary.schedule', name = 'schedule'),
    url(r'^get-calendar-events-json/(?P<itinerary_id>\d+)$', 'travelpad.views_itinerary.get_calendar_events_json', name = 'get-calendar-events-json'),
    
    
    # url(r'^add-todo$', 'travelpad.views_itinerary.add_todo', name = 'add-todo'),
#     url(r'^update-todo/(?P<todo_id>\d+)$', 'travelpad.views_itinerary.update_todo', name = 'update-todo'),
#     url(r'^delete-todo/(?P<todo_id>\d+)$', 'travelpad.views_itinerary.delete_todo', name = 'delete-todo'),
    
    url(r'^itinerary-json$', 'travelpad.views_itinerary.itinerary_json', name = 'itinerary-json'),
    
    # Todo
    url(r'^todo$', 'travelpad.views_itinerary.todo', name = 'todo'),
    # Todo API
    url(r'^todo-json$', 'travelpad.views_itinerary.todo_json', name = 'todo-json'),
    url(r'^todo-json/(?P<todo_id>\d+)$', 'travelpad.views_itinerary.todo_id_json', name = 'todo-id-json'),
    
    # # Participant API
#     url(r'^participant-json$', 'travelpad.views_itinerary.participant_json', name = 'participant-json'),
    
    
    # Feed
    url(r'^feed$', 'travelpad.views_itinerary.feed', name = 'feed'),
    url(r'^message-json$', 'travelpad.views_itinerary.message_json', name = 'message-json'),
    url(r'^reply-json$', 'travelpad.views_itinerary.reply_json', name = 'reply-json'),
    # url(r'^add-message$', 'travelpad.views_itinerary.add_message', name = 'add-message'),
#     url(r'^add-reply$', 'travelpad.views_itinerary.add_reply', name = 'add-reply'),
#     url(r'^get-message-json$', 'travelpad.views_itinerary.get_message_json', name = 'get-message-json'),
)

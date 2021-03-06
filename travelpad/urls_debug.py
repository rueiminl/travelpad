from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url('^debug$', 'travelpad.views_debug.debug', name='debug'),
    url('^debug_database$', 'travelpad.views_debug.debug_database', name='debug_database'),
    url('^debug_add_itinerary$', 'travelpad.views_debug.debug_add_itinerary', name='debug_add_itinerary'),
    url('^debug_add_user$', 'travelpad.views_debug.debug_add_user', name='debug_add_user'),
    url('^debug_add_travelpaduser$', 'travelpad.views_debug.debug_add_travelpaduser', name='debug_add_travelpaduser'),
    url('^debug_delete_itinerary$', 'travelpad.views_debug.debug_delete_itinerary', name='debug_delete_itinerary'),
    url(r'^debug_get_itinerary_photo/(?P<id>\d+)$', 'travelpad.views_debug.debug_get_itinerary_photo', name='debug_get_itinerary_photo'),
    url(r'^debug_get_travelpaduser_photo/(?P<id>\d+)$', 'travelpad.views_debug.debug_get_travelpaduser_photo', name='debug_get_travelpaduser_photo'),
)

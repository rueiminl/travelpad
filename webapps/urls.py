from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'', include('travelpad.urls')),
    url(r'', include('travelpad.urls_itinerary')),
    url(r'', include('travelpad.urls_event')),
    url(r'', include('travelpad.urls_map')),
    url(r'', include('travelpad.urls_login')),
    url(r'', include('travelpad.urls_debug')),
)

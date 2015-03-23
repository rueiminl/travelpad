from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'', include('travelpad.urls')),
    url(r'', include('travelpad.urls_itinerary')),
    url(r'', include('travelpad.urls_event')),
)

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',

    url('^calendar$', 'travelpad.views_itinerary.calendar', name='calendar'),
)

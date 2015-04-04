from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',

	url(r'^addevent$', 'travelpad.views_event.home_page', name='addevent'),
    url(r'^eventedit$', 'travelpad.views_event.eventedit', name='eventedit'),
    url(r'^getevent$', 'travelpad.views_event.getevent', name='getevent'),
)
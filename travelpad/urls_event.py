from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',

	url(r'^addevent$', 'travelpad.views_event.home_page', name='addevent'),
    url(r'^eventedit$', 'travelpad.views_event.eventedit', name='eventedit'),
    url(r'^eventedit_json$', 'travelpad.views_event.eventedit_json', name='eventedit-json'),
    url(r'^getevent$', 'travelpad.views_event.getevent', name='getevent'),
    url(r'^deleteevent$', 'travelpad.views_event.deleteevent', name='deleteevent'),
    url(r'^deleteevent_json$', 'travelpad.views_event.deleteevent_json', name='deleteevent-json'),
    url(r'^editeventtime$', 'travelpad.views_event.editeventtime', name='editeventtime'),
    url(r'^editeventtime_json$', 'travelpad.views_event.editeventtime_json', name='editeventtime-json'),
    
    url(r'^gettransport$', 'travelpad.views_event.gettransport', name='gettransport'),
    url(r'^updatetransport$', 'travelpad.views_event.updatetransport', name='updatetransport'),
)
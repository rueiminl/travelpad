from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^$', 'travelpad.views.test'),
    url(r'^todo$', 'travelpad.views.todo', name='todo'),
)

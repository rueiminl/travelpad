from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url('^$', 'travelpad.views.todolist', name='default'),
    url('^todolist$', 'travelpad.views.todolist', name='todolist'),
    url('^create_todo$', 'travelpad.views.create_todo', name='create_todo'),
    
    url('^calendar$', 'travelpad.views_schedule.calendar', name='calendar'),
)

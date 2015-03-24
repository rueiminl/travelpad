from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url('^$', 'travelpad.views.todolist', name='default'),
    url('^todolist$', 'travelpad.views.todolist', name='todolist'),
    url('^create_todo$', 'travelpad.views.create_todo', name='create_todo'),
    url(r'^update_todo/(?P<id>\d+)$', 'travelpad.views.update_todo', name='update_todo'),
    url(r'^delete_todo/(?P<id>\d+)$', 'travelpad.views.delete_todo', name='delete_todo'),
)

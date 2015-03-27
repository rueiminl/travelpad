from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'travelpad.views_login.login', name='login'),
    url(r'^register$', 'travelpad.views_login.register', name='register'),
    url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'travelpad.views_login.confirm', name='confirm'),

    )

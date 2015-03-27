from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'travelpad/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'travelpad.views_login.register', name='register'),
    url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'travelpad.views_login.confirm', name='confirm'),
    )

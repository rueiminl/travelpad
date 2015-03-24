from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^save-place$', 'travelpad.views_map.save_place', name='save_place'),
    url(r'^add-place$', 'travelpad.views_map.add_place', name='add_place'),
    )

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^profile$', 'travelpad.views_profile.profile', name='profile'),
    url(r'^update_profile$', 'travelpad.views_profile.update_profile', name='update_profile'),
    url(r'^get_user_photo$', 'travelpad.views_profile.get_user_photo', name='get_user_photo'),
    url(r'^get_user_photo/(?P<id>\d+)$', 'travelpad.views_profile.get_user_photo', name='get_user_photo'),
)

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^invitation$', 'travelpad.views_invitation.invitation', name='invitation'),
)

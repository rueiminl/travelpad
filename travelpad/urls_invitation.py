from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^participant-json$', 'travelpad.views_invitation.participant_json', name = 'participant-json'),
    url(r'^invitation$', 'travelpad.views_invitation.invitation', name='invitation'),
)

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('travelpad.urls')),
    url(r'^travelpad/', include('travelpad.urls')),
)

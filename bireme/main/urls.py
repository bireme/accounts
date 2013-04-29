from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^users/?$', 'main.views.users'),
    (r'^$', 'main.views.dashboard'),
)
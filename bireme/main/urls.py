from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^users/?$', 'main.views.users'),
    (r'^edit-user/(?P<user>\d+)/?$', 'main.views.edit_user'),
    (r'^$', 'main.views.dashboard'),
)
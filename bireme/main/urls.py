from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^users/?$', 'main.views.users'),
    (r'^edit-user/(?P<user>\d+)/?$', 'main.views.edit_user'),
    (r'^edit-user/change-user-role-service/?$', 'main.views.change_user_role_service'),
    (r'^$', 'main.views.dashboard'),
)
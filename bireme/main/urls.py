from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^users/?$', 'main.views.users'),
    (r'^users/new/?$', 'main.views.new_user'),
    (r'^users/edit/(?P<user>\d+)/?$', 'main.views.edit_user'),
    (r'^users/edit/change-user-role-service/?$', 'main.views.change_user_role_service'),
    
    (r'^$', 'main.views.dashboard'),
)
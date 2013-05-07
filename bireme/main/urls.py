from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^users/?$', 'main.views.users'),
    (r'^users/new/?$', 'main.views.new_user'),
    (r'^users/edit/(?P<user>\d+)/?$', 'main.views.edit_user'),
    
    (r'^networks/?$', 'main.views.networks'),
    (r'^network/new/?$', 'main.views.new_network'),
    (r'^network/edit/(?P<network>\d+)/?$', 'main.views.edit_network'),

    (r'^services/?$', 'main.views.services'),
    (r'^services/new/?$', 'main.views.new_service'),
    (r'^services/edit/(?P<service>\d+)/?$', 'main.views.edit_service'),

    (r'^roles/?$', 'main.views.roles'),
    (r'^roles/new/?$', 'main.views.new_role'),
    (r'^roles/edit/(?P<role>\d+)/?$', 'main.views.edit_role'),
    
    (r'^$', 'main.views.dashboard'),
)
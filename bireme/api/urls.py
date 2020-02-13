from django.conf.urls import patterns, url, include
from api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',

    url(r'^auth/', include(user_resource.urls)),

    (r'^users/edit/change-user-role-service/?$', 'api.views.change_user_role_service'),
    (r'^networks/edit/change-network-member/?$', 'api.views.change_network_member'),

    url(r'^get_ccs/?$', 'api.views.get_ccs'),
    url(r'^get_network_ccs/?$', 'api.views.get_network_ccs')
    
)
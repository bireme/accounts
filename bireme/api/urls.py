from django.urls import path, re_path, include
from api.api import UserResource

from api import views as api_views

user_resource = UserResource()

app_name = 'api'

urlpatterns = [
    re_path(r'^auth/', include(user_resource.urls)),
    re_path(r'^users/edit/change-user-role-service/?$', api_views.change_user_role_service, name='change_user_role_service'),
    re_path(r'^networks/edit/change-network-member/?$', api_views.change_network_member, name='change_network_member'),
    re_path(r'^get_ccs/?$', api_views.get_ccs, name='get_ccs'),
    re_path(r'^get_network_ccs/?$', api_views.get_network_ccs, name='get_network_ccs')
]
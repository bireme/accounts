from django.urls import path, re_path, include
from api.api import UserResource
from api import views as api_views

user_resource = UserResource()

app_name = 'api'

urlpatterns = [
    # Tastypie UserResource URLs (uses internal routing)
    re_path(r'^auth/', include(user_resource.urls)),

    # User role service management
    path('users/edit/change-user-role-service/', api_views.change_user_role_service, name='change_user_role_service'),

    # Network member management
    path('networks/edit/change-network-member/', api_views.change_network_member, name='change_network_member'),

    # Cooperative center APIs
    path('get_ccs/', api_views.get_ccs, name='get_ccs'),
    path('get_network_ccs/', api_views.get_network_ccs, name='get_network_ccs'),
]
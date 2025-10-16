from django.urls import path, re_path

from main import views as main_views

app_name = 'main'

urlpatterns = [
    # Dashboard - can use path() since it's just root
    path('', main_views.dashboard, name='dashboard'),

    # Users URLs
    path('users/', main_views.users, name='users'),
    path('users/new/', main_views.new_user, name='new_user'),
    path('users/edit/<int:user>/', main_views.edit_user, name='edit_user'),

    # Networks URLs
    path('networks/', main_views.networks, name='networks'),
    path('network/new/', main_views.new_network, name='new_network'),
    path('network/edit/<int:network>/', main_views.edit_network, name='edit_network'),

    # Services URLs
    path('services/', main_views.services, name='services'),
    path('services/new/', main_views.new_service, name='new_service'),
    path('services/edit/<int:service>/', main_views.edit_service, name='edit_service'),

    # Roles URLs
    path('roles/', main_views.roles, name='roles'),
    path('roles/new/', main_views.new_role, name='new_role'),
    path('roles/edit/<int:role>/', main_views.edit_role, name='edit_role'),
]
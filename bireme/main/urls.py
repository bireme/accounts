from django.urls import path, re_path

from main import views as main_views

app_name = 'main'

urlpatterns = [

    re_path(r'^$', main_views.dashboard, name='dashboard'),

    re_path(r'^users/?$', main_views.users, name='users'),
    re_path(r'^users/new/?$', main_views.new_user, name='new_user'),
    re_path(r'^users/edit/(?P<user>\d+)/?$', main_views.edit_user, name='edit_user'),

    re_path(r'^networks/?$', main_views.networks, name='networks'),
    re_path(r'^network/new/?$', main_views.new_network, name='new_network'),
    re_path(r'^network/edit/(?P<network>\d+)/?$', main_views.edit_network, name='edit_network'),

    re_path(r'^services/?$', main_views.services, name='services'),
    re_path(r'^services/new/?$', main_views.new_service, name='new_service'),
    re_path(r'^services/edit/(?P<service>\d+)/?$', main_views.edit_service, name='edit_service'),

    re_path(r'^roles/?$', main_views.roles, name='roles'),
    re_path(r'^roles/new/?$', main_views.new_role, name='new_role'),
    re_path(r'^roles/edit/(?P<role>\d+)/?$', main_views.edit_role, name='edit_role'),

]
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from registration import views as registration_views

urlpatterns = [
     re_path(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name='auth_login'),
     re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'registration/logout.html', 'next_page': '/'}, name='auth_logout'),
     re_path(r'^password/change/$', auth_views.PasswordChangeView.as_view(), {'template_name': "registration/change-password.html"}, name='auth_password_change'),
     re_path(r'^password/change/done/$', auth_views.PasswordChangeDoneView.as_view(), {'template_name': "registration/change-password-done.html"}, name='auth_password_change_done'),
     re_path(r'^password/reset/$', auth_views.PasswordResetView.as_view(), {'template_name': "registration/password-reset.html", 'email_template_name': 'registration/password_reset_email.html'}, name='auth_password_reset'),
     re_path(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': "registration/password-reset-confirm.html"}, name='auth_password_reset_confirm'),
     re_path(r'^password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), {'template_name': "registration/password-reset-complete.html"}, name='auth_password_reset_complete'),
     re_path(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': "registration/password-reset-done.html"}, name='auth_password_reset_done'),

     re_path(r'^change-profile/?$', registration_views.change_profile, name='change_profile'),
]
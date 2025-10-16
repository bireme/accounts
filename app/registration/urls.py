from django.urls import path
from django.contrib.auth import views as auth_views

from registration import views as registration_views

urlpatterns = [
    # Authentication views using Django's built-in auth views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='auth_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html', next_page='/'), name='auth_logout'),

    # Password change views
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'), name='auth_password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change-password-done.html'), name='auth_password_change_done'),

    # Password reset views
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html', email_template_name='registration/password_reset_email.html'), name='auth_password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'), name='auth_password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='auth_password_reset_complete'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='auth_password_reset_done'),

    # Custom registration views
    path('change-profile/', registration_views.change_profile, name='change_profile'),
]
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from registration.forms import ChangeProfileForm
from utils.email import StrictPasswordResetForm

logger = logging.getLogger(__name__)


class PasswordResetView(auth_views.PasswordResetView):
    """
    Password reset that logs email failures (with the address) instead of raising.

    Django deliberately does not tell anonymous users whether the email was
    sent (to avoid leaking which addresses exist), so on failure we log the
    error and still redirect to the "done" page.
    """
    form_class = StrictPasswordResetForm
    # project url names are prefixed with auth_, Django's default reverses 'password_reset_done'
    success_url = reverse_lazy('auth_password_reset_done')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception:
            logger.exception(
                "Failed to send password reset email to %s",
                form.cleaned_data.get('email'),
            )
            return HttpResponseRedirect(self.get_success_url())


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('auth_password_reset_complete')


@login_required
def change_profile(request):

    user = request.user
    output = {}

    form = ChangeProfileForm(instance=user)
    if request.POST:
        form = ChangeProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            output['alert'] = _("User successfully edited.")
            output['alerttype'] = "alert-success"

    output['user'] = user
    output['form'] = form

    return render(request, 'registration/change-profile.html', output)


def logout_view(request):
    """Custom logout view that handles GET requests like legacy Django versions"""
    logout(request)
    return render(request, 'registration/logout.html')

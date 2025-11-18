from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from registration.forms import ChangeProfileForm

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

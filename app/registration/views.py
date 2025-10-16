from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

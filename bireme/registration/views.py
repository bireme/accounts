#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import RequestContext
from utils.views import ACTIONS
from django.conf import settings
from datetime import datetime
from registration.forms import *
import mimetypes
import os

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

    return render_to_response('registration/change-profile.html', output, context_instance=RequestContext(request))
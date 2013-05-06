#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core import serializers
from utils.views import ACTIONS
from django.conf import settings
from datetime import datetime
from main.models import *
import mimetypes
import os
import json

@login_required
def get_ccs(request):

    ccs = CooperativeCenter.objects.all()
    if request.GET.get('code'):
        ccs = ccs.filter(code__istartswith=request.GET.get('code'))
    if request.GET.get('country'):
        ccs = ccs.filter(country__id=request.GET.get('country'))

    output = {'ccs': ccs}

    return render_to_response('api/get-ccs.html', output, context_instance=RequestContext(request))

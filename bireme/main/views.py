#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template import RequestContext
from django.conf import settings
from datetime import datetime
from models import *
import mimetypes
import os


@login_required
def index(request):
    
    user = request.user
    output = {}

    return render_to_response('main/index.html', output, context_instance=RequestContext(request))

def cookie_lang(request):

    language = request.REQUEST.get('language')
    request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = language
    request.session[settings.LANGUAGE_COOKIE_NAME] = language

    response = HttpResponse(language)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    return response    
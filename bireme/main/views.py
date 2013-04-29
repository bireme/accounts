#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import RequestContext
from django.conf import settings
from datetime import datetime
from models import *
import mimetypes
import os
from utils.views import ACTIONS as actions
from forms import *

@login_required
def dashboard(request):
    
    user = request.user
    output = {}

    return render_to_response('main/index.html', output, context_instance=RequestContext(request))

@login_required
def users(request):

    user = request.user
    cc = request.user.profile.cooperative_center
    output = {}

    # getting action parameters
    for key in actions.keys():
        if request.REQUEST.get(key):
            actions[key] = request.REQUEST.get(key)

    users = User.objects.filter(profile__cooperative_center=cc)
    users = users.order_by(actions["orderby"])
    if actions['order'] == "-":
        users = users.order_by("%s%s" % (actions["order"], actions["orderby"]))

    output['users'] = users
    output['actions'] = actions
    output['cc'] = cc

    return render_to_response('main/users.html', output, context_instance=RequestContext(request))

@login_required
def edit_user(request, user):

    user = get_object_or_404(User, id=user)
    cc = request.user.profile.cooperative_center
    output = {}

    services = Service.objects.all()
    user_role_services = UserRoleService.objects.filter(user=user)

    form = UserForm(instance=user)

    if request.POST:
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    output['form'] = form
    output['services'] = services
    output['user_roles'] = user_role_services

    return render_to_response('main/edit-user.html', output, context_instance=RequestContext(request))

@login_required
def change_user_role_service(request):

    output = {}

    user = request.REQUEST.get('user')
    role = request.REQUEST.get('role')
    service = request.REQUEST.get('service')

    user = get_object_or_404(User, id=user)
    role_service = get_object_or_404(RoleService, role__id=role, service__id=service)
    
    if request.REQUEST.get('checked') == "true":

        if not UserRoleService.objects.filter(user=user, role_service=role_service):
            role = UserRoleService(user=user, role_service=role_service)
            role.save()
            return HttpResponse(1)
    else:
        try:
            role = UserRoleService.objects.get(user=user, role_service=role_service)
            role.delete()
            return HttpResponse(1)
        except Exception as e:
            print e
            pass
    
    return HttpResponse(0)

        
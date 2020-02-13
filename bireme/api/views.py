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
from django.conf import settings
from utils.views import ACTIONS
from django.db.models import Q
from datetime import datetime
from main.models import *
import mimetypes
import os
import json

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

@login_required
def change_network_member(request):

    output = {}

    network = get_object_or_404(Network, id=request.REQUEST.get('network'))
    cc = get_object_or_404(CooperativeCenter, id=request.REQUEST.get('cc'))
    member, trash = NetworkMembership.objects.get_or_create(**{'network': network, 'cooperative_center': cc})

    if request.REQUEST.get('checked') == "true":
        member.save()
        return HttpResponse(1)
    else:
        member.delete()
        return HttpResponse(1)
    
    return HttpResponse(0)

@login_required
def get_ccs(request):

    ccs = CooperativeCenter.objects.all()
    output = {}
    members = []
    
    if request.GET.get('code'):
        ccs = ccs.filter(Q(code__istartswith=request.GET.get('code')) | Q(institution__icontains=request.GET.get('code')))
    
    if request.GET.get('country'):
        ccs = ccs.filter(country__id=request.GET.get('country'))

    if request.GET.get('network'):
        network = get_object_or_404(Network, id=request.GET.get('network'))
        members = [cc.id for cc in network.members.all()]

    output['ccs'] = ccs
    output['members'] = members

    return render_to_response('api/get-ccs.html', output, context_instance=RequestContext(request))

def get_network_ccs(request):

    output = {}
    members = []

    if request.GET.get('network'):
        network = get_object_or_404(Network, acronym__iexact=request.GET.get('network'))
        members = [cc.code for cc in network.members.all()]

    output['network_ccs'] = members

    data = json.dumps(output)
    return HttpResponse(data, content_type='application/json')

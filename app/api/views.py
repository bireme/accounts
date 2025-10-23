# coding: utf-8
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
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
    """
    AJAX view to manage user role service assignments.
    Adds or removes role service assignments for a user based on checkbox state.
    """
    output = {}

    user = request.GET.get('user')
    role = request.GET.get('role')
    service = request.GET.get('service')

    user = get_object_or_404(User, id=user)
    role_service = get_object_or_404(RoleService, role__id=role, service__id=service)

    if request.GET.get('checked') == "true":
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
            print(e)
            pass

    return HttpResponse(0)

@login_required
def change_network_member(request):
    """
    AJAX view to manage network membership.
    Adds or removes cooperative centers from networks based on checkbox state.
    """
    output = {}

    network = get_object_or_404(Network, id=request.GET.get('network'))
    cc = get_object_or_404(CooperativeCenter, id=request.GET.get('cc'))
    member, trash = NetworkMembership.objects.get_or_create(**{'network': network, 'cooperative_center': cc})

    if request.GET.get('checked') == "true":
        member.save()
        return HttpResponse(1)
    else:
        member.delete()
        return HttpResponse(1)

    return HttpResponse(0)

@login_required
def get_ccs(request):
    """
    View to retrieve and filter cooperative centers.
    Returns a rendered template with filtered cooperative centers.
    """
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

    return render(request, 'api/get-ccs.html', output)

def get_network_ccs(request):
    """
    JSON API view to retrieve cooperative centers for a specific network.
    Returns a JSON response with network cooperative center codes.
    """
    output = {}
    members = []

    if request.GET.get('network'):
        network = get_object_or_404(Network, acronym__iexact=request.GET.get('network'))
        members = [cc.code for cc in network.members.all()]

    output['network_ccs'] = members

    data = json.dumps(output)
    return HttpResponse(data, content_type='application/json')
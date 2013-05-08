#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import RequestContext
from utils.views import ACTIONS
from django.conf import settings
from datetime import datetime
from models import *
from forms import *
import mimetypes
import os

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
    actions = {}
    for key in ACTIONS.keys():
        if request.REQUEST.get(key):
            actions[key] = request.REQUEST.get(key)
        else:
            actions[key] = ACTIONS[key]


    users = User.objects.filter(profile__cooperative_center=cc, username__icontains=actions['s'])
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
            output['alert'] = _("User successfully edited.")
            output['alerttype'] = "alert-success"

    output['form'] = form
    output['user'] = user
    output['services'] = services
    output['user_roles'] = user_role_services

    return render_to_response('main/edit-user.html', output, context_instance=RequestContext(request))

@login_required
def new_user(request):

    user = request.user
    cc = request.user.profile.cooperative_center
    output = {}

    services = Service.objects.all()
    user_role_services = UserRoleService.objects.filter(user=user)

    form = UserForm()

    if request.POST:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            
            # saving user
            new_user = form.save()

            # saving profile
            new_user.profile.cooperative_center = cc
            new_user.profile.save()

            output['alert'] = _("User successfully edited.")
            output['alerttype'] = "alert-success"

            return redirect("%s/#!tab-permissions" % reverse("main.views.edit_user", args=[new_user.id]))

    output['form'] = form
    output['services'] = services
    output['user_roles'] = user_role_services
    output['is_new'] = True

    return render_to_response('main/edit-user.html', output, context_instance=RequestContext(request))

@login_required
def networks(request):

    user = request.user
    output = {}

    # getting action parameters
    actions = {}
    for key in ACTIONS.keys():
        if request.REQUEST.get(key):
            actions[key] = request.REQUEST.get(key)
        else:
            actions[key] = ACTIONS[key]

    networks = Network.objects.filter(acronym__icontains=actions['s'])

    networks = networks.order_by(actions["orderby"])
    if actions['order'] == "-":
        networks = networks.order_by("%s%s" % (actions["order"], actions["orderby"]))

    output['networks'] = networks
    output['actions'] = actions

    return render_to_response('main/networks.html', output, context_instance=RequestContext(request))

@login_required
def edit_network(request, network):

    network = get_object_or_404(Network, id=network)
    members = [cc.id for cc in network.members.all()]
    output = {}

    form = NetworkForm(instance=network)

    ccs = CooperativeCenter.objects.all()
    if network.type == 'national' or network.country:
        cc_country = network.country.id
        ccs = ccs.filter(country=network.country)

    if request.POST:
        form = NetworkForm(request.POST, request.FILES, instance=network)
        if form.is_valid():
            form.save()
            output['alert'] = _("Network successfully edited.")
            output['alerttype'] = "alert-success"

    output['form'] = form
    output['network'] = network
    output['ccs'] = ccs
    output['cc_country'] = cc_country
    output['members'] = members
    
    return render_to_response('main/edit-network.html', output, context_instance=RequestContext(request))

@login_required
def new_network(request):

    output = {}

    network = Network(creator=request.user)
    form = NetworkForm(instance=network)

    if request.POST:
        form = NetworkForm(request.POST, request.FILES, instance=network)
        
        if form.is_valid():
            form.save()
            output['alert'] = _("Network successfully created.")
            output['alerttype'] = "alert-success"

    output['is_new'] = True
    output['form'] = form
    output['network'] = network
    
    return render_to_response('main/edit-network.html', output, context_instance=RequestContext(request))


@login_required
def services(request):

    user = request.user
    output = {}

    # getting action parameters
    actions = {}
    for key in ACTIONS.keys():
        if request.REQUEST.get(key):
            actions[key] = request.REQUEST.get(key)
        else:
            actions[key] = ACTIONS[key]


    services = Service.objects.filter(name__icontains=actions['s'])

    services = services.order_by(actions["orderby"])
    if actions['order'] == "-":
        services = services.order_by("%s%s" % (actions["order"], actions["orderby"]))

    output['services'] = services
    output['actions'] = actions

    return render_to_response('main/services.html', output, context_instance=RequestContext(request))


@login_required
def edit_service(request, service):

    service = get_object_or_404(Service, id=service)   
    roles = Role.objects.all() 
    service_roles = RoleService.objects.filter(service=service)
    
    role_associated_list = request.REQUEST.getlist('roles_associated')

    output = {}

    form = ServiceForm(instance=service)

    if request.POST:
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            if role_associated_list:
                # delete previous service/roles association
                previous_service_roles = RoleService.objects.filter(service=service)
                previous_service_roles.delete()

                # save/update service/role association
                for role_id in role_associated_list:
                    role = Role.objects.get(pk=role_id)
                    role_service = RoleService(service=service, role=role)
                    role_service.save() 
           

            output['alert'] = _("Service successfully edited.")
            output['alerttype'] = "alert-success"

    output['form'] = form
    output['roles'] = roles
    output['service_roles'] = service_roles
    output['service'] = service
    
    return render_to_response('main/edit-service.html', output, context_instance=RequestContext(request))

@login_required
def new_service(request):

    output = {}

    service = Service(creator=request.user)
    roles = Role.objects.all()
    form = ServiceForm(instance=service)

    if request.POST:
        form =ServiceForm(request.POST, request.FILES, instance=service)
        
        if form.is_valid():
            form.save()
            output['alert'] = _("Service successfully created.")
            output['alerttype'] = "alert-success"

    output['is_new'] = True
    output['form'] = form
    output['roles'] = roles
    output['service'] = service
    
    return render_to_response('main/edit-service.html', output, context_instance=RequestContext(request))

@login_required
def roles(request):

    user = request.user
    output = {}

    # getting action parameters
    actions = {}
    for key in ACTIONS.keys():
        actions[key] = ACTIONS[key]
        if request.REQUEST.get(key):
            actions[key] = request.REQUEST.get(key)       

    roles = Role.objects.filter(name__icontains=actions['s'])
    roles = roles.order_by(actions["orderby"])
    if actions['order'] == "-":
        roles = roles.order_by("%s%s" % (actions["order"], actions["orderby"]))

    output['roles'] = roles
    output['actions'] = actions

    return render_to_response('main/roles.html', output, context_instance=RequestContext(request))

@login_required
def edit_role(request, role):

    role = get_object_or_404(Role, id=role)    
    output = {}

    form = RoleForm(instance=role)

    if request.POST:
        form = RoleForm(request.POST, request.FILES, instance=role)
        if form.is_valid():
            form.save()
            output['alert'] = _("Role successfully edited.")
            output['alerttype'] = "alert-success"

    output['form'] = form
    output['role'] = role
    
    return render_to_response('main/edit-role.html', output, context_instance=RequestContext(request))

@login_required
def new_role(request):

    output = {}

    role = Role(creator=request.user)
    form = RoleForm(instance=role)

    if request.POST:
        form = RoleForm(request.POST, request.FILES, instance=role)
        
        if form.is_valid():
            form.save()
            output['alert'] = _("Role successfully created.")
            output['alerttype'] = "alert-success"

    output['is_new'] = True
    output['form'] = form
    output['role'] = role
    
    return render_to_response('main/edit-role.html', output, context_instance=RequestContext(request))

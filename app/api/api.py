from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.urls import re_path
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource

from main.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'

    def prepend_urls(self):
        return [
            re_path(r"^login%s$" % trailing_slash(), self.wrap_view('login'), name="api_login"),
            re_path(r'^logout%s$' % trailing_slash(), self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')
        service = data.get('service', '')
        list_network_ccs = data.get('list_network_ccs', True)
        list_responsible = data.get('list_responsible', False)
        roles = []
        service_role = []
        network = []
        networks_responsible = []
        ccs_networks_responsible = []
        ccs = set()
        ccs_by_network = dict()

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                cc = user.profile.cooperative_center
                user_type = user.profile.type

                # if not have cooperative center code is unauthorized
                if not hasattr(cc, 'code'):
                    return self.create_response(request, {'success': False, 'reason': "user has not a cooperative center code"}, HttpUnauthorized)

                networks = [network.acronym for network in cc.network_set.all()]

                if list_responsible:
                    networks_managed = Network.objects.filter(responsible=cc)
                    networks_responsible = [network.acronym for network in networks_managed]

                    for net_managed in networks_managed:
                        ccs_networks_responsible.extend( [member.code for member in net_managed.members.all()] )

                # if service is informed return only user role of the service
                # otherwise return a list of service/role associated with the user
                if service != '':
                    roles = [role.role_service.role.acronym for role in
                        UserRoleService.objects.filter(user=user, role_service__service__acronym=service)]
                else:
                    service_role = [ {role.role_service.service.acronym: role.role_service.role.acronym} for role in
                        UserRoleService.objects.filter(user=user)]


                # if service is informed and user doesn't have role in the service return unauthorized
                if service != '' and not roles:
                    return self.create_response(request, {'success': False, 'reason': "user has no role in service"}, HttpUnauthorized)

                if list_network_ccs:
                    # loop at all networks that user cc participate (ex. BR9.9 participate of 3 networks)
                    network_list = cc.network_set.all()
                    for network in network_list:
                        # return all cc codes of current network
                        network_cc_list = network.list_members()
                        # add network list to ccs list (without duplications)
                        ccs.update(network_cc_list)
                        # add network list to dict contain network acronym and ccs list
                        ccs_by_network.update({network.acronym: network_cc_list})

                output = {
                    'success': True,
                    'data': {
                        'user': user,
                        'user_type': user_type,
                        'cc': cc,
                        'role': roles,
                        'service_role': service_role,
                        'networks' : networks,
                        'ccs_by_network': ccs_by_network,
                    }
                }
                if list_network_ccs:
                    output['data']['ccs'] = list(ccs)

                if list_responsible:
                    output['data']['networks_responsible'] = networks_responsible
                    output['data']['ccs_networks_responsible'] = ccs_networks_responsible


                if user.profile.type == "advanced":
                    # check if this user is network owner
                    network_owners = cc.network_set.all().filter(responsible=cc)

                    if network_owners:
                        # getting all centers that this center may see
                        for network in network_owners:
                            ccs.update(network.list_members())

                    output['data']['ccs'] = list(ccs)
                    output['data']['networks'] = networks

                login(request, user)

                return self.create_response(request, output)
            else:
                return self.create_response(request, {'success': False, 'reason': 'user not active'}, HttpForbidden)
        else:
            return self.create_response(request, {'success': False, 'reason': 'user or password incorrect'}, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)
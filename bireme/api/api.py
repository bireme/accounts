from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
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
            url(r"^login%s$" % trailing_slash(), self.wrap_view('login'), name="api_login"),
            url(r'^logout%s$' % trailing_slash(), self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')
        service = data.get('service', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:

                cc = user.profile.cooperative_center
                ccs = [cc.code]
                networks = [network.acronym for network in cc.network_set.all()]
                roles = [role.role_service.role.acronym for role in UserRoleService.objects.filter(user=user, role_service__service__acronym=service)]
                
                # if not have roles in this service, is unauthorized
                if not roles:
                    return self.create_response(request, {'success': False, 'reason': "user has no role in service"}, HttpUnauthorized)
                
                output = {
                    'success': True,
                    'data': {
                        'user': user,
                        'cc': cc,
                        'ccs': ccs,
                        'role': roles,
                    }
                }

                if user.profile.type == "advanced":
                    
                    # check if this user is network owner
                    network_owners = cc.network_set.all().filter(responsible=cc)
                    
                    if network_owners:
                        # getting all centers that this center may see
                        for network in network_owners:
                            ccs += network.list_members()
                        ccs = list(set(ccs))

                    output['ccs'] = ccs
                    output['networks'] = networks

                login(request, user)
                return self.create_response(request, output)
            else:
                return self.create_response(request, {'success': False, 'reason': 'user not active'}, HttpForbidden)
        else:
            return self.create_response(request, {'success': False, 'reason': 'user or password incorrect'}, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)
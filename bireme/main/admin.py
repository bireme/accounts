from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import *
from utils.admin import GenericAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserRoleAdmin(admin.TabularInline):
    model = UserRoleService
    extra = 0

# Define a new User admin
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_active')}
        ),
    )
    inlines = (ProfileInline, UserRoleAdmin )


class RoleLocalAdmin(admin.TabularInline):
    model = RoleLocal
    extra = 0

class RoleAdmin(GenericAdmin):
    model = Role
    inlines = [RoleLocalAdmin, ]


class ServiceLocalAdmin(admin.TabularInline):
    model = ServiceLocal
    extra = 0

class ServiceAdmin(GenericAdmin):
    model = Service
    inlines = [ServiceLocalAdmin,]

class CooperativeCenterAdmin(GenericAdmin):
    model = CooperativeCenter
    #raw_id_fields = ("country", )


class TopicLocalAdmin(admin.TabularInline):
    model = TopicLocal
    extra = 0

class TopicAdmin(GenericAdmin):
    model = Topic
    inlines = [TopicLocalAdmin,]


class NetworkAdmin(GenericAdmin):
    model = Network 
    list_display = ['acronym', 'type', 'responsible', 'country']
    list_filter = ['type', ]


admin.site.register(Role, RoleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CooperativeCenter, CooperativeCenterAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(NetworkMembership)
admin.site.register(RoleService)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import *
from utils.admin import GenericAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserRoleAdmin(admin.TabularInline):
    model = UserRoleService
    extra = 0

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, UserRoleAdmin )
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_active', "is_staff", "is_superuser")}),
        ("Information", {'fields': ('first_name', "last_name", 'last_login', "date_joined")}),
    )

    readonly_fields = ("last_login", "date_joined")

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
    readonly_fields = [field.name for field in model._meta.fields]

    list_display = ['code', 'country']
    list_filter = ['country', ]
    search_fields = ['code']

    def has_delete_permission(self, request, obj=None):
        return False
    

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
    raw_id_fields = ['responsible', ]

class NetworkMembershipAdmin(admin.ModelAdmin):
    model = NetworkMembership
    list_display = ['cooperative_center', 'network']
    list_filter = ['network', 'network__type']


admin.site.register(Role, RoleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CooperativeCenter, CooperativeCenterAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(NetworkMembership, NetworkMembershipAdmin)
admin.site.register(RoleService)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


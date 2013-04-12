from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


class GenericAdmin(admin.ModelAdmin):
    exclude = ('created', 'creator', 'updated', 'updater')

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updater = request.user
            else:
                obj.creator = request.user
                obj.updater = request.user
        obj.save()    


class CooperativeCenterAdmin(GenericAdmin):
    model = CooperativeCenter
    #raw_id_fields = ("country", )
    

class CountryLocalAdmin(admin.TabularInline):
    model = CountryLocal
    extra = 0

class CountryAdmin(GenericAdmin):
    model = Country
    inlines = [CountryLocalAdmin,]

class TopicLocalAdmin(admin.TabularInline):
    model = TopicLocal
    extra = 0


class TopicAdmin(GenericAdmin):
    model = Topic
    inlines = [TopicLocalAdmin,]


class NetworkAdmin(GenericAdmin):
    model = Network


admin.site.register(CooperativeCenter, CooperativeCenterAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Network, NetworkAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


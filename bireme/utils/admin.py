from django.contrib import admin
from django.contrib.admin.models import LogEntry
# from django.contrib.contenttypes.models import ContentType

from models import *


class GenericAdmin(admin.ModelAdmin):
    exclude = ()

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updater = request.user
            else:
                obj.creator = request.user
                obj.updater = request.user
        obj.save()


class CountryLocalAdmin(admin.TabularInline):
    model = CountryLocal
    extra = 0


class CountryAdmin(GenericAdmin):
    model = Country
    inlines = [CountryLocalAdmin,]
    search_fields = list_display = ['code', 'name']


# class ContentTypeAdmin(GenericAdmin):
#     model = ContentType
#     list_display = ['pk', 'name']
#     search_fields = ['name',]


class LogEntryAdmin(GenericAdmin):
    model = LogEntry


admin.site.register(Country, CountryAdmin)
# admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

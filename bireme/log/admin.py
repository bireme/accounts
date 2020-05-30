# -*- coding: utf-8 -*-
import datetime
from django.contrib import admin
from django.contrib.admin.models import LogEntry

class LogEntryModelAdmin(admin.ModelAdmin):
    list_display = ('action_time','user','content_type','object_repr','change_message','action_flag')
    list_filter = ['action_time','user','content_type']
    ordering = ('-action_time',)

admin.site.unregister(LogEntry)
admin.site.register(LogEntry, LogEntryModelAdmin)

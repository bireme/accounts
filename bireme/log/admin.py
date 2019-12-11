#-*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import LogReview


class LogReviewAdmin(admin.ModelAdmin):
    model = LogReview
    date_hierarchy = 'created'
    raw_id_fields = ('log',)

admin.site.register(LogReview, LogReviewAdmin)

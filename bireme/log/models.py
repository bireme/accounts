#-*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _

from utils.models import Generic

REVISION_CHOICES = (
    (-1, _('Not approved')),
    (1, _('Approved')),
)


class LogReview(Generic):
    log = models.ForeignKey(LogEntry)
    status = models.SmallIntegerField(_('Status'), choices=REVISION_CHOICES, null=True)

    class Meta:
        verbose_name = "Log Review"
        verbose_name_plural = "Log Reviews"

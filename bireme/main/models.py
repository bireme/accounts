#-*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from log.mixins import AuditLog
from utils.models import Generic, Country, LANGUAGES_CHOICES


class Profile(models.Model, AuditLog):
    USER_TYPE_CHOICES = (
        ('basic', _('Basic')),
        ('advanced', _('Advanced')),
    )

    cooperative_center = models.ForeignKey("CooperativeCenter", verbose_name=_("Cooperative Center"), null=True, blank=True)
    user = models.OneToOneField(User, verbose_name="user", primary_key=True) # allow extension of default django User
    type = models.CharField(_("type"), max_length=30, choices=USER_TYPE_CHOICES, default="basic")

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def get_role_services(self):
        services = {}
        for item in UserRoleService.objects.filter(user=self):
            try:
                services[item.role_service.service].append(item.role_service.role)
            except:
                services[item.role_service.service] = [item.role_service.role]
        return services

    def is_basic(self):
        if self.type == "basic":
            return True
        return False

    def is_advanced(self):
        if self.type == "advanced":
            return True
        return False


class Role(Generic, AuditLog):
    acronym = models.CharField(_('acronym'), max_length=55)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __unicode__(self):
        return unicode(self.name)


class RoleLocal(models.Model, AuditLog):
    role = models.ForeignKey(Role, verbose_name=_("role"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        verbose_name = _("role translation")
        verbose_name_plural = _("role translations")

    def unicode(self):
        return unicode(self.description)


class Service(Generic, AuditLog):
    acronym = models.CharField(_('acronym'), max_length=55)
    name = models.CharField(_('name'), max_length=255)
    roles = models.ManyToManyField("Role", through='RoleService')

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __unicode__(self):
        return unicode(self.acronym)


class ServiceLocal(models.Model, AuditLog):
    service = models.ForeignKey(Service, verbose_name=_("service"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _("service translation")
        verbose_name_plural = _("service translations")


class RoleService(models.Model, AuditLog):
    role = models.ForeignKey(Role)
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return unicode("%s | %s" % (self.role, self.service))


class UserRoleService(models.Model, AuditLog):
    user = models.ForeignKey(User)
    role_service = models.ForeignKey(RoleService)


class CooperativeCenter(Generic, AuditLog):
    code = models.CharField(_("code"), max_length=55, unique=True)
    country = models.ForeignKey(Country, verbose_name=_("country"))
    institution = models.TextField(_("institution"), blank=True, null=True)

    class Meta:
        verbose_name = _("cooperative center")
        verbose_name_plural = _("cooperative centers")

    def __unicode__(self):
        return unicode(self.code)


class Topic(Generic, AuditLog):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __unicode__(self):
        return unicode(self.name)


class TopicLocal(models.Model, AuditLog):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])

    class Meta:
        verbose_name = _("topic translation")
        verbose_name_plural = _("topic translations")


class Network(Generic, AuditLog):
    NETWORK_TYPE_CHOICES = (
        ('national', _('National')),
        ('thematic', _('Thematic')),
        ('institutional', _('Institutional')),
    )

    acronym = models.CharField(_('acronym'), max_length=255)
    responsible = models.ForeignKey(CooperativeCenter, verbose_name=_("Responsible Cooperative Center"), related_name="+")
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), blank=True, null=True)
    type = models.CharField(_("type"), max_length=30, choices=NETWORK_TYPE_CHOICES, blank=True)
    country = models.ForeignKey(Country, verbose_name=_("country"), blank=True, null=True)
    members = models.ManyToManyField(CooperativeCenter, through='NetworkMembership')

    class Meta:
        verbose_name = _("network")
        verbose_name_plural = _("networks")

    def __unicode__(self):
        return unicode(self.acronym)

    def list_members(self):
        return [item.code for item in self.members.all()]


class NetworkMembership(models.Model, AuditLog):
    network = models.ForeignKey(Network)
    cooperative_center = models.ForeignKey(CooperativeCenter, verbose_name=_("Cooperative Center"))

    class Meta:
        verbose_name = _("Network Membership")
        verbose_name_plural = _("Network Memberships")

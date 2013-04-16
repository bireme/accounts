#! coding: utf-8

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models

# Create your models here.

LANGUAGES_CHOICES = (
    ('en', 'English'),                  # default language 
    ('pt-br', 'Brazilian Portuguese'),
    ('es', 'Spanish'),
)  

class Generic(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(_("created"), default=datetime.now())
    updated = models.DateTimeField(_("updated"), default=datetime.now())
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+")
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+")

    def save(self):
        self.updated = datetime.now()
        super(Generic, self).save()


class Profile(models.Model):

    USER_TYPE_CHOICES = (
        ('basic', _('Basic')),
        ('advanced', _('Advanced')),
        ('superuser', _('Super User')),
    )

    user = models.OneToOneField(User)       # allow extension of default django User
    type = models.CharField(_("type"), max_length=30, choices=USER_TYPE_CHOICES)
    

class Role(Generic):
    name = models.CharField(_('name'), max_length=55)
    description = models.TextField(_("description"), null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class RoleLocal(models.Model):

    role = models.ForeignKey(Role, verbose_name=_("role"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    description = models.TextField(_("description"), null=True, blank=True)


class Service(Generic):
    acronym = models.CharField(_('acronym'), max_length=55) 
    name = models.CharField(_('name'), max_length=255)

    def __unicode__(self):
        return unicode(self.name)


class ServiceLocal(models.Model):

    service = models.ForeignKey(Service, verbose_name=_("service"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_('name'), max_length=255)


class RoleService(models.Model):

    role = models.ForeignKey(Role)
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return "%s | %s" % (self.role, self.service)


class UserRoleService(models.Model):

    user = models.ForeignKey(User)
    role_service = models.ForeignKey(RoleService)


class Country(Generic):
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    code = models.CharField(_('code'), max_length=55)
    name = models.CharField(_('name'), max_length=255)

    def __unicode__(self):
        return unicode(self.name)


class CountryLocal(models.Model):

    class Meta:
        verbose_name = "Country Translation"
        verbose_name_plural = "Country Translations"

    country = models.ForeignKey(Country, verbose_name=_("country"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_("name"), max_length=255)
    

class CooperativeCenter(Generic):
    class Meta:
        verbose_name = "Cooperative Center"
        verbose_name_plural = "Cooperative Center's"

    code = models.CharField('code', max_length=55)
    country = models.ForeignKey(Country, verbose_name=_("country"))

    def __unicode__(self):
        return unicode(self.code)

class Topic(Generic):

    name = models.CharField('name', max_length=255)

    def __unicode__(self):
        return unicode(self.name
)

class TopicLocal(models.Model):

    topic = models.ForeignKey(Topic, verbose_name=_("topic"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])



class Network(Generic):

    NETWORK_TYPE_CHOICES = (
        ('national', _('National')),
        ('thematic', _('Thematic')),
    )

    acronym = models.CharField(_('acronym'), max_length=255)
    country = models.ForeignKey(Country, verbose_name=_("country"), blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), blank=True, null=True)
    type = models.CharField(_("type"), max_length=30, choices=NETWORK_TYPE_CHOICES, blank=True)
    members = models.ManyToManyField(CooperativeCenter, through='NetworkMembership')

    def __unicode__(self):
        return unicode(self.acronym)


class NetworkMembership(models.Model):
    
    class Meta:
        verbose_name = "Network Membership"
        verbose_name_plural = "Network Membership's"

    network = models.ForeignKey(Network)
    cooperative_center = models.ForeignKey(CooperativeCenter, verbose_name=_("Cooperative Center"))



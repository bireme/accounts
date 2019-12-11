#-*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _
from pytz import utc

LANGUAGES_CHOICES = (
    ('en', 'English'), # default language
    ('pt-br', 'Brazilian Portuguese'),
    ('es', 'Spanish'),
)

class Generic(models.Model):
    created = models.DateTimeField(_("created"), default=datetime.now(utc))
    updated = models.DateTimeField(_("updated"), default=datetime.now(utc))
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+")
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+")

    class Meta:
        abstract = True

    def save(self):
        self.updated = datetime.now()
        super(Generic, self).save()


class Country(Generic):
    code = models.CharField(_('code'), max_length=55)
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __unicode__(self):
        language = get_language()
        try:
            translation = self.countrylocal_set.get(language=language)
            return unicode(translation.name)
        except CountryLocal.DoesNotExist:
            return unicode(self.name)


class CountryLocal(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("country"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = "Country Translation"
        verbose_name_plural = "Country Translations"

    country = models.ForeignKey(Country, verbose_name=_("country"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_("name"), max_length=255)

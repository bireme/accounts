from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone

LANGUAGES_CHOICES = (
    ('en', 'English'), # default language
    ('pt-br', 'Brazilian Portuguese'),
    ('es', 'Spanish'),
)

class Generic(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(_("created"), default=timezone.now, editable=False)
    updated = models.DateTimeField(_("updated"), default=timezone.now, editable=False)
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+", on_delete=models.PROTECT)
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+", on_delete=models.PROTECT)

    def save(self):
        self.updated = timezone.now()
        super(Generic, self).save()

class Country(Generic):

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    code = models.CharField(_('code'), max_length=55)
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return str(self.name)


class CountryLocal(models.Model):

    class Meta:
        verbose_name = "Country Translation"
        verbose_name_plural = "Country Translations"

    country = models.ForeignKey(Country, verbose_name=_("country"), on_delete=models.CASCADE)
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES[1:])
    name = models.CharField(_("name"), max_length=255)
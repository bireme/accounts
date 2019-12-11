#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from main.models import CooperativeCenter, Network, NetworkMembership, Profile


def append_memberships(sender, instance, created, **kwargs):
    """
    If the network type is national and was included your country,
    automatically appends all centers that have that country too.
    """
    if created:
        if instance.type == 'national' and instance.country:
            for cc in CooperativeCenter.objects.filter(country=instance.country):
                nm = NetworkMembership(network=instance, cooperative_center=cc)
                nm.save()

post_save.connect(append_memberships, sender=Network, dispatch_uid="some.unique.string.id")


def create_profile(sender, instance, created, **kwargs):
    """
    Creates automatically and profile
    """
    if created:
        profile = Profile(user=instance)
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="user_create_profile")

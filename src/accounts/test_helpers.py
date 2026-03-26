from django.contrib.auth.models import User
from utils.models import Country, CountryLocal
from main.models import (
    Profile, Role, Service, RoleService, UserRoleService,
    CooperativeCenter, Topic, Network, NetworkMembership,
)


def create_country(code="BR", name="Brazil"):
    return Country.objects.create(code=code, name=name)


def create_country_local(country=None, language="pt-br", name="Brasil"):
    if country is None:
        country = create_country()
    return CountryLocal.objects.create(country=country, language=language, name=name)


def create_cooperative_center(code="BR1.1", country=None, institution="Test Institution"):
    if country is None:
        country = create_country()
    return CooperativeCenter.objects.create(code=code, country=country, institution=institution)


def create_user(username="testuser", email="test@example.com", password="TestPass123!", is_superuser=False, is_active=True):
    user = User.objects.create_user(
        username=username, email=email, password=password,
        is_superuser=is_superuser, is_staff=is_superuser, is_active=is_active,
    )
    return user


def create_basic_user(username="basicuser", email="basic@example.com", cc=None):
    user = create_user(username=username, email=email)
    user.profile.type = "basic"
    if cc:
        user.profile.cooperative_center = cc
    user.profile.save()
    return user


def create_advanced_user(username="advuser", email="adv@example.com", cc=None):
    user = create_user(username=username, email=email)
    user.profile.type = "advanced"
    if cc:
        user.profile.cooperative_center = cc
    user.profile.save()
    return user


def create_superuser(username="admin", email="admin@example.com"):
    return create_user(username=username, email=email, is_superuser=True)


def create_role(acronym="EDR", name="Editor", description="Editor role"):
    return Role.objects.create(acronym=acronym, name=name, description=description)


def create_service(acronym="FI", name="FI-Admin"):
    return Service.objects.create(acronym=acronym, name=name)


def create_role_service(role=None, service=None):
    if role is None:
        role = create_role()
    if service is None:
        service = create_service()
    return RoleService.objects.create(role=role, service=service)


def create_topic(name="Health"):
    return Topic.objects.create(name=name)


def create_network(acronym="TestNet", responsible=None, topic=None, network_type="national", country=None):
    if responsible is None:
        responsible = create_cooperative_center()
    if country is None:
        country = responsible.country
    return Network.objects.create(
        acronym=acronym, responsible=responsible, topic=topic,
        type=network_type, country=country,
    )

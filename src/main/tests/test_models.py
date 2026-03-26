from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from main.models import (
    Profile, Role, RoleLocal, Service, ServiceLocal,
    RoleService, UserRoleService, CooperativeCenter,
    Topic, TopicLocal, Network, NetworkMembership,
)
from accounts.test_helpers import (
    create_country, create_cooperative_center, create_user,
    create_role, create_service, create_role_service,
    create_topic, create_network,
)


class ProfileModelTest(TestCase):

    def test_profile_auto_created_on_user_creation(self):
        user = create_user()
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, Profile)

    def test_profile_default_type_is_basic(self):
        user = create_user()
        self.assertEqual(user.profile.type, "basic")

    def test_profile_is_basic(self):
        user = create_user()
        user.profile.type = "basic"
        self.assertTrue(user.profile.is_basic())

    def test_profile_is_advanced(self):
        user = create_user()
        user.profile.type = "advanced"
        self.assertTrue(user.profile.is_advanced())

    def test_profile_is_not_basic_when_advanced(self):
        user = create_user()
        user.profile.type = "advanced"
        self.assertFalse(user.profile.is_basic())

    def test_profile_get_role_services(self):
        user = create_user()
        role = create_role()
        service = create_service()
        rs = create_role_service(role=role, service=service)
        UserRoleService.objects.create(user=user, role_service=rs)

        result = user.profile.get_role_services()
        self.assertIn(service, result)
        self.assertIn(role, result[service])

    def test_profile_get_role_services_empty(self):
        user = create_user()
        result = user.profile.get_role_services()
        self.assertEqual(result, {})

    def test_profile_cooperative_center(self):
        user = create_user()
        cc = create_cooperative_center()
        user.profile.cooperative_center = cc
        user.profile.save()
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.cooperative_center, cc)


class RoleModelTest(TestCase):

    def test_create_role(self):
        role = create_role(acronym="ADM", name="Administrator", description="Admin role")
        self.assertEqual(role.acronym, "ADM")
        self.assertEqual(role.name, "Administrator")
        self.assertEqual(role.description, "Admin role")

    def test_role_str(self):
        role = create_role(name="Editor")
        self.assertEqual(str(role), "Editor")


class RoleLocalModelTest(TestCase):

    def test_create_role_local(self):
        role = create_role()
        local = RoleLocal.objects.create(role=role, language="pt-br", name="Editor", description="Papel de editor")
        self.assertEqual(local.role, role)
        self.assertEqual(local.language, "pt-br")

    def test_role_local_str(self):
        role = create_role()
        local = RoleLocal.objects.create(role=role, language="es", name="Editor", description="Rol de editor")
        self.assertEqual(str(local), "Rol de editor")

    def test_role_local_cascade_delete(self):
        role = create_role()
        RoleLocal.objects.create(role=role, language="pt-br", name="Editor")
        self.assertEqual(RoleLocal.objects.count(), 1)
        role.delete()
        self.assertEqual(RoleLocal.objects.count(), 0)


class ServiceModelTest(TestCase):

    def test_create_service(self):
        service = create_service(acronym="FI", name="FI-Admin")
        self.assertEqual(service.acronym, "FI")
        self.assertEqual(service.name, "FI-Admin")

    def test_service_str(self):
        service = create_service(acronym="FI")
        self.assertEqual(str(service), "FI")

    def test_service_roles_m2m_through(self):
        role = create_role()
        service = create_service()
        RoleService.objects.create(role=role, service=service)
        self.assertIn(role, service.roles.all())


class ServiceLocalModelTest(TestCase):

    def test_create_service_local(self):
        service = create_service()
        local = ServiceLocal.objects.create(service=service, language="es", name="FI-Admin")
        self.assertEqual(local.service, service)


class RoleServiceModelTest(TestCase):

    def test_create_role_service(self):
        rs = create_role_service()
        self.assertIsNotNone(rs.role)
        self.assertIsNotNone(rs.service)

    def test_role_service_str(self):
        role = create_role(name="Editor")
        service = create_service(acronym="FI")
        rs = RoleService.objects.create(role=role, service=service)
        self.assertEqual(str(rs), "Editor | FI")


class UserRoleServiceModelTest(TestCase):

    def test_create_user_role_service(self):
        user = create_user()
        rs = create_role_service()
        urs = UserRoleService.objects.create(user=user, role_service=rs)
        self.assertEqual(urs.user, user)
        self.assertEqual(urs.role_service, rs)

    def test_cascade_delete_on_role_service(self):
        user = create_user()
        role = create_role()
        service = create_service()
        rs = RoleService.objects.create(role=role, service=service)
        UserRoleService.objects.create(user=user, role_service=rs)
        self.assertEqual(UserRoleService.objects.count(), 1)
        # RoleService has PROTECT on role/service, so delete via queryset workaround
        # Actually RoleService -> UserRoleService is CASCADE
        rs.delete()
        self.assertEqual(UserRoleService.objects.count(), 0)


class CooperativeCenterModelTest(TestCase):

    def test_create_cooperative_center(self):
        cc = create_cooperative_center(code="BR1.1", institution="BIREME")
        self.assertEqual(cc.code, "BR1.1")
        self.assertEqual(cc.institution, "BIREME")

    def test_cooperative_center_str(self):
        cc = create_cooperative_center(code="BR1.1")
        self.assertEqual(str(cc), "BR1.1")

    def test_code_unique_constraint(self):
        create_cooperative_center(code="BR1.1")
        with self.assertRaises(IntegrityError):
            country = create_country(code="AR", name="Argentina")
            CooperativeCenter.objects.create(code="BR1.1", country=country)


class TopicModelTest(TestCase):

    def test_create_topic(self):
        topic = create_topic(name="Health Information")
        self.assertEqual(topic.name, "Health Information")

    def test_topic_str(self):
        topic = create_topic(name="Health")
        self.assertEqual(str(topic), "Health")

    def test_topic_local_cascade_delete(self):
        topic = create_topic()
        TopicLocal.objects.create(topic=topic, language="pt-br")
        self.assertEqual(TopicLocal.objects.count(), 1)
        topic.delete()
        self.assertEqual(TopicLocal.objects.count(), 0)


class NetworkModelTest(TestCase):

    def test_create_network(self):
        network = create_network(acronym="TestNet", network_type="national")
        self.assertEqual(network.acronym, "TestNet")
        self.assertEqual(network.type, "national")
        self.assertIsNotNone(network.responsible)
        self.assertIsNotNone(network.country)

    def test_network_str(self):
        network = create_network(acronym="BVS")
        self.assertEqual(str(network), "BVS")

    def test_network_list_members(self):
        country = create_country()
        cc1 = create_cooperative_center(code="BR1.1", country=country)
        cc2 = create_cooperative_center(code="BR2.1", country=country)
        network = create_network(responsible=cc1, country=country)
        NetworkMembership.objects.create(network=network, cooperative_center=cc1)
        NetworkMembership.objects.create(network=network, cooperative_center=cc2)
        members = network.list_members()
        self.assertIn("BR1.1", members)
        self.assertIn("BR2.1", members)
        self.assertEqual(len(members), 2)

    def test_network_list_members_empty(self):
        network = create_network()
        self.assertEqual(network.list_members(), [])

    def test_network_type_choices(self):
        valid_types = ["national", "thematic", "institutional"]
        for t in valid_types:
            network = create_network(
                acronym=f"Net-{t}",
                responsible=create_cooperative_center(code=f"CC-{t}"),
                network_type=t,
            )
            self.assertEqual(network.type, t)


class NetworkMembershipModelTest(TestCase):

    def test_create_membership(self):
        country = create_country()
        cc = create_cooperative_center(code="BR1.1", country=country)
        network = create_network(responsible=cc, country=country)
        membership = NetworkMembership.objects.create(network=network, cooperative_center=cc)
        self.assertEqual(membership.network, network)
        self.assertEqual(membership.cooperative_center, cc)

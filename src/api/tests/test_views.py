import json
from django.test import TestCase
from django.contrib.auth.models import User
from main.models import (
    RoleService, UserRoleService, NetworkMembership, Network, CooperativeCenter,
)
from accounts.test_helpers import (
    create_country, create_cooperative_center, create_user,
    create_role, create_service, create_role_service,
    create_network,
)


class ChangeUserRoleServiceViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.target_user = create_user(username="target", email="target@example.com")
        self.role = create_role()
        self.service = create_service()
        self.rs = create_role_service(role=self.role, service=self.service)

    def test_unauthenticated_redirects(self):
        response = self.client.get("/api/users/edit/change-user-role-service/")
        self.assertEqual(response.status_code, 302)

    def test_add_role_service_checked_true(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/users/edit/change-user-role-service/", {
            "user": self.target_user.pk,
            "role": self.role.pk,
            "service": self.service.pk,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "1")
        self.assertTrue(
            UserRoleService.objects.filter(user=self.target_user, role_service=self.rs).exists()
        )

    def test_remove_role_service_checked_false(self):
        UserRoleService.objects.create(user=self.target_user, role_service=self.rs)
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/users/edit/change-user-role-service/", {
            "user": self.target_user.pk,
            "role": self.role.pk,
            "service": self.service.pk,
            "checked": "false",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "1")
        self.assertFalse(
            UserRoleService.objects.filter(user=self.target_user, role_service=self.rs).exists()
        )

    def test_add_duplicate_does_not_duplicate(self):
        UserRoleService.objects.create(user=self.target_user, role_service=self.rs)
        self.client.login(username="testuser", password="TestPass123!")
        self.client.get("/api/users/edit/change-user-role-service/", {
            "user": self.target_user.pk,
            "role": self.role.pk,
            "service": self.service.pk,
            "checked": "true",
        })
        self.assertEqual(
            UserRoleService.objects.filter(user=self.target_user, role_service=self.rs).count(), 1
        )

    def test_invalid_user_returns_404(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/users/edit/change-user-role-service/", {
            "user": 99999,
            "role": self.role.pk,
            "service": self.service.pk,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 404)

    def test_invalid_role_service_returns_404(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/users/edit/change-user-role-service/", {
            "user": self.target_user.pk,
            "role": 99999,
            "service": self.service.pk,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 404)


class ChangeNetworkMemberViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.country = create_country()
        self.cc = create_cooperative_center(code="BR1.1", country=self.country)
        self.cc2 = create_cooperative_center(code="BR2.1", country=self.country)
        self.network = create_network(responsible=self.cc, country=self.country)

    def test_unauthenticated_redirects(self):
        response = self.client.get("/api/networks/edit/change-network-member/")
        self.assertEqual(response.status_code, 302)

    def test_add_member_checked_true(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/networks/edit/change-network-member/", {
            "network": self.network.pk,
            "cc": self.cc2.pk,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "1")
        self.assertTrue(
            NetworkMembership.objects.filter(network=self.network, cooperative_center=self.cc2).exists()
        )

    def test_remove_member_checked_false(self):
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc2)
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/networks/edit/change-network-member/", {
            "network": self.network.pk,
            "cc": self.cc2.pk,
            "checked": "false",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "1")
        self.assertFalse(
            NetworkMembership.objects.filter(network=self.network, cooperative_center=self.cc2).exists()
        )

    def test_invalid_network_returns_404(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/networks/edit/change-network-member/", {
            "network": 99999,
            "cc": self.cc2.pk,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 404)

    def test_invalid_cc_returns_404(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/networks/edit/change-network-member/", {
            "network": self.network.pk,
            "cc": 99999,
            "checked": "true",
        })
        self.assertEqual(response.status_code, 404)


class GetCcsViewTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.country = create_country()
        self.cc1 = create_cooperative_center(code="BR1.1", country=self.country, institution="BIREME")
        self.cc2 = create_cooperative_center(code="AR1.1", country=create_country(code="AR", name="Argentina"), institution="OPS Argentina")

    def test_login_required(self):
        response = self.client.get("/api/get_ccs/")
        self.assertEqual(response.status_code, 302)

    def test_get_all_ccs(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/get_ccs/")
        self.assertEqual(response.status_code, 200)
        cc_codes = [cc.code for cc in response.context["ccs"]]
        self.assertIn("BR1.1", cc_codes)
        self.assertIn("AR1.1", cc_codes)

    def test_filter_by_code(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/get_ccs/", {"code": "BR"})
        self.assertEqual(response.status_code, 200)
        cc_codes = [cc.code for cc in response.context["ccs"]]
        self.assertIn("BR1.1", cc_codes)
        self.assertNotIn("AR1.1", cc_codes)

    def test_filter_by_country(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/api/get_ccs/", {"country": self.country.pk})
        self.assertEqual(response.status_code, 200)
        for cc in response.context["ccs"]:
            self.assertEqual(cc.country, self.country)

    def test_filter_with_network_context(self):
        self.client.login(username="testuser", password="TestPass123!")
        network = create_network(responsible=self.cc1, country=self.country)
        NetworkMembership.objects.create(network=network, cooperative_center=self.cc1)
        response = self.client.get("/api/get_ccs/", {"network": network.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.cc1.pk, response.context["members"])


class GetNetworkCcsViewTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc1 = create_cooperative_center(code="BR1.1", country=self.country)
        self.cc2 = create_cooperative_center(code="BR2.1", country=self.country)
        self.network = create_network(acronym="TestNet", responsible=self.cc1, country=self.country)
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc1)
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc2)

    def test_get_network_ccs_returns_json(self):
        response = self.client.get("/api/get_network_ccs/", {"network": "TestNet"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertIn("BR1.1", data["network_ccs"])
        self.assertIn("BR2.1", data["network_ccs"])

    def test_get_network_ccs_no_param(self):
        response = self.client.get("/api/get_network_ccs/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["network_ccs"], [])

    def test_get_network_ccs_nonexistent_returns_404(self):
        response = self.client.get("/api/get_network_ccs/", {"network": "NonExistent"})
        self.assertEqual(response.status_code, 404)

    def test_no_auth_required(self):
        response = self.client.get("/api/get_network_ccs/", {"network": "TestNet"})
        self.assertEqual(response.status_code, 200)

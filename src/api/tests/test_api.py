import json
from django.test import TestCase
from main.models import (
    RoleService, UserRoleService, NetworkMembership,
)
from accounts.test_helpers import (
    create_country, create_cooperative_center, create_user,
    create_role, create_service, create_role_service,
    create_network, create_advanced_user,
)


class UserResourceLoginTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(code="BR1.1", country=self.country)
        self.user = create_user(username="apiuser", email="apiuser@example.com")
        self.user.profile.cooperative_center = self.cc
        self.user.profile.save()

        self.role = create_role()
        self.service = create_service()
        self.rs = create_role_service(role=self.role, service=self.service)
        UserRoleService.objects.create(user=self.user, role_service=self.rs)

        self.network = create_network(responsible=self.cc, country=self.country)
        NetworkMembership.objects.create(network=self.network, cooperative_center=self.cc)

    def _login_post(self, data):
        return self.client.post(
            "/api/auth/login/",
            json.dumps(data),
            content_type="application/json",
        )

    def test_login_success(self):
        response = self._login_post({
            "username": "apiuser@example.com",
            "password": "TestPass123!",
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])

    def test_login_wrong_password(self):
        response = self._login_post({
            "username": "apiuser@example.com",
            "password": "wrong",
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertFalse(data["success"])

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self._login_post({
            "username": "apiuser@example.com",
            "password": "TestPass123!",
        })
        # EmailModelBackend doesn't check is_active, so Tastypie returns 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_login_user_without_cc(self):
        user_no_cc = create_user(username="nocc", email="nocc@example.com")
        response = self._login_post({
            "username": "nocc@example.com",
            "password": "TestPass123!",
        })
        self.assertEqual(response.status_code, 401)

    def test_login_with_service_filter(self):
        response = self._login_post({
            "username": "apiuser@example.com",
            "password": "TestPass123!",
            "service": self.service.acronym,
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertIn(self.role.acronym, data["data"]["role"])

    def test_login_with_service_no_role_returns_unauthorized(self):
        service2 = create_service(acronym="OTHER", name="Other Service")
        response = self._login_post({
            "username": "apiuser@example.com",
            "password": "TestPass123!",
            "service": "OTHER",
        })
        self.assertEqual(response.status_code, 401)

    def test_login_method_not_allowed_get(self):
        response = self.client.get("/api/auth/login/")
        self.assertEqual(response.status_code, 405)


class UserResourceLogoutTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(code="BR1.1", country=self.country)
        self.user = create_user(username="logoutuser", email="logout@example.com")
        self.user.profile.cooperative_center = self.cc
        self.user.profile.save()

    def test_logout_success(self):
        # Login first
        self.client.login(username="logoutuser", password="TestPass123!")
        response = self.client.get("/api/auth/logout/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["success"])

    def test_logout_unauthenticated(self):
        response = self.client.get("/api/auth/logout/")
        self.assertEqual(response.status_code, 401)

    def test_logout_method_not_allowed_post(self):
        self.client.login(username="logoutuser", password="TestPass123!")
        response = self.client.post("/api/auth/logout/")
        self.assertEqual(response.status_code, 405)

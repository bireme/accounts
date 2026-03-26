from django.test import TestCase
from accounts.test_helpers import (
    create_basic_user, create_advanced_user, create_superuser,
    create_cooperative_center,
)


class AdvancedPermissionDecoratorTest(TestCase):

    def setUp(self):
        cc = create_cooperative_center()
        self.basic_user = create_basic_user(cc=cc)
        self.advanced_user = create_advanced_user(cc=cc)
        self.superuser = create_superuser()

    def test_basic_user_gets_404(self):
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 404)

    def test_advanced_user_allowed(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_superuser_allowed(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_redirects_to_login(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class SuperuserPermissionDecoratorTest(TestCase):

    def setUp(self):
        cc = create_cooperative_center()
        self.basic_user = create_basic_user(cc=cc)
        self.advanced_user = create_advanced_user(cc=cc)
        self.superuser = create_superuser()

    def test_basic_user_gets_404(self):
        self.client.login(username="basicuser", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 404)

    def test_advanced_user_gets_404(self):
        self.client.login(username="advuser", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 404)

    def test_superuser_allowed(self):
        self.client.login(username="admin", password="TestPass123!")
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_redirects_to_login(self):
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

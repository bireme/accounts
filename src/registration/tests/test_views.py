from django.test import TestCase
from django.contrib.auth.models import User
from accounts.test_helpers import create_user


class ChangeProfileViewTest(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_get_unauthenticated_redirects(self):
        response = self.client.get("/accounts/change-profile/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_get_authenticated_renders_form(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/accounts/change-profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/change-profile.html")
        self.assertIn("form", response.context)

    def test_post_valid_email_update(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.post("/accounts/change-profile/", {"email": "newemail@example.com"})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_post_blank_email_accepted(self):
        # Django User.email has blank=True, so empty email is accepted
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.post("/accounts/change-profile/", {"email": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].errors)


class LogoutViewTest(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_logout_renders_template(self):
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/logout.html")

    def test_logout_actually_logs_out(self):
        self.client.login(username="testuser", password="TestPass123!")
        self.client.get("/accounts/logout/")
        # After logout, accessing a login_required page should redirect
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

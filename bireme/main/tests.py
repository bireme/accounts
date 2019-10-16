from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UsersGetTest(TestCase):
    def setUp(self):
        credentials = {"username": "admin", "password": "admin"}
        User.objects.create_superuser(email="admin@admin.com", **credentials)
        self.client.login(**credentials)

        User.objects.create_user(username="john.doe", email="john.doe@bireme.org")
        User.objects.create_user(username="jane.doe", email="jane.doe@bireme.org")

    def test_list(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<td>admin</td>")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertContains(response, "<td>jane.doe</td>")

    def test_filter_by_username_no_results(self):
        response = self.client.get("/users?s=unknown-username")
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<tbody></tbody>", response.content)

    def test_filter_by_username(self):
        response = self.client.get("/users?s=doe")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

        response = self.client.get("/users?s=john")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertNotContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

        response = self.client.get("/users?s=jane")
        self.assertNotContains(response, "<td>john.doe</td>")
        self.assertContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

    def test_filter_by_email(self):
        response = self.client.get("/users?s=@bireme.org")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

        response = self.client.get("/users?s=john.doe@bireme.org")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertNotContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

        response = self.client.get("/users?s=unknown@email.com")
        self.assertInHTML("<tbody></tbody>", response.content)

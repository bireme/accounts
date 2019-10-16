# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from main.models import CooperativeCenter, Country

User = get_user_model()


class UsersGetTest(TestCase):
    def setUp(self):
        credentials = {"username": "admin", "password": "admin"}
        User.objects.create_superuser(email="admin@admin.com", **credentials)
        self.client.login(**credentials)

        country = Country(code="CY", name="Country")
        country.save()

        cc = CooperativeCenter(code="AB12.3", country=country)
        cc.save()

        cc2 = CooperativeCenter(code="CD45.6", country=country)
        cc2.save()

        john = User.objects.create_user(username="john.doe", email="john.doe@bireme.org")
        john.profile.cooperative_center = cc
        john.profile.save()

        jane = User.objects.create_user(username="jane.doe", email="jane.doe@bireme.org")
        jane.profile.cooperative_center = cc2
        jane.profile.save()

        settings.ITEMS_PER_PAGE = 3

    def test_get(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get("/users")
        self.assertTemplateUsed(response, "main/users.html")

    def test_list_all(self):
        response = self.client.get("/users")
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

    def test_filter_by_cc(self):
        response = self.client.get("/users?cc=1")
        self.assertNotContains(response, "<td>admin</td>")
        self.assertContains(response, "<td>john.doe</td>")
        self.assertNotContains(response, "<td>jane.doe</td>")

        response = self.client.get("/users?cc=2")
        self.assertNotContains(response, "<td>admin</td>")
        self.assertNotContains(response, "<td>john.doe</td>")
        self.assertContains(response, "<td>jane.doe</td>")

        response = self.client.get("/users?cc=3")
        self.assertInHTML("<tbody></tbody>", response.content)
        self.assertNotContains(response, "<td>john.doe</td>")
        self.assertNotContains(response, "<td>jane.doe</td>")
        self.assertNotContains(response, "<td>admin</td>")

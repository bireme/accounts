from django.test import TestCase, RequestFactory
from main.forms import UserForm, NetworkForm, ServiceForm, RoleForm
from accounts.test_helpers import (
    create_country, create_cooperative_center, create_superuser,
    create_advanced_user, create_topic, create_network, create_user,
)


class UserFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.cc = create_cooperative_center()
        self.superuser = create_superuser()

    def _make_request(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_valid_form_superuser(self):
        request = self._make_request(self.superuser)
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "type": "basic",
            "is_active": True,
            "cc": self.cc.pk,
        }
        form = UserForm(data, request=request)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        request = self._make_request(self.superuser)
        data = {"email": "test@example.com", "type": "basic", "is_active": True, "cc": self.cc.pk}
        form = UserForm(data, request=request)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_allows_blank_email(self):
        request = self._make_request(self.superuser)
        data = {"username": "test", "email": "", "type": "basic", "is_active": True, "cc": self.cc.pk}
        form = UserForm(data, request=request)
        # Django User.email has blank=True, so empty email is valid at form level
        self.assertTrue(form.is_valid())

    def test_save_updates_profile_type(self):
        request = self._make_request(self.superuser)
        data = {
            "username": "typeuser",
            "email": "typeuser@example.com",
            "type": "advanced",
            "is_active": True,
            "cc": self.cc.pk,
        }
        form = UserForm(data, request=request)
        self.assertTrue(form.is_valid())
        user = form.save()
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.type, "advanced")

    def test_save_updates_profile_cc_for_superuser(self):
        request = self._make_request(self.superuser)
        cc2 = create_cooperative_center(code="AR1.1", country=create_country(code="AR", name="Argentina"))
        data = {
            "username": "ccuser",
            "email": "ccuser@example.com",
            "type": "basic",
            "is_active": True,
            "cc": cc2.pk,
        }
        form = UserForm(data, request=request)
        self.assertTrue(form.is_valid())
        user = form.save()
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.cooperative_center, cc2)

    def test_superuser_has_cc_field(self):
        request = self._make_request(self.superuser)
        form = UserForm(request=request)
        self.assertIn("cc", form.fields)

    def test_advanced_user_with_network_sees_cc_field(self):
        adv_user = create_advanced_user(cc=self.cc)
        network = create_network(responsible=self.cc, country=self.cc.country)
        # Add at least 2 members to trigger the cc field
        cc2 = create_cooperative_center(code="BR2.1", country=self.cc.country)
        from main.models import NetworkMembership
        NetworkMembership.objects.create(network=network, cooperative_center=self.cc)
        NetworkMembership.objects.create(network=network, cooperative_center=cc2)

        request = self._make_request(adv_user)
        form = UserForm(request=request)
        self.assertIn("cc", form.fields)

    def test_advanced_user_without_network_no_cc_field(self):
        adv_user = create_advanced_user(
            username="adv2", email="adv2@example.com",
            cc=self.cc,
        )
        request = self._make_request(adv_user)
        form = UserForm(request=request)
        self.assertNotIn("cc", form.fields)


class NetworkFormTest(TestCase):

    def setUp(self):
        self.country = create_country()
        self.cc = create_cooperative_center(country=self.country)
        self.topic = create_topic()

    def test_valid_form(self):
        data = {
            "acronym": "BVS",
            "responsible": self.cc.pk,
            "type": "national",
            "country": self.country.pk,
            "topic": self.topic.pk,
        }
        form = NetworkForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_acronym(self):
        data = {"responsible": self.cc.pk, "type": "national"}
        form = NetworkForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("acronym", form.errors)

    def test_invalid_form_missing_responsible(self):
        data = {"acronym": "BVS", "type": "national"}
        form = NetworkForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("responsible", form.errors)

    def test_responsible_queryset_ordered_by_code(self):
        cc2 = create_cooperative_center(code="AA1.1", country=self.country)
        form = NetworkForm()
        qs = form.fields["responsible"].queryset
        codes = list(qs.values_list("code", flat=True))
        self.assertEqual(codes, sorted(codes))


class ServiceFormTest(TestCase):

    def test_valid_form(self):
        form = ServiceForm({"name": "FI-Admin", "acronym": "FI"})
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        form = ServiceForm({"acronym": "FI"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_invalid_form_missing_acronym(self):
        form = ServiceForm({"name": "FI-Admin"})
        self.assertFalse(form.is_valid())
        self.assertIn("acronym", form.errors)


class RoleFormTest(TestCase):

    def test_valid_form(self):
        form = RoleForm({"name": "Editor", "acronym": "EDR", "description": "Editor role"})
        self.assertTrue(form.is_valid())

    def test_valid_form_without_description(self):
        form = RoleForm({"name": "Editor", "acronym": "EDR"})
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        form = RoleForm({"acronym": "EDR"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_invalid_form_missing_acronym(self):
        form = RoleForm({"name": "Editor"})
        self.assertFalse(form.is_valid())
        self.assertIn("acronym", form.errors)

from django.test import TestCase
from registration.forms import ChangeProfileForm
from accounts.test_helpers import create_user


class ChangeProfileFormTest(TestCase):

    def test_valid_form(self):
        form = ChangeProfileForm({"email": "new@example.com"})
        self.assertTrue(form.is_valid())

    def test_form_allows_blank_email(self):
        # Django User.email has blank=True, so empty email is valid at form level
        form = ChangeProfileForm({"email": ""})
        self.assertTrue(form.is_valid())

    def test_form_only_has_email_field(self):
        form = ChangeProfileForm()
        self.assertEqual(list(form.fields.keys()), ["email"])

    def test_save_updates_email(self):
        user = create_user()
        form = ChangeProfileForm({"email": "changed@example.com"}, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        user.refresh_from_db()
        self.assertEqual(user.email, "changed@example.com")

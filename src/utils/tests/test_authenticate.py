from django.test import TestCase
from utils.authenticate import EmailModelBackend
from accounts.test_helpers import create_user


class EmailModelBackendTest(TestCase):

    def setUp(self):
        self.backend = EmailModelBackend()
        self.user = create_user(username="emailuser", email="emailuser@example.com", password="TestPass123!")

    def test_authenticate_with_email_success(self):
        result = self.backend.authenticate(None, username="emailuser@example.com", password="TestPass123!")
        self.assertEqual(result, self.user)

    def test_authenticate_with_email_wrong_password(self):
        result = self.backend.authenticate(None, username="emailuser@example.com", password="wrong")
        self.assertIsNone(result)

    def test_authenticate_with_nonexistent_email(self):
        result = self.backend.authenticate(None, username="noone@example.com", password="TestPass123!")
        self.assertIsNone(result)

    def test_get_user_existing(self):
        result = self.backend.get_user(self.user.pk)
        self.assertEqual(result, self.user)

    def test_get_user_nonexistent(self):
        result = self.backend.get_user(99999)
        self.assertIsNone(result)

import smtplib
from unittest import mock

from django.core import mail
from django.test import TestCase, RequestFactory
from utils.email import send_password_setup_email
from accounts.test_helpers import create_user, create_superuser


SEND_PATH = "django.core.mail.EmailMultiAlternatives.send"


class SendPasswordSetupEmailTest(TestCase):

    def setUp(self):
        self.user = create_user(username="target", email="target@example.com")
        self.admin = create_superuser()
        self.request = RequestFactory().get("/")
        self.request.user = self.admin

    def test_success_sends_email_and_returns_true(self):
        result = send_password_setup_email(self.request, self.user.email)
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])

    def test_smtp_failure_is_logged_and_returns_false(self):
        with mock.patch(SEND_PATH, side_effect=smtplib.SMTPException("boom")):
            with self.assertLogs("utils.email", level="ERROR") as logs:
                result = send_password_setup_email(self.request, self.user.email)
        self.assertFalse(result)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("target@example.com", logs.output[0])
        self.assertIn("admin", logs.output[0])
        self.assertIn("SMTPException: boom", logs.output[0])

    def test_connection_error_is_logged_and_returns_false(self):
        with mock.patch(SEND_PATH, side_effect=ConnectionRefusedError()):
            with self.assertLogs("utils.email", level="ERROR"):
                result = send_password_setup_email(self.request, self.user.email)
        self.assertFalse(result)

    def test_invalid_email_is_logged_as_warning_and_returns_false(self):
        with self.assertLogs("utils.email", level="WARNING") as logs:
            result = send_password_setup_email(self.request, "not-an-email")
        self.assertFalse(result)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("invalid address", logs.output[0])

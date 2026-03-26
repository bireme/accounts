from django.test import TestCase
from django.conf import settings


class CookieLangViewTest(TestCase):

    def test_cookie_lang_sets_cookie(self):
        response = self.client.get("/cookie-lang/", {"language": "es"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "es")

    def test_cookie_lang_returns_language_text(self):
        response = self.client.get("/cookie-lang/", {"language": "pt-br"})
        self.assertEqual(response.content.decode(), "pt-br")

    def test_cookie_lang_sets_session(self):
        self.client.get("/cookie-lang/", {"language": "en"})
        session = self.client.session
        self.assertEqual(session.get(settings.LANGUAGE_COOKIE_NAME), "en")

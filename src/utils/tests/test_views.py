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

    def test_cookie_lang_normalizes_language_code(self):
        response = self.client.get("/cookie-lang/", {"language": "pt-BR"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "pt-br")

    def test_cookie_lang_rejects_invalid_language(self):
        response = self.client.get("/cookie-lang/", {"language": "xx"})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)

    def test_cookie_lang_rejects_missing_language(self):
        response = self.client.get("/cookie-lang/")
        self.assertEqual(response.status_code, 400)

from django.test import TestCase
from django.conf import settings

from accounts.test_helpers import create_superuser


class LanguageSwitchTest(TestCase):

    def setUp(self):
        create_superuser()
        self.client.login(username="admin", password="TestPass123!")

    def set_language(self, language, next_url="/"):
        return self.client.post("/i18n/setlang/", {"language": language, "next": next_url})

    def test_default_language_is_pt_br(self):
        response = self.client.get("/")
        self.assertEqual(response["Content-Language"], "pt-br")
        self.assertContains(response, "Painel de Controle")

    def test_set_language_redirects_to_next(self):
        response = self.set_language("es", next_url="/users/")
        self.assertRedirects(response, "/users/", fetch_redirect_response=False)
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "es")

    def test_set_language_switches_interface(self):
        self.set_language("es")
        response = self.client.get("/")
        self.assertEqual(response["Content-Language"], "es")
        self.assertContains(response, "Panel de control")

        self.set_language("en")
        response = self.client.get("/")
        self.assertEqual(response["Content-Language"], "en")
        self.assertContains(response, "Dashboard")

    def test_cookie_overrides_accept_language(self):
        self.set_language("es")
        response = self.client.get("/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertEqual(response["Content-Language"], "es")

    def test_cookie_lang_activates_language(self):
        self.client.get("/cookie-lang/", {"language": "es"})
        response = self.client.get("/")
        self.assertEqual(response["Content-Language"], "es")

    def test_menu_hides_active_language(self):
        self.set_language("es")
        response = self.client.get("/")
        self.assertNotContains(response, "change_language('es')")
        self.assertContains(response, "change_language('en')")
        self.assertContains(response, "change_language('pt-br')")

    def test_lang_form_next_is_current_path(self):
        response = self.client.get("/users/")
        self.assertContains(response, 'name="next" type="hidden" value="/users/"')

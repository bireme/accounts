import time
from django.test import TestCase
from django.contrib.auth.models import User
from utils.models import Country, CountryLocal
from accounts.test_helpers import create_country, create_country_local, create_user


class CountryModelTest(TestCase):

    def test_create_country(self):
        country = create_country(code="AR", name="Argentina")
        self.assertEqual(country.code, "AR")
        self.assertEqual(country.name, "Argentina")
        self.assertIsNotNone(country.created)
        self.assertIsNotNone(country.updated)

    def test_country_str(self):
        country = create_country(name="Brazil")
        self.assertEqual(str(country), "Brazil")

    def test_country_updated_on_save(self):
        country = create_country()
        original_updated = country.updated
        time.sleep(0.01)
        country.name = "Brasil"
        country.save()
        country.refresh_from_db()
        self.assertGreater(country.updated, original_updated)

    def test_country_creator_updater_nullable(self):
        country = create_country()
        self.assertIsNone(country.creator)
        self.assertIsNone(country.updater)

    def test_country_creator_can_be_set(self):
        user = create_user()
        country = Country.objects.create(code="CL", name="Chile", creator=user)
        self.assertEqual(country.creator, user)


class CountryLocalModelTest(TestCase):

    def test_create_country_local(self):
        country = create_country()
        local = create_country_local(country=country, language="pt-br", name="Brasil")
        self.assertEqual(local.country, country)
        self.assertEqual(local.language, "pt-br")
        self.assertEqual(local.name, "Brasil")

    def test_country_local_cascade_delete(self):
        country = create_country()
        create_country_local(country=country)
        self.assertEqual(CountryLocal.objects.count(), 1)
        country.delete()
        self.assertEqual(CountryLocal.objects.count(), 0)

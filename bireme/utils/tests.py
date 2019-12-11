from mock import patch
from django.test import TestCase

from utils.models import Country, CountryLocal


class TestCountryModel(TestCase):
    def setUp(self):
        self.country = Country(code='BR', name='Brazil')
        self.country.save()

    @patch('utils.models.get_language', return_value='en')
    def test_unicode_default(self, get_language):
        self.assertEqual('Brazil', unicode(self.country))

    @patch('utils.models.get_language', return_value='pt-br')
    def test_unicode_existing_translation(self, get_language):
        country_pt_br = CountryLocal(
            country=self.country,
            language='pt-br',
            name='Brasil'
        )
        country_pt_br.save()

        self.assertEqual('Brasil', unicode(self.country))

    @patch('utils.models.get_language', return_value='xpto')
    def test_unicode_translation_not_available(self, get_language):
        """Must return country name when translation is not available"""
        self.assertEqual('Brazil', unicode(self.country))

import unittest
from modules.scrapper import Scrapper


class TestScrapper(unittest.TestCase):
    """
    Testa as funções do scrapper
    """
    def setUp(self):
        self.scrapper = Scrapper()

    def test_get_url(self):
        response = self.scrapper.get_url(
            'https://www.ludopedia.com.br/anuncios', 'teste')
        self.assertEqual(response.status_code, 200)

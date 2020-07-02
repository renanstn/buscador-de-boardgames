import unittest
from modules.scrapper import Scrapper


class TestScrapper(unittest.TestCase):
    def test_scrap_leiloes(self):
        scrapper = Scrapper()
        expected_data = [
            {
                'name': 'munchkin',
                'price': '60,00',
                'link': 'https://www.ludopedia.com.br/leilao/332651/munchkin',

            },
            {
                'name': 'munchkin',
                'price': '70,00',
                'link': 'https://www.ludopedia.com.br/leilao/332652/munchkin',

            }
        ]
        data = scrapper.scrap_leiloes()
        self.assertEqual(data, expected_data)

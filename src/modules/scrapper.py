import os
from requests import get
from bs4 import BeautifulSoup


class Scrapper:
    """
    Efetua o web scrap no site do ludopedia
    """
    def __init__(self):
        """
        Define as URLs e elementos utilizados no scrapping
        """
        self.url_anuncios = os.environ.get(
            'URL_ANUNCIO', 'https://www.ludopedia.com.br/anuncios')

    def get_url(self, url, name):
        """
        Monta a URL e faz a request
        """
        payload = {'nm_jogo': name}
        response = get(url, params=payload)
        if response.status_code != 200:
            print('Houve um erro na request')
            # TODO adicionar log

        return response

    def scrap_anuncios(self, name):
        """
        Procura pelo boardgame na sessão de anúncios
        Retorna um dicionário com as informações principais do
        jogo encontrado
        """
        response = self.get_url(self.url_anuncios, name)
        bs4 = BeautifulSoup(response.text, 'html.parser')

        result_list = bs4.find('ul', class_='row')
        itens = result_list.find_all('li')
        resultados = []

        for item in itens:
            dl = item.find('dl')

            name = item.find('a', class_='link-elipsis')
            category = item.find('div', class_='box-anuncio-title')
            link = dl.find('a')
            value = dl.find('dd', class_='proximo_lance')

            resultados.append({
                'category': category.text,
                'name': name.text,
                'value': value.text,
                'link': link['href']
            })

        return resultados

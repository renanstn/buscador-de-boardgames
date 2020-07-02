import os
from requests import get
from bs4 import BeautifulSoup


class Scrapper:
    """
    Efetura o web scrap no site do ludopedia
    """
    def __init__(self):
        """
        Define as URLs e elementos utilizados no scrapping
        """
        # URLs
        self.url_anuncios = os.environ.get('URL_ANUNCIOS', 'https://www.ludopedia.com.br/anuncios')
        # Elemento que armazena o painel principal
        self.element_results = 'row'
        # Elemento que armazena cada item no resultado da busca
        self.element_item = 'item-leilao'
        # Elemento que armazena o nome do jogo
        self.element_name = 'link-elipsis'
        # Elemento que armazena o valor do jogo
        self.element_value = 'prod-preco'
        # Elemento que armazena a categoria
        self.element_category = 'box-anuncio-title'

    def __get(self, url, name):
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
        Procura pelo boardgame na sessão de leilões
        """
        response = self.__get(self.url_anuncios, name)
        bs4 = BeautifulSoup(response.text, 'html.parser')

        result_list = bs4.find('ul', class_=self.element_results)
        itens = result_list.find_all('li')
        results = []

        for item in itens:
            category = item.find('div', class_=self.element_category)
            print(category.text)
            # name = item.find('a', class_=self.element_name)
            # value = item.find('span', class_=self.element_value)
            # link = item.find('a')

            results.append({
                # 'category': category.text,
                # 'name': name.text,
                # 'value': value.text,
                # 'link': link['href']
            })

        return results

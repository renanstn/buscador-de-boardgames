import os
import requests


class Service:
    """
    Serviço que consome a API do ComparaJogos para comparar o preço
    de um produto com o preço médio de mercado
    """
    def __init__(self):
        self.url = os.environ.get(
            'URL_SERVICO', 'https://api.comparajogos.com.br/v1alpha1/graphql')

    def busca(self, nome):
        """
        Busca o jogo na API do site via graphql, utilizando a mesma
        query que o front utiliza para pesquisas
        """
        query = {
            "operationName": "product_list",
            "variables": {
                "where": {
                    "product": {
                        "name_unaccented": {
                            "_ilike": f"%{nome}%"
                        },
                        "type": {
                            "_in": ["game"]
                        }
                    }
                },
                "limit": 15,
                "offset": 0,
                "order_by": [
                    {
                        "available": "desc"
                    },
                    {
                        "product": {
                            "bgg_ranking": "asc_nulls_last"
                        }
                    },
                    {
                        "product": {
                            "slug": "asc"
                        }
                    }
                ]
            },
            "query": "query product_list($limit: Int, $offset: Int, $order_by: [product_price_order_by!], $where: product_price_bool_exp) {\n  list: product_price(order_by: $order_by, limit: $limit, offset: $offset, where: $where) {\n    ...product_price_fragment\n    __typename\n  }\n  count: product_price_aggregate(where: $where) {\n    aggregate {\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment product_price_fragment on product_price {\n  id\n  product {\n    id\n    slug\n    name\n    playing_time\n    max_players\n    min_players\n    thumbnail_url\n    bgg_rating\n    bgg_ranking\n    bgg_weight\n    type\n    list_items_mine {\n      list\n      __typename\n    }\n    count {\n      own\n      wish\n      __typename\n    }\n    __typename\n  }\n  min_price\n  stores_count\n  available\n  __typename\n}\n"
        }

        result = requests.post(self.url, json=query)

        if result.status_code == 200:
            return result.json()
        else:
            print("Houve um problema com a consulta do preço no ComparaJogos")

    def busca_preco_medio(self, boardgame):
        data = self.busca(boardgame)

        if len(data['data']['list']) == 0:
            return {
                'boardgame': boardgame,
                'preco': None
            }
        else:
            return {
                'boardgame': data['data']['list'][0]['product']['name'],
                'preco': data['data']['list'][0]['min_price'],
            }

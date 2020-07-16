import os
import pymongo


class Sync:
    """
    Classe responsável por armazenar e buscar dados no mongo
    """
    def __init__(self):
        mongo_url = os.environ.get('MONGODB_URI', 'mongodb://mongo:27017/')
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client['database']
        self.cadastros = self.db['cadastros']

    def add_cadastro(self, data):
        """
        Adiciona um boardgame para ser buscado
        """
        response = self.cadastros.insert_one(data)
        return response.inserted_id

    def load_cadastros_by_id(self, chat_id):
        """
        Carrega todos os cadastros de um usuario
        """
        data = self.cadastros.find({'chat_id': chat_id})
        return data

    def load_all_cadastros(self):
        data = self.cadastros.find()
        return data

    def atualiza_average_price(self, data, price):
        self.cadastros.update({
            'chat_id': data['chat_id'],
            'boardgame': data['boardgame']
        }, {
            'average_price': price
        })

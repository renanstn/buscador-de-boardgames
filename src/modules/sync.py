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
        resposta = self.cadastros.insert_one(data)
        return resposta.inserted_id

    def verifica_cadastro_existente(self, chat_id, boardgame):
        """
        Verifica se um usuário já possui o boardgame cadastrado
        """
        resultado = self.cadastros.find({
            'chat_id': chat_id,
            'boardgame': boardgame
        })
        return len(resultado) > 0

    def busca_cadastro_por_id(self, chat_id):
        """
        Carrega todos os cadastros de um usuario
        """
        dados = self.cadastros.find({'chat_id': chat_id})
        return dados

    def carrega_todos_os_cadastros(self):
        dados = self.cadastros.find()
        return dados

    def atualiza_preco_medio(self, data, price):
        self.cadastros.update_one({
            'chat_id': data['chat_id'],
            'boardgame': data['boardgame']
        }, {'$set': {
            'preco_medio': price
        }})

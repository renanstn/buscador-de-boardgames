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

    def bulk_save(self, chat_id, data):
        """
        Atualiza os anuncios salvos de um usuario no banco
        ### DEPRECIADO, APAGAR
        """
        self.anuncios.delete_many({'chat_id': chat_id})
        result = self.anuncios.insert_many(data)
        return result.inserted_ids

    def load(self, chat_id):
        """
        Carrega todos os anúncios de um usuario
        ### DEPRECIADO, APAGAR
        """
        data = self.anuncios.find({'chat_id': chat_id})
        return data

    def get_all_anuncios(self):
        """
        Retorna todos os anúncios do banco
        ### DEPRECIADO, APAGAR
        """
        print("{} anuncios carregados".format(self.anuncios.count_documents({})))
        data = self.anuncios.find()
        anuncios = []
        for i in data:
            anuncios.append(i)
        return anuncios

    def clear_anuncios(self):
        """
        Apaga todos os anúncios do banco
        ### DEPRECIADO, APAGAR
        """
        self.anuncios.delete_many({})

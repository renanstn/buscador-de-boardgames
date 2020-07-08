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
        self.anuncios = self.db['anuncios']

    def bulk_save(self, user_id, data):
        """
        Atualiza os anuncios salvos de um usuario no banco
        """
        self.anuncios.delete_many({'user_id': user_id})
        result = self.anuncios.insert_many(data)
        return result.inserted_ids

    def load(self, user_id):
        """
        Carrega todos os anúncios de um usuario
        """
        data = self.anuncios.find({'user_id': user_id})
        return data

    def get_all_anuncios(self):
        """
        Retorna todos os anúncios do banco
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
        """
        self.anuncios.delete_many({})

import os
import pymongo


class Sync:
    """
    Classe responsável por armazenar e buscar dados no banco
    """
    def __init__(self):
        mongo_url = os.environ.get('MONGODB_URI', 'mongodb://mongo:27017/')
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client['database']
        self.anuncios = self.db['anuncios']

    def bulk_save(self, user_id, data):
        """
        Salva um anúncio no banco
        """
        result = self.anuncios.update_many(
            {'user': user_id},
            data,
            True
        )
        return result.inserted_ids

    def load(self, id):
        data = self.anuncios.find_one({'_id': id})
        return data

    def get_all_anuncios(self):
        anuncios = []
        print("{} anuncios carregados".format(self.anuncios.count_documents({})))
        data = self.anuncios.find()
        for i in data:
            anuncios.append(i)
        return anuncios

    def clear_anuncios(self):
        self.anuncios.delete_many({})

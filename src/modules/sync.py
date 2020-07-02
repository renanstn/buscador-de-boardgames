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

    def save(self, data):
        """
        Salva um anúncio no banco
        """
        assert 'nome' in data
        assert 'preco' in data
        assert 'link' in data
        inserted_id = self.anuncios.insert_one(data).inserted_id
        print(f"Anuncio inserido, {inserted_id}")

    def load(self, id):
        data = self.anuncios.find_one({'_id': id})
        return data

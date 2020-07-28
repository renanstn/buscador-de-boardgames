import os
from peewee import Model, CharField, PostgresqlDatabase
from playhouse.db_url import connect


class Cadastros(Model):
    chat_id = CharField()
    boardgame = CharField()
    preco_medio = CharField(null=True)

    class Meta:
        database = None


class Sync:
    """
    Classe responsável por armazenar e buscar dados no mongo
    """
    def __init__(self):
        DATABASE_URL = os.environ.get(
            'DATABASE_URL',
            'postgresql://postgres:admin@postgres:5432/postgres'
        )
        self.db = connect(DATABASE_URL)
        tabela_cadastros = Cadastros()
        tabela_cadastros._meta.database = self.db
        tabela_cadastros.create_table()

    def add_cadastro(self, data):
        """
        Adiciona um boardgame para ser buscado
        """
        Cadastros.create(
            chat_id=data.get('chat_id'),
            boardgame=data.get('boardgame'),
            preco_medio=data.get('preco_medio')
        )

    def verifica_cadastro_existente(self, chat_id, boardgame):
        """
        Verifica se um usuário já possui o boardgame cadastrado
        """
        query = Cadastros.select().where(
            (Cadastros.chat_id == chat_id) &
            (Cadastros.boardgame == boardgame)
        )
        return query.count() > 0

    def carrega_todos_os_cadastros(self):
        query = Cadastros.select()
        return [{
            'chat_id': i.chat_id,
            'boardgame': i.boardgame
            } for i in query
        ]

    def atualiza_preco_medio(self, data, preco):
        Cadastros.update({Cadastros.preco_medio: preco}).where(
            (Cadastros.chat_id == data.get('chat_id')) &
            (Cadastros.boardgame == data.get('boardgame'))
        ).execute()

    def remove_cadastro(self, chat_id, boardgame):
        """
        Remove um boardgame dos cadastros
        """
        deleted = Cadastros.delete().where(
            (Cadastros.chat_id == chat_id) &
            (Cadastros.boardgame == boardgame)
        ).execute()

        return deleted

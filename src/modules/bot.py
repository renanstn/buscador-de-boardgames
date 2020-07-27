import os
from telegram.bot import Bot as TBot
from telegram.ext import Updater, CommandHandler
from modules.sync import Sync
from modules.service import Service


class Bot:
    """
    Bot que recebe os cadastros de boardgames a buscar e que também
    envia as notificações de boardgames encontrados
    """
    def __init__(self):
        """
        Inicializa o bot com os parâmetros necessários e os handlers
        """
        token = os.environ.get('TELEGRAM_TOKEN')
        self.bot = TBot(token)
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('busca', self.cadastra_nova_busca)

        self.dispatcher.add_handler(start_handler)
        # TODO Adicionar uma mensgaem padrão para qualquer outro comando

    def cadastra_nova_busca(self, update, context):
        """
        Recebe o nome de um boardgame para ser cadastrado
        """
        chat_id = update.effective_chat.id
        boardgame = update.message.text.replace('/busca', '')

        if not boardgame:
            context.bot.send_message(
                chat_id=chat_id,
                text=(
                    "Informe o nome do boardgame após o comando.\n\n"
                    "Exemplo:\n/busca munchkin"
                )
            )
            return

        service = Service()
        boardgame = boardgame.strip()
        preco_medio = service.busca_preco_medio(boardgame).get('preco')

        data = {
            'chat_id': str(chat_id),
            'boardgame': boardgame,
            'preco_medio': preco_medio
        }

        sync = Sync()

        ja_cadastrado = sync.verifica_cadastro_existente(chat_id, boardgame)
        if ja_cadastrado:
            context.bot.send_message(
                chat_id=chat_id,
                text="Este jogo já foi cadastrado e já está sendo monitorado."
            )
            return

        sync.add_cadastro(data)

        context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"Jogo '{boardgame}' cadastrado com sucesso!\n"
                f"O preço médio deste produto segundo o 'Compara Jogos' é de R$ {preco_medio}\n"
                "Buscas periódicas serão feitas por este jogo a partir de agora.\n"
                "Te avisarei caso encontre algum anúncio cujo preço esteja abaixo da média.\n"
            )
        )

    def listen(self):
        """
        Inicia o monitoramento de mensagens do bot
        """
        print('listening...')
        self.updater.start_polling()

    def enviar_notificacao(self, chat_id, mensagem):
        """
        Envia uma mensagem para o usuário
        """
        self.bot.send_message(
            chat_id,
            mensagem
        )

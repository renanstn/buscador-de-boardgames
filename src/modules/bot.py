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
        self.token = os.environ.get('TELEGRAM_TOKEN')
        self.port = int(os.environ.get("PORT", "5000"))

        self.bot = TBot(self.token)
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        busca_handler = CommandHandler('busca', self.cadastra_nova_busca)
        cancela_handler = CommandHandler('cancela', self.cancela_busca)

        self.dispatcher.add_handler(busca_handler)
        self.dispatcher.add_handler(cancela_handler)
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
        sync = Sync()
        boardgame = boardgame.strip().lower()

        ja_cadastrado = sync.verifica_cadastro_existente(str(chat_id), boardgame)
        if ja_cadastrado:
            context.bot.send_message(
                chat_id=chat_id,
                text="Este jogo já foi cadastrado e já está sendo monitorado."
            )
            return

        preco_medio = service.busca_preco_medio(boardgame).get('preco')
        data = {
            'chat_id': str(chat_id),
            'boardgame': boardgame,
            'preco_medio': preco_medio
        }
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

    def cancela_busca(self, update, context):
        """
        Cancela o rastreamento de um boardgame
        """
        chat_id = update.effective_chat.id
        boardgame = update.message.text.replace('/cancela', '')
        boardgame = boardgame.strip().lower()

        sync = Sync()
        removido = sync.remove_cadastro(str(chat_id), boardgame)

        if removido:
            context.bot.send_message(
                chat_id=chat_id,
                text=f"O jogo '{boardgame}' foi removido da lista de buscas periódicas."
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="Não foi encontrado nenhum jogo com este nome cadastrado."
            )

    def listen(self):
        """
        Inicia o monitoramento de mensagens do bot
        """
        # self.updater.start_polling()
        self.updater.start_webhook(
            listen='0.0.0.0',
            port=self.port,
            url_path=self.token
        )
        self.updater.bot.set_webhook('https://boardgame-scrapper-bot.herokuapp.com/' + self.token)
        print('listening...')

    def enviar_notificacao(self, chat_id, mensagem):
        """
        Envia uma mensagem para o usuário
        """
        self.bot.send_message(
            chat_id,
            mensagem
        )

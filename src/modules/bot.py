import os
from telegram.ext import Updater, CommandHandler
from modules.sync import Sync


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
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('busca', self.busca)

        self.dispatcher.add_handler(start_handler)
        # TODO Adicionar uma mensgaem padrão para qualquer outro comando

    def busca(self, update, context):
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

        data = {
            'chat_id': str(chat_id),
            'boardgame': boardgame.strip(),
            'average_price': None
        }

        sync = Sync()
        sync.add_cadastro(data)

    def listen(self):
        """
        Inicia o monitoramento de mensagens do bot
        """
        print('listening...')
        self.updater.start_polling()

    def send_notification(self, chat_id, message):
        """
        Envia uma mensagem para o usuário
        """
        self.bot.send_message(
            self.chat_id,
            message
        )

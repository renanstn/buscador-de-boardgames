from modules.bot import Bot
from modules.scrapper import Scrapper
from modules.sync import Sync


def main():
    # telegram_bot = Bot()
    # telegram_bot.listen()

    # Fazer o scrappin
    scrapper = Scrapper()
    anuncios = scrapper.scrap_anuncios('luxor')

    # Adicionar user_id ao dicionário
    user_id = '0123456789'
    data = {
        'user': user_id,
        'anuncios': anuncios
    }

    # Salvar os resultados
    sync = Sync()
    sync.bulk_save(user_id, data)

    anuncios = sync.get_all_anuncios()
    print(anuncios)


if __name__ == "__main__":
    main()

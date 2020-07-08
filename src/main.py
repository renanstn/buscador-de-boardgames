from modules.bot import Bot
from modules.scrapper import Scrapper
from modules.sync import Sync


def main():
    # telegram_bot = Bot()
    # telegram_bot.listen()
    user_id = '01234567891'

    # Fazer o scrappin
    scrapper = Scrapper()
    anuncios = scrapper.scrap_anuncios('luxor')

    # Adicionar user_id ao dicionário
    for anuncio in anuncios:
        anuncio['user_id'] = user_id

    # Salvar os resultados
    sync = Sync()
    sync.bulk_save(user_id, anuncios)
    print("anuncios salvos")
    print('procurando anuncios')
    salvos = sync.load(user_id)
    for i in salvos:
        print(i)
    print('fim')
    # sync.clear_anuncios()


if __name__ == "__main__":
    main()

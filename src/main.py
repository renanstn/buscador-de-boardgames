from modules.bot import Bot
from modules.scrapper import Scrapper
from modules.sync import Sync
from modules.service import Service


def main():
    # telegram_bot = Bot()
    # telegram_bot.listen()
    user_id = '0123456789'
    boardgame = 'luxor'
    # sync = Sync()

    # Fazer o scrappin
    # scrapper = Scrapper()
    # anuncios = scrapper.scrap_anuncios(boardgame)

    # Adicionar user_id ao dicionário
    # for anuncio in anuncios:
        # anuncio['user_id'] = user_id

    # Salvar os resultados
    # sync.bulk_save(user_id, anuncios)
    # print("anuncios salvos")
    # print('procurando anuncios')
    # salvos = sync.load(user_id)
    # for i in salvos:
        # print(i)
    # print('fim')
    # sync.clear_anuncios()
    service = Service()
    result = service.busca(boardgame)
    print(result)


if __name__ == "__main__":
    main()

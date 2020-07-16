from modules.scrapper import Scrapper
from modules.sync import Sync
from modules.service import Service


def main():
    chat_id = '747786172'
    sync = Sync()
    service = Service()

    teste = service.busca('xaxaxaxaxaxa')
    print(teste)

    #salvos = sync.load_cadastros_by_id(chat_id)
    #for i in salvos:
        #data = service.busca(i['boardgame'])
        #print(data)

    # Fazer o scrappin
    # scrapper = Scrapper()
    # anuncios = scrapper.scrap_anuncios(boardgame)

    # Adicionar chat_id ao dicionário
    # for anuncio in anuncios:
        # anuncio['chat_id'] = chat_id

    # Salvar os resultados
    # sync.bulk_save(chat_id, anuncios)
    # print("anuncios salvos")
    # print('procurando anuncios')
    # sync.clear_anuncios()


if __name__ == "__main__":
    main()

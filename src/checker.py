from modules.sync import Sync
from modules.scrapper import Scrapper
from modules.service import Service


def main():
    sync = Sync()
    service = Service()
    scrapper = Scrapper()
    cadastros = sync.load_all_cadastros()

    for cadastro in cadastros:
        service_result = service.busca_preco_medio(cadastro['boardgame'])
        sync.atualiza_average_price(cadastro, service_result['price'])
        scrapper_result = scrapper.scrap_anuncios(cadastro['boardgame'])


if __name__ == "__main__":
    main()

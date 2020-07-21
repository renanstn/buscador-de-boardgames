from modules.sync import Sync
from modules.scrapper import Scrapper
from modules.service import Service
from modules.bot import Bot


def main():
    sync = Sync()
    service = Service()
    scrapper = Scrapper()
    cadastros = sync.load_all_cadastros()

    for cadastro in cadastros:
        service_result = service.busca_preco_medio(cadastro['boardgame'])
        sync.atualiza_average_price(cadastro, service_result['price'])
        if not service_result['price']:
            continue
        scrapper_result = scrapper.scrap_anuncios(cadastro['boardgame'])

        emitir_notificacao = compara_precos(service_result['price'], scrapper_result)

        if emitir_notificacao:
            bot = Bot()
            msg = 'teste'
            bot.send_notification(cadastro['chat_id'], msg)


def compara_precos(average, scrapper_results):
    for item in scrapper_results:
        valor = item['value'].replace('R$', '').replace(',', '.').strip()
        if float(valor) < float(average):
            return True

    return False


if __name__ == "__main__":
    main()

from modules.sync import Sync
from modules.scrapper import Scrapper
from modules.service import Service
from modules.bot import Bot


def main():
    sync = Sync()
    service = Service()
    scrapper = Scrapper()
    cadastros = sync.carrega_todos_os_cadastros()

    for cadastro in cadastros:
        # Busca e atualiza o preço médio do boardgame
        service_result = service.busca_preco_medio(cadastro['boardgame'])
        sync.atualiza_preco_medio(cadastro, service_result['price'])
        if not service_result['price']:
            continue

        # Faz o scrap no ludopedia para buscar anúncios deste produto
        resultado_scrapper = scrapper.scrap_anuncios(cadastro['boardgame'])

        # Compara os preços para ver se precisa ou não notificar o usuário
        emitir_notificacao = compara_precos(service_result['price'], resultado_scrapper)

        if emitir_notificacao:
            bot = Bot()
            msg = 'teste'
            bot.enviar_notificacao(cadastro['chat_id'], msg)


def compara_precos(media, resultado_scrapper):
    """
    Compara os resultados do scrapper com o preço médio do boardgame
    Retorna True caso algum esteja abaixo da média, e False caso não esteja
    """
    for item in scrapper_results:
        valor = item['value'].replace('R$', '').replace(',', '.').strip()
        if float(valor) < float(media):
            return True
    return False


if __name__ == "__main__":
    main()

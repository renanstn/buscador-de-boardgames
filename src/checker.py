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
        sync.atualiza_preco_medio(cadastro, service_result['preco'])
        if not service_result['preco']:
            continue

        # Faz o scrap no ludopedia para buscar anúncios deste produto
        resultado_scrapper = scrapper.scrap_anuncios(cadastro['boardgame'])

        # Compara os preços para ver se precisa ou não notificar o usuário
        itens_para_notificar = filtra_itens_abaixo_do_preco(
            service_result['preco'], resultado_scrapper)

        if len(itens_para_notificar) == 0:
            continue

        bot = Bot()
        for item in itens_para_notificar:
            mensagem = (
                "** ITEM ABAIXO DO PREÇO **\n\n"
                f"O item '{cadastro['boardgame'].upper()}' possui preço médio de R$ {service_result['preco']}\n"
                f"Encontramos o(s) seguinte(s) anúncio(s) abaixo do preço médio:\n"
                "- Categoria: {}\n- Preço: {}\n- Link: {}".format(
                    item.get('category'),
                    item.get('value'),
                    item.get('link')
                )
            )
            bot.enviar_notificacao(cadastro['chat_id'], mensagem)


def filtra_itens_abaixo_do_preco(media, resultado_scrapper):
    """
    Compara os resultados do scrapper com o preço médio do boardgame
    Retorna uma lista somente com os itens abaixo do preço
    """
    abaixo_do_preco = []
    for item in resultado_scrapper:
        valor = item['value'].replace('R$', '').replace(',', '.').strip()
        if float(valor) < float(media):
            abaixo_do_preco.append(item)
    return abaixo_do_preco


if __name__ == "__main__":
    main()

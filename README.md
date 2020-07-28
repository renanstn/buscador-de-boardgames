# Buscador de Boardgames

[@Ludopedia Scrapper Bot](https://t.me/board_scrapper_bot)

Projeto que compara preços de boardgames anunciados do [Ludopedia](https://www.ludopedia.com.br/) com o preço médio encontrado no [Compara Jogos](https://www.comparajogos.com.br/), e notifica caso o valor esteja abaixo da média.

<img src="https://github.com/renanstd/buscador-de-boardgames/blob/master/screenshots/img01.jpg" width="360" height="640"/>

## O que é

- Este bot serve para monitorar o preço de um boardgame que você tenha interesse, no site de leilões [Ludopedia](https://www.ludopedia.com.br/). Fiz a pedido de um amigo que é viciado em comprar boardgames nesses leilões da vida.
- O preço dos anúncios do [Ludopedia](https://www.ludopedia.com.br/) é comparado com o preço médio do jogo no [Compara Jogos](https://www.comparajogos.com.br/)
- Caso o preço de um anúncio esteja abaixo da média, o bot te notifica, informando o jogo, o preço, e o link

## Como utilizar

- Este bot está online atualmente, basta clicar no [aqui](https://t.me/board_scrapper_bot) para acessá-lo a em seu Telegram
- Cadastre produtos neles com o comando `/busca <nome do jogo>`
- Pronto. A partir de agora você receberá notificações caso  o bot encontre algum anúncio com preço abaixo da média

## Como eu fiz

Este repositório possuem 2 scripts que são pontos de partida: o `start_bot.py` e o `checker.py`.

- O `start_bot` inicializa o bot e mantém ele ouvindo os comandos. Todo cadastro recebido é salvo no postgres através do `sync`
- O `checker` é o script que faz a verificação periódica, compara os preços, e notifica o usuário. Um scheduler no Heroku roda esse script de hora em hora

Dentro de `modules`, temos:

- O `bot`, é o Bot (dã), implementado usando o [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- O `scrapper` é quem faz a busca no ludopedia, aqui eu uso o [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) para fazer o web scrapping
- O `service` (não arrumei um nome melhor) utiliza o backend do Compara Jogos para buscar o preço médio, através de graphQL (agradeço de coração aos devs do Compara Jogos pelo endpoint)
- O `sync` é quem manipula o banco. Utilizei o [Peewee](http://docs.peewee-orm.com/en/latest/) como ORM

## TODO
- [ ] Não permitir que o bot notifique o usuário mais de uma vez caso encontre um produto abaixo do preço
- [ ] Adicionar um comando `/cancela`, que **remove** um jogo da busca periódica

<img src="https://github.com/renanstd/buscador-de-boardgames/blob/master/screenshots/img02.jpg" width="360" height="720"/>

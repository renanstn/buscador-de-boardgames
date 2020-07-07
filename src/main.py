from modules.bot import Bot
from modules.scrapper import Scrapper
from modules.sync import Sync


def main():
    # telegram_bot = Bot()
    # telegram_bot.listen()
    scrapper = Scrapper()
    results = scrapper.scrap_anuncios('luxor')
    sync = Sync()
    sync.bulk_save(results)
    anuncios = sync.get_all_anuncios()
    print(anuncios)


if __name__ == "__main__":
    main()

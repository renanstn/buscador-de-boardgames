from modules.bot import Bot
from modules.scrapper import Scrapper


def main():
    # telegram_bot = Bot()
    # telegram_bot.listen()
    scrapper = Scrapper()
    scrapper.scrap_anuncios('munchkin')


if __name__ == "__main__":
    main()

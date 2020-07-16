from modules.bot import Bot
from modules.sync import Sync

def main():
    telegram_bot = Bot()
    telegram_bot.listen()


if __name__ == "__main__":
    main()

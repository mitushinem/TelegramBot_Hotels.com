from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.db import init_db
from config_data.config import logger

from telebot.custom_filters import StateFilter
from filters.custom import *


def main():
    try:
        init_db()   # Инициализация базы данных

        set_default_commands(bot)
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitCorrectFilter())
        bot.add_custom_filter(IsFotoCountFilter())
        bot.add_custom_filter(IsPriceCorrectFilter())
        bot.add_custom_filter(IsMessageCorrectFilter())
        bot.add_custom_filter(IsLangCorrectFilter())

        bot.infinity_polling(skip_pending=True)
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()

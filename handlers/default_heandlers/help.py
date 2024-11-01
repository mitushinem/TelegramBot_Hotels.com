from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/<b>{command}</b> - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, '\n'.join(text))

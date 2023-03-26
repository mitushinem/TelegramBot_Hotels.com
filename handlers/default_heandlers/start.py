from telebot.types import Message
from database.db import add_user
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    add_user(message.from_user.full_name, message.from_user.id)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}! \n"
                                      f"Для того что-бы узнать я умею набери /help")

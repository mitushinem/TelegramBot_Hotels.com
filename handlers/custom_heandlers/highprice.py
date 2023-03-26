from telebot.types import Message

from database.db import add_user
from loader import bot
from states.state import StateUser


@bot.message_handler(commands=['highprice'])
def bot_lowprice(message: Message) -> None:
    add_user(message.from_user.full_name, message.from_user.id)
    bot.set_state(message.from_user.id, StateUser.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text

    bot.send_message(message.from_user.id, '<b>В каком городе будем искать отели?</b>')

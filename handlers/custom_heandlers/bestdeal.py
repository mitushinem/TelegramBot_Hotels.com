from telebot.types import Message
import filters.actions
from database.db import add_user
from loader import bot
from states.state import StateUser


@bot.message_handler(commands=['bestdeal'])
def bot_bestdeal(message: Message) -> None:
    add_user(message.from_user.full_name, message.from_user.id)
    bot.set_state(message.from_user.id, StateUser.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text

    bot.send_message(message.from_user.id, '<b>В каком городе будем искать отели?</b>')


@bot.message_handler(state=StateUser.price_range, is_price_correct=True)
def get_price_range(message: Message) -> None:
    """
    Получение диапозона цен для поиска
    """
    bot.set_state(message.from_user.id, StateUser.distance_range, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['priceMin'] = message.text.split(' ')[0]
        data['priceMax'] = message.text.split(' ')[1]

    bot.send_message(message.from_user.id,
                     '<b>Введите диапазон расстояний, на котором находится отель от центра</b>')


@bot.message_handler(state=StateUser.distance_range, is_price_correct=True)
def get_distance_range(message: Message) -> None:
    """
    Получение диапозона расстояний гостиниц от центра
    """
    bot.set_state(message.from_user.id, StateUser.hotel_count, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance_range'] = message.text.split(' ')

    bot.send_message(message.from_user.id, '<b>Сколько отелей вывести в результатах поиска?</b>')

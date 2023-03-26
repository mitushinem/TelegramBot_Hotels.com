from telebot.types import Message

from loader import bot
from states.state import StateUser


@bot.message_handler(state=StateUser.city, is_message_correct=False)
def city_incorrect(message: Message) -> None:
    """
    Обработчик некорректного ввода города для поиска
    """
    bot.send_message(message.from_user.id, 'Вводимое значение города некорректное. Повторите ввод')


@bot.message_handler(state=StateUser.city, is_lang_correct=False)
def city_lang_incorrect(message: Message) -> None:
    """
    Обработчик некорректного ввода города для поиска
    """
    bot.send_message(message.from_user.id, 'Ввод данных должен быть на одном языке')


@bot.message_handler(state=StateUser.hotel_count, is_digit_correct=False)
def hotel_count_incorrect(message: Message) -> None:
    """
    Обработчик некорректного ввода значения кол-ва отелей
    """
    bot.send_message(message.from_user.id, 'Ошибка ввода значения. Повторите ввод.\n'
                                           'Вводимое значение должно быть числом в диапозоне от 1 до 25')


@bot.message_handler(state=StateUser.price_range, is_price_correct=False)
def price_range_incorrect(message: Message) -> None:
    """
    Проверка на некорректный ввод диапозонов цен
    """
    bot.send_message(message.from_user.id,
                     'Вы ввели не корректные значения цен на отели.\n'
                     'Введите два числа через пробел.')


@bot.message_handler(state=StateUser.distance_range, is_price_correct=False)
def price_range_incorrect(message: Message) -> None:
    """
    Проверка на некорректный ввод диапозонов цен
    """
    bot.send_message(message.from_user.id,
                     'Вы ввели не корректный диапазон расстояний.\n'
                     'Введите два числа через пробел.')

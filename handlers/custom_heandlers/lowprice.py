from config_data.config import logger
from database.db import add_user
from handlers.default_heandlers.help import bot_help
from rapid_api.hotels import get_id_destinations
from keyboards.inline.inline_keyboard import *
from keyboards.reply.reply_keyboard import accept_keyboard
from loader import bot
from states.state import StateUser
from utils.utils import is_lang
import filters.actions


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message) -> None:
    add_user(message.from_user.full_name, message.from_user.id)
    bot.set_state(message.from_user.id, StateUser.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
    bot.send_message(message.from_user.id, '<b>В каком городе будем искать отели?</b>')


@bot.message_handler(state=StateUser.city, is_message_correct=True, is_lang_correct=True)
def get_city(message: Message) -> None:
    """
    Получение вариантов поиска по запросу, формирование keyboard с вариантами городов
    """
    lang = is_lang(message.text)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['locale'] = lang[0]
        data['currency'] = lang[1]

        match data['command']:
            case '/lowprice':
                data['sort'] = 'PRICE_LOW_TO_HIGH'
            case '/highprice':
                data['sort'] = 'RECOMMENDED'
            case '/bestdeal':
                data['sort'] = 'DISTANCE'

    bot.send_message(message.chat.id, "<b>Пожалуйста подождите. Запрос выполняется...</b>")

    id_destinations = get_id_destinations(query=message.text, locale=lang)
    if id_destinations:
        bot.send_message(message.chat.id,
                         f'По запросу <b>"{message.text}"</b> найдены варианты:\n'
                         f'Ознакомтесь с предложенными вариантами и выберите наиболее подходящий',
                         reply_markup=keyboard_gen_id_destinations(id_destinations))
    else:
        msg = bot.send_message(message.chat.id,
                               'По вашему запросу ничего не найдено. Повторите запрос заново',
                               reply_markup=keyboard_back())
        bot.delete_state(message.from_user.id, message.chat.id)
        bot_help(msg)


@bot.message_handler(state=StateUser.hotel_count, is_digit_correct=True)
def get_hotel_count(message: Message) -> None:
    """
    Получение hotel_count
    """
    bot.set_state(message.from_user.id, StateUser.data_in, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['resultsSize'] = message.text

    msg = bot.send_message(message.from_user.id, '<b>А теперь определимся с датами проживания</b>', )
    keyboard_data_check_in(msg)


@bot.message_handler(state=StateUser.adults)
def get_rooms_count(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adults'] = message.text
        bot.set_state(message.from_user.id, StateUser.foto_load, message.chat.id)
        bot.send_message(message.chat.id, 'Показать фотографии отелей?', reply_markup=keyboard_foto_check())




#TODO Написать фильтр проверки введа количества проживающих на число и не более 7




@bot.message_handler(state=StateUser.foto_count, is_foto_count_correct=True)
def get_foto_count(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['foto_count'] = message.text
        bot.set_state(message.from_user.id, StateUser.result, message.chat.id)
        bot.send_message(message.from_user.id, 'Для продолжения требуется подтверждение...',
                         reply_markup=accept_keyboard())


@bot.message_handler(state=StateUser.foto_count, is_foto_count_correct=False)
def foto_count_incorrect(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Ошибка ввода значения. Повторите ввод.'
                                           'Вводимое значение должно быть числом в диапозоне от 1 до 5')

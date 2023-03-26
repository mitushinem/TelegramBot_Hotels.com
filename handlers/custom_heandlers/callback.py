import re

from telebot.types import CallbackQuery
from handlers.custom_heandlers.history import get_message_history
from handlers.default_heandlers.help import bot_help
from keyboards.inline.inline_keyboard import *
from keyboards.reply.reply_keyboard import accept_keyboard
from loader import bot
from states.state import StateUser
from utils.utils import is_valid_data_out
from database.db import *


@bot.callback_query_handler(func=lambda call: call.data == 'start')
def callback_start(call: CallbackQuery) -> None:
    """
    Обработчик нажатия по отмена
    """
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.from_user.id, 'Операция отменена. Повторите запрос с новыми параметрами поиска')
    bot_help(msg)


@bot.callback_query_handler(func=lambda call: re.search(r'\|', call.data))
def callback_city(call: CallbackQuery) -> None:
    """
    Обработчик нажатия по кнопке выбора города
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)

    city = call.data.split('|')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['destinationId'] = city[1]
        data['city'] = city[0]
        if data['command'].endswith('price'):
            bot.set_state(call.from_user.id, StateUser.hotel_count, call.message.chat.id)
            bot.send_message(call.from_user.id, 'Сколько отелей вывести в результатах поиска?')
        elif data['command'].endswith('bestdeal'):
            bot.set_state(call.from_user.id, StateUser.price_range, call.message.chat.id)
            bot.send_message(call.from_user.id, 'Введите диапозон цен через пробел?')


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_calendar_1(call: CallbackQuery) -> None:
    """
    Обработка inline callback запросов календаря
    """
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name,
                                           action=action, year=year, month=month, day=day)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        match action:
            case "DAY":
                if date >= date.now().replace(hour=0, minute=0, second=0, microsecond=0):
                    bot.set_state(call.from_user.id, StateUser.data_out, call.message.chat.id)
                    data['checkInDate'] = {"day": day,
                                           "month": month,
                                           "year": year
                                           }
                    data['checkIn'] = date.strftime('%Y-%m-%d')
                    bot.send_message(call.from_user.id, 'Дата заезда: {}'.format(data['checkIn']))
                    msg = bot.send_message(call.from_user.id, '<b>Выберите дату выезда из отеля</b>')
                    keyboard_data_check_out(msg)
                else:
                    msg = bot.send_message(call.from_user.id, '<b>Неверная дата. Повторите выбор</b>')
                    keyboard_data_check_in(msg)

            case "CANCEL":
                bot.delete_state(call.from_user.id, call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       'Операция отменена. Повторите запрос с новыми параметрами поиска')
                bot_help(msg)


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_2_callback.prefix))
def callback_calendar_2(call: CallbackQuery) -> None:
    """
    Обработка inline callback запросов календаря
    """
    name, action, year, month, day = call.data.split(calendar_2_callback.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name,
                                           action=action, year=year, month=month, day=day)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        match action:
            case "DAY":
                data_out = date.strftime('%Y-%m-%d')
                days = is_valid_data_out(data['checkIn'], data_out)
                if days > 0:
                    data['days'] = days
                    data['checkOut'] = data_out
                    data['checkOutDate'] = {"day": day,
                                           "month": month,
                                           "year": year
                                           }

                    bot.send_message(call.from_user.id, 'Дата выезда: {}'.format(data['checkOut']))
                    bot.set_state(call.from_user.id, StateUser.adults, call.message.chat.id)
                    bot.send_message(call.message.chat.id, 'Сколько человек будет проживать в номере?')

                else:
                    msg = bot.send_message(call.from_user.id, 'Ошибка. Выберите дату позднее даты заезда в отель.')
                    keyboard_data_check_out(msg)

            case "CANCEL":
                bot.delete_state(call.from_user.id, call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       'Операция отменена. Повторите запрос с новыми параметрами поиска')
                bot_help(msg)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_foto'))
def callback_foto_download(call: CallbackQuery) -> None:
    """
    Обработчик нажатия по кнопке выбора показа фото в выдаче или нет
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        match call.data:
            case 'yes_foto':
                data['load_image'] = True
                bot.set_state(call.from_user.id, StateUser.foto_count, call.message.chat.id)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.from_user.id, 'Сколько фотографий отеля загружать, но не более 5?')
            case 'no_foto':
                data['load_image'] = False
                bot.set_state(call.from_user.id, StateUser.result, call.message.chat.id)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.from_user.id, 'Для продолжения требуется подтверждение...',
                                 reply_markup=accept_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith('is_'))
def callback_history(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        match call.data:
            case 'is_today':
                for i_msg in select_all_record_for_days(call.from_user.id):
                    bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
                                     disable_web_page_preview=True)
            case 'is_week':
                pass
                for i_msg in select_all_record_for_days(call.from_user.id, days=7):
                    bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
                                     disable_web_page_preview=True)
            case 'is_month':
                for i_msg in select_all_record_for_days(call.from_user.id, days=30):
                    bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
                                     disable_web_page_preview=True)
            case 'is_all':
                for i_msg in select_all_record(call.from_user.id):
                    bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
                                     disable_web_page_preview=True)
            case 'is_delete':
                delete_all_record(call.from_user.id)
    except Exception as err:
        bot.send_message(call.from_user.id, err)

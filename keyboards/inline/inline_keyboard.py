from typing import List, Tuple
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
from loader import bot

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
calendar_2_callback = CallbackData("calendar_2", "action", "year", "month", "day")


def keyboard_gen_id_destinations(id_destinations: List[Tuple]) -> InlineKeyboardMarkup:
    """
    Генерация Inline клавиатуры с вариантами городов при вводе запроса пользователя
    """

    gen_keyboard = InlineKeyboardMarkup()

    for elem in id_destinations:
        key = InlineKeyboardButton(text=elem[0], callback_data='|'.join((elem[0], elem[1])))
        gen_keyboard.add(key)
    key = InlineKeyboardButton(text="Отмена операции", callback_data='start')
    gen_keyboard.add(key)

    return gen_keyboard


def keyboard_back(text_message: str = 'Отмена операции') -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой Отмена
    """
    key_back = InlineKeyboardMarkup()
    key = InlineKeyboardButton(text=text_message, callback_data='start')
    key_back.add(key)
    return key_back


def keyboard_data_check_in(message: Message) -> None:
    """
    Вывод клавиатуры-календарь для выбора дата заезда в отель
    """
    #bot.delete_message(message.chat.id, message.message_id)
    now = datetime.now()

    bot.send_message(message.chat.id,
                     '<b>Выберите дату заезда в отель</b>',
                     reply_markup=calendar.create_calendar(name=calendar_1_callback.prefix,
                                                           year=now.year,
                                                           month=now.month,
                                                           ),
                     )


def keyboard_data_check_out(message: Message) -> None:
    """
    Вывод клавиатуры-календарь для выбора даты выезда из отеля
    """
    #bot.delete_message(message.chat.id, message.message_id)

    now = datetime.now()

    bot.send_message(message.chat.id,
                     "<b>Выберите дату выселения из отеля</b>",
                     reply_markup=calendar.create_calendar(name=calendar_2_callback.prefix,
                                                           year=now.year, month=now.month,
                                                           ),
                     )


def keyboard_foto_check() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора да\нет для загрузки фото в выдаче
    """
    key_foto = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Да', callback_data='yes_foto')
    key_foto.add(key_yes)
    key_no = InlineKeyboardButton(text='Нет', callback_data='no_foto')
    key_foto.add(key_no)

    return key_foto


def keyboard_history() -> InlineKeyboardMarkup:
    """
    Генерация Inline клавиатуры с вариантами городов при вводе запроса пользователя
    """
    keyboard = InlineKeyboardMarkup()

    key_1 = InlineKeyboardButton(text='За сегодня', callback_data='is_today')
    key_2 = InlineKeyboardButton(text='За неделю', callback_data='is_week')
    key_3 = InlineKeyboardButton(text='За месяц', callback_data='is_month')
    key_2_1 = InlineKeyboardButton(text='Вся история', callback_data='is_all')
    key_3_1 = InlineKeyboardButton(text='Удалить всю историю', callback_data='is_delete')

    keyboard.add(key_1, key_2, key_3)
    keyboard.add(key_2_1)
    keyboard.add(key_3_1)

    return keyboard

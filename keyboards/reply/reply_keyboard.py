from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def accept_keyboard() -> ReplyKeyboardMarkup:
    key_markup = ReplyKeyboardMarkup(True, True)
    btn1 = KeyboardButton('Подтвердить')
    btn2 = KeyboardButton('Отмена')
    key_markup.add(btn1, btn2)

    return key_markup

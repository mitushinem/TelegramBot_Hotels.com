import re

from telebot.types import Message
from telebot.custom_filters import SimpleCustomFilter


class IsDigitCorrectFilter(SimpleCustomFilter):
    """
    # проверка message.text на числа и значение в диапозоне от 1 до 25
    Пример использования:
    @bot.message_handler(is_digit_correct=True)
    """
    key = 'is_digit_correct'

    def check(self, message: Message) -> bool:
        return message.text.isdigit() and 0 < int(message.text) < 26


class IsFotoCountFilter(SimpleCustomFilter):
    """
    # проверка вводимого значения "Количество фото при выводе" на числа и значение в диапозоне от 1 до 5
    Пример использования:
    @bot.message_handler(is_foto_count_correct=True)
    """
    key = 'is_foto_count_correct'

    def check(self, message: Message) -> bool:
        return message.text.isdigit() and 0 < int(message.text) < 6


class IsPriceCorrectFilter(SimpleCustomFilter):
    """
    проверка message.text два числа, разделенных пробелом
    Пример использования:
    @bot.message_handler(is_price_correct=True)
    """
    key = 'is_price_correct'

    def check(self, message: Message) -> bool:
        msg = message.text.split(' ')
        return len(msg) == 2 and all(map((lambda x: x.isdigit()), msg)) and int(msg[1]) > int(msg[0])


class IsMessageCorrectFilter(SimpleCustomFilter):
    """
    Проверка на остутствие спецсимволов или цифр в передаваемой строке
    Пример использования:
    @bot.message_handler(is_message_correct=True)
    """
    key = 'is_message_correct'

    def check(self, message: Message) -> bool:
        bad_chars = '$^=?\".,:;\'!_*+()\\[]{}|/#%&\n\t0123456789'

        return not any(char in bad_chars for char in message.text)


class IsLangCorrectFilter(SimpleCustomFilter):
    """
    Проверка на корректный язык ввода
    Пример использования:
    @bot.message_handler(is_message_correct=True)
    """
    key = 'is_lang_correct'

    def check(self, message: Message) -> bool:
        msg_rus = re.search(r'[а-яА-Я\- ]+', message.text)
        msg_eng = re.search(r'[a-zA-Z\- ]+', message.text)

        if msg_rus is not None and len(msg_rus.group()) == len(message.text):
            return True
        elif msg_eng is not None and len(msg_eng.group()) == len(message.text):
            return True

        return False






# def is_lang(message: str) -> Union[Tuple[str, str], None]:
#     """
#     Проверки языка ввода от пользователя
#     """
#     pattern_rus = r'[а-яА-Я\- ]+'
#     pattern_eng = r'[a-zA-Z\- ]+'
#     try:
#         msg_rus = re.search(pattern_rus, message)
#         msg_eng = re.search(pattern_eng, message)
#
#         if msg_rus is not None and len(msg_rus.group()) == len(message):
#             return 'ru_RU', 'RUB'
#         elif msg_eng is not None and len(msg_eng.group()) == len(message):
#             return 'en_US', 'USD'
#
#     except ValueError as err:
#         logger.error(err)

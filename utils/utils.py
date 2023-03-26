import re
import time
from datetime import datetime
from random import randint
from typing import Tuple, Union, List, Set


def is_lang(message: str) -> Union[Tuple[str, str], None]:
    """
    Определение языка ввода и валюты
    """
    if re.search(r'[а-яА-Я\- ]+', message) is not None:
        return 'ru_RU', 'RUB'
    elif re.search(r'[a-zA-Z\- ]+', message) is not None:
        return 'en_US', 'USD'


def get_day_from_date(data: str) -> datetime:
    """
    преобразование строки в объект datatime
    """
    v_date = time.strptime(data, '%Y-%m-%d')
    dt = datetime.fromtimestamp(time.mktime(v_date))
    return dt


def is_valid_data_out(data_in: str, data_out: str) -> int:
    """
    Получаем количество дней разницей двух дат
    """
    d_in = get_day_from_date(data_in)
    d_out = get_day_from_date(data_out)

    return (d_out - d_in).days


def random_index_foto(arr: List, count: str) -> Set:
    """
    генерируется уникальный список индексов для получения всегда разных фото
    """
    index_foto = set()

    while True:
        if len(index_foto) == int(count):
            break
        index_foto.add(randint(0, len(arr)-1))

    return index_foto

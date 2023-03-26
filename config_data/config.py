import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger
from pathlib import Path

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Самые дешевые отели'),
    ('highprice', 'Самые дорогие отели'),
    ('bestdeal', 'Выбрать отели по своим параметрам'),
    ('history', 'История запросов'),
)

HEADERS_HOTEL_API = {
    'content-type': 'application/json',
    'x-rapidapi-host': 'hotels4.p.rapidapi.com',
    'x-rapidapi-key': RAPID_API_KEY
}

URL_API = {
    'search_v3': 'locations/v3/search',
    'list_v2': 'properties/v2/list',
    'get_detail_v2': 'properties/v2/detail',
}

logger.add(Path.cwd() / 'log' / 'bot_hotels.log', compression='zip',
           rotation='10MB', format='{time} {level} {message}', level='DEBUG')

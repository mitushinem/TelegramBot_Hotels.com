import json
import requests
from requests import RequestException
from config_data.config import HEADERS_HOTEL_API, URL_API, logger
from requests.exceptions import ConnectTimeout, HTTPError, ConnectionError
from typing import Union


def api_request(method_endswith, params: dict, method_type: str):
    """"
    :param method_endswith: Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
    :param params: Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
    :param method_type: GET\POST
    """
    # TODO описать typing

    url_api = f'https://hotels4.p.rapidapi.com/{method_endswith}'

    match method_type:
        case 'GET':
            return get_request(url=url_api, params=params)
        case 'POST':
            return post_request(url=url_api, payload=params)


def get_request(url: str, params: dict):
    """
    GET запрос на сервер
    """
    try:
        response = requests.get(url=url, headers=HEADERS_HOTEL_API, params=params, timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            response.raise_for_status()
    except RequestException as err:
        logger.error(str(err))


def post_request(url, payload):
    """
    Отправка POST запроса на сервер, получение ответа в json
    """
    try:
        response = requests.post(url=url, headers=HEADERS_HOTEL_API, json=payload, timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            response.raise_for_status()

    except RequestException as err:
        logger.error(str(err))


def get_id_destinations(query: str, locale: tuple) -> list[tuple]:
    """
    Метод получает списка возможных городов по запросу пользователя. Поиск по двум локалям.
    На вход поступает точный или примерный запрос от пользователя с названием региона поиска
    :param query: str строка запроса поиска от пользователя
    :param locale: Tuple (локаль, валюта)

    :return List
    Пример результата работы метода:
    ('Москва', '1153093'), ('Центр Москвы', '10565407'), ('Измайлово', '10779356'), ('Арбат', '1665959')
    """
    try:
        query_json = {
            'q': query,
            'locale': locale[0],
        }
        response = api_request(method_endswith=URL_API['search_v3'], method_type='GET', params=query_json)
        data = json.loads(response)

        if data['sr']:
            return [(i_elem['regionNames']['shortName'], i_elem['gaiaId']) for i_elem in data['sr']
                    if i_elem['type'] == 'CITY']
        else:
            raise ValueError(f'Регион "{query}" не найден. Выполнение невозможно')

    except Exception as err:
        logger.error(err.args)


def generate_json_info_hotel(date_dict: dict, command: Union[str, None] = None) -> dict:
    payload = {
        'currency': date_dict['currency'],
        'eapid': 1,
        'locale': date_dict['locale'],
        'destination': {'regionId': date_dict['destinationId']},
        'checkInDate': {
            'day': int(date_dict['checkInDate']['day']),
            'month': int(date_dict['checkInDate']['month']),
            'year': int(date_dict['checkInDate']['year'])
        },
        'checkOutDate': {
            'day': int(date_dict['checkOutDate']['day']),
            'month': int(date_dict['checkOutDate']['month']),
            'year': int(date_dict['checkOutDate']['year'])
        },
        'rooms': [
            {
                'adults': int(date_dict['adults']),
            }
        ],
        'resultsStartingIndex': 0,
        'resultsSize': int(date_dict['resultsSize']),
        'sort': date_dict['sort'],
        'filters': {
            'availableFilter': 'SHOW_AVAILABLE_ONLY',
        }
    }
    if command == '/bestdeal':
        payload['filters']['price'] = {'max': date_dict['priceMax'], 'min': date_dict['priceMin']}

    return payload

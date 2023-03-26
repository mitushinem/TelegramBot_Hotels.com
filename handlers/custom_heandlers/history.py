import json
from telebot.types import Message
from keyboards.inline.inline_keyboard import keyboard_history
from loader import bot


def get_message_history(query: dict) -> list:
    list_url = json.loads(query['hotels'])['url']

    msg = [
        '<b>Дата запроса: </b>{}'.format(query['created_at'].strftime('%Y-%m-%d %H:%M:%S')),
        '<b>Команда: </b>{}\n'.format(query['command']),
        '<b>Город: </b>{}\n'.format(query['city']),
        '<b>Список найденных отелей:\n</b>',
        '{}'.format('\n'.join(list_url))
    ]
    return msg


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Выберите вариант поиска запросов', reply_markup=keyboard_history())

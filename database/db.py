from database.models import *
from config_data.config import logger
from datetime import datetime, timedelta
from typing import Iterator


def init_db() -> None:
    """
    Инициализация БД и создание таблиц
    """

    try:
        db.connect()
        db.create_tables([User, History])

    except InternalError as err:
        logger.error(err)


def add_user(name: str, telegram_id: int) -> None:
    """
    Добавление записи в БД в таблицу User о новом пользователе
    """

    with db:
        try:
            User.get(User.telegram_id == telegram_id)
        except DoesNotExist:
            User.create(name=str(name.strip()), telegram_id=telegram_id)
            logger.info(f'Пользователь с ID {telegram_id} создан')


def add_record(telegram_id, command, date, hotels, city):
    """
    Добавление записи в БД
    """

    with db:
        try:
            user = User.get(User.telegram_id == telegram_id)
            History.create(command=command, hotels=hotels, user_id=user, created_at=date, city=city)

        except DoesNotExist as err:
            logger.error(err)


def select_all_record(telegram_id: int) -> Iterator:
    """
    получить все записи из БД за весь период
    """

    with db:
        user = User.select(User.user_id).where(User.telegram_id == telegram_id)
        query = History.select().where(History.user_id.in_(user))

        if query.exists():
            for record in query.dicts().execute():
                yield record
        else:
            raise Exception('Нет записей в базе данных')


def select_all_record_for_days(telegram_id: int, days: int = 0) -> Iterator:
    if days == 0:
        lo = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        lo = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
    hi = datetime.now().replace(microsecond=0)

    with db:
        user = User.select(User.user_id).where(User.telegram_id == telegram_id)  # <class 'peewee.ModelSelect'>
        query = History.select().where((History.user_id.in_(user)) & (History.created_at.between(lo, hi)))

        if query.exists():
            for record in query.dicts().execute():
                yield record
        else:
            raise Exception('Нет записей в базе данных')


def delete_all_record(telegram_id: int) -> None:
    with db:
        user_to_delete = User.select(User.user_id).where(User.telegram_id == telegram_id)
        query = History.delete().where(History.user_id.in_(user_to_delete))
        try:
            query.execute()
        except:
            raise 'Нет записей в базе данных'


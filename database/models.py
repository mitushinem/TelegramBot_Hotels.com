from datetime import datetime
from pathlib import Path
from peewee import *

db = SqliteDatabase(Path.cwd()/'database'/'hotels-tb.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = AutoField(null=False)
    name = CharField(max_length=100)
    telegram_id = IntegerField(unique=True, null=False)
    data_registration = DateField(default=datetime.now)

    class Meta:
        order_by = ('data_registration',)


class History(BaseModel):
    query_id = AutoField(null=False)
    user_id = ForeignKeyField(User, to_field='user_id', on_update='CASCADE', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.now)
    command = CharField()
    city = CharField()
    hotels = CharField()

    class Meta:
        order_by = ('user_id',)

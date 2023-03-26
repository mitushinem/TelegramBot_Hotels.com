from telebot.handler_backends import State, StatesGroup


class StateUser(StatesGroup):
    city = State()
    hotel_count = State()
    price_range = State()
    distance_range = State()
    data_in = State()
    data_out = State()
    adults = State()
    children = State()
    foto_load = State()
    foto_count = State()
    result = State()

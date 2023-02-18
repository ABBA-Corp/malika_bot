from aiogram.dispatcher.filters.state import StatesGroup, State


class UserGet(StatesGroup):
    get_name = State()
    get_number = State()
    get_pass = State()
    get_self = State()
    get_card = State()
    get_model = State()
    get_phone = State()
    get_color = State()
    get_type = State()
    get_conf = State()

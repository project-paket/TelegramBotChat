from aiogram.dispatcher.filters.state import StatesGroup, State


class Chat(StatesGroup):
    get_id = State()
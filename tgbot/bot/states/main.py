from aiogram.filters.state import State, StatesGroup


class MessageState(StatesGroup):
    message = State()
    check = State()
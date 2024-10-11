from aiogram.filters.state import State, StatesGroup


class MessageState(StatesGroup):
    message = State()
    check = State()
    

class RegistrationState(StatesGroup):
    language = State()
    location = State()
    phone = State()
    code = State()
    name = State()
    

class CreateOrderState(StatesGroup):
    delivery_type = State()
    address = State()
    phone = State()
    comment = State()
    confirm = State()
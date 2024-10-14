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
    orderId = State()
    delivery_type = State()
    location = State()
    address = State()
    addention = State()
    branch = State()
    phone = State()
    full_name = State()
    confirm = State()
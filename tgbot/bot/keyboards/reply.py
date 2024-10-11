from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="smayliki"),
            KeyboardButton(text="ssilki")
        ],
        [
            KeyboardButton(text="calculator"),
            KeyboardButton(text="maxsus btn")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Biror birini tanlang",
    selective=True

)

maxsus_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="location", request_location=True),
            KeyboardButton(text="contact", request_contact=True),
        ],
        [
            KeyboardButton(text="poll", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Orqaga")

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()


location_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Geo-Manzilni yuborish", request_location=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Telefon raqamni yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

delivery_type_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚕 Yetkazib berish"),
            KeyboardButton(text="🏃 Olib ketish"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

def get_address_btn(address: str=None):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📍 Geo-Manzilni yuborish", request_location=True),
            ],
            [
                KeyboardButton(text=address),
            ],
            [
                KeyboardButton(text="⬅️ Ortga"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)
from tgbot.bot.utils.all_texts import BUTTON_TEXTS

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

def back_btn(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["back"][lang]),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def location_btn(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["send_location"][lang], request_location=True),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_btn(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["send_phone"][lang], request_contact=True),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def delivery_type_btn(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["delivery"][lang]),
                KeyboardButton(text=BUTTON_TEXTS["pickup"][lang]),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_address_btn(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["send_location"][lang], request_location=True),
            ],
            [
                KeyboardButton(text=BUTTON_TEXTS["back"][lang]),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def address_confirmation(lang='uz'):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_TEXTS["correct"][lang]),
                KeyboardButton(text=BUTTON_TEXTS["incorrect"][lang]),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


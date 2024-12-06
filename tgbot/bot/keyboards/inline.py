from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.bot.utils.all_texts import BUTTON_TEXTS

ssilki_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram", url="https://t.me/Mamatmusayev_uz"),
            InlineKeyboardButton(text="Youtube", url="https://youtube.com/mamatmusayev.uz/")
        ],

    ]
)
def main_btn(lang='uz'):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['menu'][lang]}", callback_data="categories"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['about_us'][lang]}", callback_data="aboutus"),
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['my_cart'][lang]}", callback_data="mycart"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['branches'][lang]}", callback_data="branches"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['comment'][lang]}", callback_data="comment"),
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['setting'][lang]}", callback_data="settings"),
            ],
        ]
    )


language_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            # InlineKeyboardButton(text="🇺🇸 English", callback_data="en"),
        ],
    ]
)


def cart_btn(empty=True, order_id=None, not_fill_field=True, lang='uz'):
    if empty:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"{BUTTON_TEXTS['add_product'][lang]}", callback_data="categories"),
                ],
                [
                    InlineKeyboardButton(text=f"{BUTTON_TEXTS['back'][lang]}", callback_data="category_0"),
                ],
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['change_product'][lang]}", callback_data=f"changeproducts_{order_id}"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['add_product'][lang]}", callback_data="categories"),
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['order'][lang]}" if not_fill_field else f"{BUTTON_TEXTS['payment'][lang]}", callback_data=f"createToOrder_{order_id}"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['back'][lang]}", callback_data="category_0"),
            ],
        ]
    )

def back_btn(lang='uz'):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['back'][lang]}", callback_data="categories"),
            ],
        ]
    )


def delivery_type_btn(lang='uz'):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['delivery'][lang]}", callback_data="delivery"),
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['pickup'][lang]}", callback_data="pickup"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['back'][lang]}", callback_data="mycart"),
            ],
        ]
    )



def pay_btn(lang='uz'):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['payment'][lang]}", pay=True),
            ],
        ]
    )


def payment_type(order_id, lang='uz'):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Payme", callback_data=f"payme_{order_id}"),
                InlineKeyboardButton(text="💳 Click", callback_data=f"click_{order_id}"),
            ],
            [
                InlineKeyboardButton(text=f"{BUTTON_TEXTS['back'][lang]}", callback_data="mycart"),
            ],
        ]
    )

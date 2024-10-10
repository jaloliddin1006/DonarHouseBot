from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ssilki_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram", url="https://t.me/Mamatmusayev_uz"),
            InlineKeyboardButton(text="Youtube", url="https://youtube.com/mamatmusayev.uz/")
        ],

    ]
)

main_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Menu", callback_data="categories"),
        ],
        [
            InlineKeyboardButton("Biz haqimizda", callback_data="aboutus"),
            InlineKeyboardButton("Buyurtmalarim", callback_data="myorders"),
        ],
        [
            InlineKeyboardButton("Filiallar", callback_data="branches"),
        ],
        [
            InlineKeyboardButton("Fikr bildirish", callback_data="comment"),
            InlineKeyboardButton("Sozlamalarim", callback_data="settings"),
        ],
    ]
)


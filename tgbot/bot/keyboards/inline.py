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
            InlineKeyboardButton(text="🛒 Menu", callback_data="categories"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data="aboutus"),
            InlineKeyboardButton(text="🛍 Buyurtmalarim", callback_data="myorders"),
        ],
        [
            InlineKeyboardButton(text="📍 Filiallar", callback_data="branches"),
        ],
        [
            InlineKeyboardButton(text="💬 Fikr bildirish", callback_data="comment"),
            InlineKeyboardButton(text="⚙️ Sozlamalarim", callback_data="settings"),
        ],
    ]
)

language_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="en"),
        ],
    ]
)

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
            InlineKeyboardButton(text="🛍 Savatcha", callback_data="mycart"),
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


def cart_btn(empty=True, order_id=None, not_fill_field=True):
    if empty:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🛒 Maxsulot qo'shish", callback_data="categories"),
                ],
                [
                    InlineKeyboardButton(text="⬅️ Ortga", callback_data="category_0"),
                ],
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Maxsulotlarni o'zgartirish", callback_data=f"changeproducts_{order_id}"),
            ],
            [
                InlineKeyboardButton(text="🛒 Maxsulot qo'shish", callback_data="categories"),
                InlineKeyboardButton(text="🚚 Buyurtma qilish" if not_fill_field else "💳 To'lov qilish", callback_data=f"createToOrder_{order_id}"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Ortga", callback_data="category_0"),
            ],
        ]
    )


back_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="category_0"),
        ],
    ]
)


delivery_type_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚚 Yetkazib berish", callback_data="delivery"),
            InlineKeyboardButton(text="🏃‍♂️ Olib ketish", callback_data="pickup"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="mycart"),
        ],
    ]
)
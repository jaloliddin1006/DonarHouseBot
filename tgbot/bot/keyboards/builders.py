from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def calc_kb():
    items = [
        "1", "2", "3", "+",
        "4", "5", "6", "-",
        "7", "8", "9", "*",
        "0", ".", "=", "/"
    ]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]

    builder.button(text="Orqaga")
    builder.adjust(*[4] * 4, 1)  # 4, 4, 4, 4, 1

    return builder.as_markup(resize_keyboard=True)


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]
    [builder.button(text=item) for item in text]

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def check_channel_sub(channels: list):
    builder = InlineKeyboardBuilder()
    [builder.button(text=name, url=link) for name, link in channels]
    return builder.as_markup()


def get_categories_btn(categories: list = [], back: str = "category_0", user_cart: bool=False):
    builder = InlineKeyboardBuilder()
    len_ = len(categories)
    [builder.button(text=category.name, callback_data=f"category_{category.id}") for category in categories]
    builder.button(text="⬅️ Ortga", callback_data=back)
    builder.adjust(*[2]*(len_//2), 1)  
    if user_cart:
        builder.button(text="🛍 Savatcha", callback_data='mycart')
    return builder.as_markup()

def get_products_btn(products: list, back: str):
    len_ = len(products)
    builder = InlineKeyboardBuilder()
    [builder.button(text=product.get('name'), callback_data=f"product_{product.get('id')}") for product in products]
    builder.button(text="⬅️ Ortga", callback_data=back)
    builder.adjust(*[2]*(len_//2), 1)  
    return builder.as_markup()

def get_brancches_btn(branches: list):
    len_ = len(branches)
    builder = InlineKeyboardBuilder()
    [builder.button(text=branch.name, callback_data=f"branch_{branch.id}") for branch in branches]
    builder.button(text="⬅️ Ortga", callback_data="branch_0")
    builder.adjust(*[2]*(len_//2), 1)  
    return builder.as_markup()


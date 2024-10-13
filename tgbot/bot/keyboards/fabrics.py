from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from tgbot.bot.loader import bot, STICERS


class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page).pack()),
        width=2

    )
    return builder.as_markup()


class ProductValue(CallbackData, prefix='pag'):
    action: str
    count: int
    product_id: int
    category_id: int


def value_compressor(cnt: int = 0, pro_id: int = 0, ctg_id: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➖", callback_data=ProductValue(action="remove", count=cnt, product_id=pro_id, category_id=ctg_id).pack()),
        InlineKeyboardButton(text=f"{cnt}", callback_data="none"),
        InlineKeyboardButton(text="➕", callback_data=ProductValue(action="add", count=cnt, product_id=pro_id, category_id=ctg_id).pack()),
        width=3

    )
    builder.row(
        InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=ProductValue(action=f"addcart", count=cnt, product_id=pro_id, category_id=ctg_id).pack()),
        InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"category_{ctg_id}"),
        width=1        
    )
    return builder.as_markup()


class ChangeOrderProductsValue(CallbackData, prefix='pag'):
    action: str
    quantity: int
    orderItemId: int
    order_id: int

def change_values(orderItems: list = [], order_id: int = 0):
    builder = InlineKeyboardBuilder()
    for index, item in orderItems:
        builder.row(
            InlineKeyboardButton(text="➖", callback_data=ChangeOrderProductsValue(action=f"remove_{item.get('id')}", orderItemId=item.get("id"), order_id=order_id, quantity=item.get('quantity')).pack()),
            InlineKeyboardButton(text=f"{STICERS[index]}", callback_data="none"),
            # InlineKeyboardButton(text=f"{item.get('product__name')}", callback_data="none"),
            InlineKeyboardButton(text="➕", callback_data=ChangeOrderProductsValue(action=f"add_{item.get('id')}", orderItemId=item.get("id"), order_id=order_id, quantity=item.get('quantity')).pack()),
            width=3
        )
    builder.row(
        InlineKeyboardButton(text="🔄 Savatni Bo'shatish", callback_data="clearOrder"),
        InlineKeyboardButton(text="⬅️ Ortga", callback_data="mycart"),
        width=1
    )
    return builder.as_markup()
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


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


def value_compressor(cnt: int = 0, pro_id: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➖", callback_data=ProductValue(action="remove", count=cnt, product_id=pro_id).pack()),
        InlineKeyboardButton(text=f"{cnt}", callback_data="none"),
        InlineKeyboardButton(text="➕", callback_data=ProductValue(action="add", count=cnt, product_id=pro_id).pack()),
        width=3

    )
    builder.row(
        InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=ProductValue(action=f"addcart", count=cnt, product_id=pro_id).pack()),
        InlineKeyboardButton(text="⬅️ Kategoriyalar", callback_data="categories"),
        width=1        
    )
    return builder.as_markup()

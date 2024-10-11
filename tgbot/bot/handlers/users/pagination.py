from contextlib import suppress
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from tgbot.bot.keyboards import fabrics
from aiogram import Router, F
from asgiref.sync import sync_to_async
from tgbot.models import Product
from tgbot.bot.loader import STICERS
# from data.subloader import get_json

router = Router()


@router.callback_query(fabrics.ProductValue.filter(F.action.in_(['remove', 'add'])))
async def pagination_handler(call: CallbackQuery, callback_data: fabrics.ProductValue):
    await call.answer()
    current_count = int(callback_data.count)
    product_id = int(callback_data.product_id)
    action = callback_data.action
    count = current_count - 1 if current_count > 0 else 0
    if action == 'add':
        count = current_count + 1 if current_count < 11 - 1 else current_count
            
    product = await sync_to_async(Product.objects.get)(id=product_id)
    caption = f"Nomi: <b>{product.name}</b> \n"
    caption += f"Tavsif: {product.description}\n"
    caption += f"Narxi: {product.price} so'm \n\n"
    caption += f"{STICERS[count]} x {product.price} = {product.price*count} so'm"
    # print(caption)
    with suppress(TelegramBadRequest):
        await call.message.edit_caption(caption=caption, reply_markup=fabrics.value_compressor(count, pro_id=product_id, ctg_id=product.category_id))
    # await call.answer("xatolik!!", show_alert=True)
    
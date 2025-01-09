from contextlib import suppress
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from tgbot.bot.handlers.users.utils import get_cart_items_text
from tgbot.bot.keyboards import fabrics
from aiogram import Router, F
from asgiref.sync import sync_to_async
from tgbot.models import OrderItem, Product
from tgbot.bot.loader import STICERS
from tgbot.bot.utils.all_texts import REGISTER_TEXTS


router = Router()


@router.callback_query(fabrics.ProductValue.filter(F.action.in_(['remove', 'add'])))
async def pagination_handler(call: CallbackQuery, callback_data: fabrics.ProductValue, user_language: str='uz'):
    await call.answer()
    current_count = int(callback_data.count)
    product_id = int(callback_data.product_id)
    action = callback_data.action
    count = current_count - 1 if current_count > 0 else 0
    if action == 'add':
        count = current_count + 1 if current_count < 11 - 1 else current_count
            
    product = await sync_to_async(Product.objects.get)(id=product_id)
    caption = f"{REGISTER_TEXTS['name'][user_language]}: <b>{product.name}</b> \n"
    caption += f"{REGISTER_TEXTS['description'][user_language]}: {product.description}\n"
    caption += f"{REGISTER_TEXTS['price'][user_language]}: {product.price} UZS \n\n"
    caption += f"{STICERS[count]} x {product.price} = {product.price*count} UZS"
    

    if call.message.caption:  
        await call.message.edit_caption(
            caption=caption,
            reply_markup=fabrics.value_compressor(
                count,
                pro_id=product_id,
                ctg_id=product.category_id,
                lang=user_language
            )
        )
    else:  
        await call.message.edit_text(
            text=caption,
            reply_markup=fabrics.value_compressor(
                count,
                pro_id=product_id,
                ctg_id=product.category_id,
                lang=user_language
            )
        )
    # await call.answer("xatolik!!", show_alert=True)


@router.callback_query(fabrics.ChangeOrderProductsValue.filter(F.action.startswith('remove') | F.action.startswith('add')))
async def change_order_products_value(call: CallbackQuery, callback_data: fabrics.ChangeOrderProductsValue, user_language: str='uz'):
    await call.answer()
    action = callback_data.action.split('_')[0]
    orderItemId = callback_data.orderItemId
    orderId = callback_data.order_id
    quantity = callback_data.quantity
    count = quantity - 1 if quantity > 0 else 0
    if action == 'add':
        count = quantity + 1 if quantity < 11 - 1 else quantity
        
    orderItem = await sync_to_async(OrderItem.objects.get)(id=orderItemId)
    if count == 0:
        await orderItem.adelete()
    else:   
        orderItem.quantity = count
        await orderItem.asave()
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=orderId))
    
    # orderItems = list(enumerate(orderItems, 1))
    text = await get_cart_items_text(list(enumerate(orderItems, 1)), user_language=user_language)
    # print(text)
    with suppress(TelegramBadRequest):
        await call.message.edit_text(text, reply_markup=fabrics.change_values(list(enumerate(orderItems, 1)), order_id=orderId, lang=user_language ))
    # await call.answer("xatolik!!", show_alert=True)
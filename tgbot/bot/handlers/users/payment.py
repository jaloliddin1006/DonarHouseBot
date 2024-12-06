from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from tgbot.bot.handlers.users.utils import get_cart_items_text
from tgbot.bot.loader import bot, STICERS
from tgbot.bot.handlers.users.main import my_cart_message
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.bot.states.main import CreateOrderState
from tgbot.utils import get_address
from tgbot.models import Branch, User, Category, Product, Order, OrderItem, Payment
from PIL import Image
from io import BytesIO
import os
from django.conf import settings
from tgbot.bot.utils.all_texts import BOT_WORDS

router = Router()    

from aiogram import types
from aiogram.types import LabeledPrice

from tgbot.bot.utils.payment_data import Product


async def create_invoice(order: Order, isQrCode=None, payment='click'):
    prices = []
    delivery_price = 0
    
    if payment == 'click':
        provider_token = settings.PAYMENT_TOKEN_CLICK
    else:
        provider_token = settings.PAYMENT_TOKEN_PAYMEE
    
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=order.id))
    print(isQrCode)
    
    for item in orderItems:
        prices.append(
            LabeledPrice(
                label=f"""{item.get("quantity")}  x  {item.get("product__name")}""",
                amount=item.get("total_price")*100
            )
        )
        
    
    if order.delivery == 'pickup':
        ...
    else:
        prices.append(
            LabeledPrice(
                label="Yetkazib berish",
                amount=delivery_price
            )
        )
        # if isQrCode:
        #     prices.append(
        #         LabeledPrice(
        #             label="Chegirma",
        #             amount=-(delivery_price/10) # 10 % chegirma
        #         )
        #     )
    

    invoice = Product(
        title="To'lovni amalga oshirish",
        description="""Siz tanlagan maxsulotlaringiz uchun to'lovni amalga oshirasiz. Bu yerda kartangiz xavfsizligiga bankni o'zi javobgardir. """,
        currency="UZS",
        prices=prices,
        start_parameter="create_invoice_products",
        photo_url="https://media.istockphoto.com/vectors/mobile-tax-form-concept-vector-id1322978180?b=1&k=20&m=1322978180&s=612x612&w=0&h=rtd2ba3P2hyqcPfquqOy70M7609d8tBzGKq1xYhtl7M=",
        photo_width = 1246,
        photo_height = 823,
        need_email=False,
        need_name=True,
        need_phone_number=True,
        provider_token = provider_token,
        # max_tip_amount = 1000000,
        # suggested_tip_amounts = [100000, 200000, 500000]
        
    )
    
    return invoice

async def get_order_full_info(order_id, user_language='uz'):

    order = await sync_to_async(Order.objects.get_full_order, thread_sensitive=True)(order_id)
    
    # print(order.get("delivery"))
    text = f"{BOT_WORDS['order_info'].get(user_language)}\n\n"
    if order.delivery == 'pickup':
        # branch = await sync_to_async(Branch.objects.get)(id=order.branch)
        
        text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>Olib ketish</b>\n"
        text += f"""{BOT_WORDS['branch'].get(user_language)}: <a href="{order.get('branch__location')}"><b>{order.get('branch__name')}</b></a>\n"""
        text += f"{BOT_WORDS['order_user'].get(user_language)}: <b>{order.full_name}</b>\n"
        text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{order.phone}</b>\n"
    else:
        text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>Yetkazib berish</b>\n"
        text += f"{BOT_WORDS['order_user_input'].get(user_language)}: <b>{order.full_name}</b>\n"
        text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{order.phone}</b>\n"
        text += f"{BOT_WORDS['order_address'].get(user_language)}: <b>{order.address}</b>\n"
        text += f"{BOT_WORDS['location'].get(user_language)}: <b>{order.location}</b>\n"
        text += f"{BOT_WORDS['order_addention'].get(user_language)}: <b>{order.addention}</b>\n\n"
    text += f"{BOT_WORDS['order_status'].get(user_language)}: <b>{BOT_WORDS['payment_wait'].get(user_language)}</b>"

    return text

@router.callback_query(F.data=="payment")
async def payment_to_order(call: types.CallbackQuery, order: Order = None, user_language: str='uz'):
    # orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=order.id))
    # order_info = await get_cart_items_text(enumerate(orderItems, 1), order)
    await call.answer()
    
    await call.message.delete_reply_markup()
    
    await call.message.answer(f"{BOT_WORDS['choose_payment_type'].get(user_language)}", reply_markup=inline.payment_type(order.id, user_language))
    
@router.callback_query(F.data.startswith("click_"))
async def click_payment(call: types.CallbackQuery, state: FSMContext):
    order_id = call.data.split("_")[1]
    order = await Order.objects.aget(id=order_id)
    await state.clear()
    user = await User.objects.aget(telegram_id=call.from_user.id)
    print(user.isQrCode)
    invoice = await create_invoice(order, user.isQrCode, payment='click')
    await call.message.answer_invoice(**invoice.generate_invoice(), name='alibobo', payload=f"{order.id}")
    

@router.callback_query(F.data.startswith("payme_"))
async def payme_payment(call: types.CallbackQuery, state: FSMContext):
    order_id = call.data.split("_")[1]
    order = await Order.objects.aget(id=order_id)
    await state.clear()
    await call.message.delete_reply_markup()
    user = await User.objects.aget(telegram_id=call.from_user.id)
    print(user.isQrCode)
    invoice = await create_invoice(order, user.isQrCode, payment='payme')
    await call.message.answer_invoice(**invoice.generate_invoice(), name='alibobo', payload=f"{order.id}")

@router.pre_checkout_query()
async def on_pre_checkout_query( pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message, user_language: str='uz'):
    print('successful_payment:')
    GROUP_ID = -4554019429
    # print(message.successful_payment)
       
    order_id = message.successful_payment.invoice_payload
    total_amount = message.successful_payment.total_amount/100
    name = message.successful_payment.order_info.name
    phone = message.successful_payment.order_info.phone_number
    telegram_payment_charge_id = message.successful_payment.telegram_payment_charge_id
    telegram_user_id = message.from_user.id
    telegram_user_full_name = message.from_user.full_name
    provider_payment_charge_id = message.successful_payment.provider_payment_charge_id
    # print(provider_payment_charge_id)

    await Payment.objects.aupdate_or_create(
        order_id=order_id,
        defaults={
        "amount":total_amount,
        "full_name":name,
        "phone":phone,
        "telegram_payment_charge_id":telegram_payment_charge_id,
        "provider_payment_charge_id":provider_payment_charge_id
        }
    )   
    
    order = await Order.objects.aget(id=order_id)
    order.is_paid = True
    order.status = 'completed'
    await order.asave() 
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=order.id))
    order_info = await get_cart_items_text(list(enumerate(orderItems, 1)), order, user_language)
    
    check_sell1 =  f"PAYMENT ID: {telegram_payment_charge_id}\n\n"
    check_sell = f"Order ID: {order_id}\n"
    check_sell +=  f"To'lov: {total_amount} UZS\n"
    check_sell += f"Telegram user: [{telegram_user_full_name}](tg://user?id={telegram_user_id})\n"
    check_sell +=  f"Xaridor: {name}\n"
    check_sell +=  f"Tel: {phone}\n"
    
    await bot.send_message(chat_id=GROUP_ID,
                           text=check_sell1+check_sell,     
                           parse_mode=ParseMode.MARKDOWN                                                         
                            )
 
    await bot.send_message(chat_id=GROUP_ID,
                           text=order_info,     
                           parse_mode=ParseMode.HTML                                                         
                            )
    await message.answer("To'lovingiz qabul qilindi.  \n  Operatorlarimizning siz bilan bog'lanishini kuting. \n 📲 Call-Markaz: +998932977419")
    await message.answer("Asosiy menyu", reply_markup=inline.main_btn)
    
    
# @router.pre_checkout_query()
# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
# #     user_id = pre_checkout_query.from_user.id
# #     payment_id=pre_checkout_query.id
# #     name = pre_checkout_query.order_info.name
# #     phone = pre_checkout_query.order_info.phone_number
# #     total_amount = pre_checkout_query.total_amount/100
# #     payload = pre_checkout_query.invoice_payload
# #     print(payload)
    
#     await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
    
    
#     # db.add_sells_products(user_id, check_sell, check_sell1, date)
    
#     # await bot.send_message(chat_id=CHANEL_CHAT_ID,
#     #                        text=check_sell1+check_sell,
                           
                                                                                           
#     #                         )
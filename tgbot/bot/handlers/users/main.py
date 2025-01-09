from django.conf import settings
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from tgbot.bot.handlers.users.iiko_integration import create_order, get_delivery_info_by_id
from tgbot.utils import get_address
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.models import User, Category, Product, Order, OrderItem, Branch, About
from tgbot.bot.loader import STICERS, bot
from tgbot.bot.states.main import CreateOrderState
from PIL import Image
from io import BytesIO
import os
from tgbot.bot.utils.all_texts import BOT_WORDS, REGISTER_TEXTS


router = Router()

# TODO: commandlar to'g'irlanib qo'shib chiqilishi kerak
@router.message(F.text == "/mycart")
async def my_cart_message(message: types.Message, state: FSMContext, user_language: str='uz'):

    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await message.answer(f"{REGISTER_TEXTS['empty'][user_language]}", reply_markup=inline.cart_btn(empty=True, lang=user_language))
        return True
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
    
    if not orderItems:
        await message.answer(f"{REGISTER_TEXTS['empty'][user_language]}", reply_markup=inline.cart_btn(empty=True, lang=user_language))
        return True
        
    total_price = 0
    text = f"{BOT_WORDS['your_bucket'][user_language]}: \n\n"
    for index, item in enumerate(orderItems, 1):
        text += f"""{STICERS[index]} <b> {item.get("product__name")}</b>\n """
        text += f"""  >  {item.get("quantity")}  x  {int(item.get("product__price"))} UZS => {item.get("total_price")} UZS\n\n"""
        total_price += item.get("total_price")
        
    text += f"<b>{BOT_WORDS['all'][user_language]}: {total_price} UZS </b>"
    
    await message.answer(text, reply_markup=inline.cart_btn(empty=False, lang=user_language), parse_mode=ParseMode.HTML)
        



@router.callback_query(F.data == "branches")
async def branches(call: types.CallbackQuery, state=FSMContext, user_language: str='uz'):
    await call.message.delete()
    branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
    await call.message.answer(f"{REGISTER_TEXTS['get_branches'][user_language]}", reply_markup=builders.get_brancches_btn(branches, lang=user_language))
    
    
@router.callback_query(F.data.startswith("branch_"))
async def get_branch(call: types.CallbackQuery, state=FSMContext, user_language: str='uz'):
    await call.answer()
    branch_id = int(call.data.split("_")[1])
    if branch_id == 0:
        await call.message.delete()
        await call.message.answer(f"{BOT_WORDS['main_sentence'][user_language]} ", reply_markup=inline.main_btn(user_language))
        await state.clear()
        return True
    
    branch = await Branch.objects.aget(id=branch_id)
    branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
    await call.message.edit_text(f"{branch.name}\n{branch.phone}\n{branch.address}\n{branch.working_hours}\n{branch.location}", 
                              reply_markup=builders.get_brancches_btn(branches, lang=user_language))
                                  

@router.callback_query(F.data == "aboutus")
async def about_us(call: types.CallbackQuery, state=FSMContext, user_language: str='uz'):
    about = await About.objects.alast()
    await call.message.edit_text(about.description, reply_markup=inline.back_btn(user_language), parse_mode=ParseMode.MARKDOWN)
    

@router.callback_query(F.data == "settings")
async def settings_func(call: types.CallbackQuery, state=FSMContext, user_language: str='uz'):
    await call.message.edit_text(f"{BOT_WORDS['choose_lang'][user_language]}", reply_markup=inline.language_btn)


@router.callback_query(F.data.startswith("lang_"))
async def change_language(call: types.CallbackQuery, user_language: str='uz'):
    lang_code = call.data.split("_")[-1]
    user = await User.objects.aget(telegram_id=call.from_user.id)
    user.language_code = lang_code
    await user.asave()
    await call.message.edit_text(
        f"{BOT_WORDS['success_change'][user_language]}: {lang_code.upper()}",
        reply_markup=None
    )

@router.message(F.text == "/order_info")
async def my_cart_message(message: types.Message, state: FSMContext, user_language: str='uz'):
    # GROUP_ID = settings.TELEGRAM_GROUP_ID
    # order = await Order.objects.aget(id=3)

    # response = await create_order(order)
    # if response.get("code") == 200:
    #     await bot.send_message(chat_id=GROUP_ID,
    #                        text=f"Buyurtma IIKO ga muvaffaqiyatli qo'shildi. \nIIKO dagi buyurtma ID {response.get('data').get('orderInfo').get('id')}",     
    #                        parse_mode=ParseMode.MARKDOWN                                                         
    #                         )
    # else:
    #     await bot.send_message(chat_id=GROUP_ID,
    #                        text=f"Buyurtma IIKO ga yuborishda muvaffaqiyatsizlikka uchradi. \nIIKO dagi buyurtma ID {response.get('data').get('orderInfo').get('id')}",     
    #                        parse_mode=ParseMode.MARKDOWN                                                         
    #                         )
        
    
    
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await message.answer(f"{REGISTER_TEXTS['empty'][user_language]}")
        return True
    
    response = await get_delivery_info_by_id(userOrder.iiko_order_id)
    print(response)
    await message.answer(f"""Sizning buyurtmangiz: {response}""")
    
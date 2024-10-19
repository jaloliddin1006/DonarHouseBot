from django.conf import settings
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from tgbot.utils import get_address
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.models import User, Category, Product, Order, OrderItem, Branch, About
from tgbot.bot.loader import STICERS, bot
from tgbot.bot.states.main import CreateOrderState
from PIL import Image
from io import BytesIO
import os


router = Router()

# TODO: commandlar to'g'irlanib qo'shib chiqilishi kerak
@router.message(F.text == "/mycart")
async def my_cart_message(message: types.Message, state: FSMContext):

    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await message.answer("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
    
    if not orderItems:
        await message.answer("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
        
    total_price = 0
    text = "Sizning savatingizda quidagilar mavjud: \n\n"
    for index, item in enumerate(orderItems, 1):
        text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> dan\n """
        text += f"""  >  {item.get("quantity")} ta  x  {int(item.get("product__price"))} so'm => {item.get("total_price")} so'm\n\n"""
        total_price += item.get("total_price")
        
    text += f"<b>Jami: {total_price} so'm </b>"
    
    await message.answer(text, reply_markup=inline.cart_btn(empty=False), parse_mode=ParseMode.HTML)
        



@router.callback_query(F.data == "branches")
async def branches(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
    await call.message.answer("Filiallardan birini tanlang", reply_markup=builders.get_brancches_btn(branches))
    
    
@router.callback_query(F.data.startswith("branch_"))
async def get_branch(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    branch_id = int(call.data.split("_")[1])
    if branch_id == 0:
        await call.message.delete()
        await call.message.answer("Biz bilan birga buyurtma qilishga tayyormisiz? ", reply_markup=inline.main_btn)
        await state.clear()
        return True
    
    branch = await Branch.objects.aget(id=branch_id)
    branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
    await call.message.edit_text(f"{branch.name}\n{branch.phone}\n{branch.address}\n{branch.working_hours}\n{branch.location}", 
                              reply_markup=builders.get_brancches_btn(branches))
                                  

@router.callback_query(F.data == "aboutus")
async def about_us(call: types.CallbackQuery, state=FSMContext):
    about = await About.objects.alast()
    await call.message.edit_text(about.description, reply_markup=inline.back_btn, parse_mode=ParseMode.MARKDOWN)
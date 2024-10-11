from django.conf import settings
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from asgiref.sync import sync_to_async
from tgbot.utils import get_address
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.models import User, Category, Product
from tgbot.bot.loader import bot
from tgbot.bot.states.main import CreateOrderState
from PIL import Image
from io import BytesIO
from aiogram.types import InputFile, FSInputFile
import os
router = Router()

# @router.callback_query(F.data=="createorder")
# async def create_order(call: types.CallbackQuery, state=FSMContext):
#     await state.set_state(CreateOrderState.delivery_type)
#     await call.message.answer("Buyurtma turini tanlang", reply_markup=reply.delivery_type_btn)
    

# @router.message(StateFilter(CreateOrderState.delivery_type))
# async def set_delivery_type(message: types.Message, state: FSMContext):
#     delivery_type = message.text
#     await state.update_data(delivery_type=delivery_type)
#     await state.set_state(CreateOrderState.address)
#     user = await User.objects.aget(telegram_id=message.from_user.id)
#     await message.answer("Buyurtma manzilini kiriting", reply_markup=reply.get_address_btn(user.address))
    
    
# @router.message(StateFilter(CreateOrderState.address))
# async def set_address(message: types.Message, state: FSMContext):
#     address = message.text
#     await state.update_data(address=address)
#     await state.set_state(CreateOrderState.phone)
#     await message.answer("Telefon raqamingizni kiriting", reply_markup=reply.get_phone_btn())
    
    
@router.callback_query(F.data=="categories") 
async def categories(call: types.CallbackQuery, state=FSMContext):
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.delete()
    await call.message.answer("Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(categories))

@router.callback_query(F.data.startswith("category_"))
async def get_subcategories(call: types.CallbackQuery, state=FSMContext):
    category_id = int(call.data.split("_")[1])
    await call.message.delete()
    sub_categories = await sync_to_async(list)(Category.objects.sub_ctg(id=category_id))
    if sub_categories:
        await call.message.answer("Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(sub_categories))
    else:
        products = await sync_to_async(list)(Product.objects.filter(category_id=category_id))
        await call.message.answer("Maxsulotlardan birini tanlang", reply_markup=builders.get_products_btn(products))
        

@router.callback_query(F.data.startswith("product_"))
async def get_product(call: types.CallbackQuery, state=FSMContext):
    product_id = int(call.data.split("_")[1])
    await call.message.delete()
    product = await sync_to_async(Product.objects.get)(id=product_id)
    caption = f"Nomi: <b>{product.name}</b> \n"
    caption += f"Tavsif: {product.description}\n"
    caption += f"Narxi: {product.price} so'm"
    if product.image:
        try:
            photo = FSInputFile(product.image.path)  
            await call.message.answer_photo(photo=photo, caption=caption, reply_markup=fabrics.value_compressor(1, product.id))
        except Exception as error:
            await call.message.answer(caption, reply_markup=fabrics.value_compressor(1, product.id))
    else:
        await call.message.answer(caption, reply_markup=fabrics.value_compressor(1, product.id))
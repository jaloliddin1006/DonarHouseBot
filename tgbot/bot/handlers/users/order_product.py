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
from tgbot.models import User, Category, Product, Order, OrderItem
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
    
    
@router.callback_query(F.data == "categories") 
async def categories(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.answer("Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(categories, f"category_{0}"))

@router.callback_query(F.data.startswith("category_"))
async def get_subcategories(call: types.CallbackQuery, state=FSMContext):
    category_id = int(call.data.split("_")[1])
    await call.message.delete()
    if category_id == 0:
        await call.message.answer("Biz bilan birga buyurtma qilishga tayyormisiz? ", reply_markup=inline.main_btn)
        return True
    
    sub_categories = await sync_to_async(list)(Category.objects.sub_ctg(id=category_id))
    category = await Category.objects.aget(id=category_id)
        
    photo = FSInputFile(category.image.path)  
    if sub_categories:
        if sub_categories[0].level == 1:
            await call.message.answer_photo(photo=photo, caption="Sub Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(sub_categories, f"categories"))
        else:
            await call.message.answer_photo(photo=photo, caption="Sub kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(sub_categories, f"category_{sub_categories[0].parent_id}"))
        return True
    
    products = await sync_to_async(list)(Product.objects.get_ctg_products(category_id=category_id))
    if products:
        if products[0].get("category__parent_id"):
            await call.message.answer_photo(photo=photo, caption="Maxsulotlardan birini tanlang", reply_markup=builders.get_products_btn(products, f"category_{products[0].get('category__parent_id')}"))
        else:
            await call.message.answer_photo(photo=photo, caption="Maxsulotlardan birini tanlang", reply_markup=builders.get_products_btn(products, f"categories"))
        return True
    
    await call.answer("Maxsulotlar topilmadi")
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.answer("Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(categories, f"category_{0}"))


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
            await call.message.answer_photo(photo=photo, caption=caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id))
        except Exception as error:
            await call.message.answer(caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id))
    else:
        await call.message.answer(caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id))
        

@router.callback_query(fabrics.ProductValue.filter(F.action.in_(['addcart'])))
async def add_cart(call: types.CallbackQuery, callback_data: fabrics.ProductValue):
    await call.answer()
    quantity = int(callback_data.count)
    product_id = int(callback_data.product_id)
    # action = callback_data.action
    
    user = await sync_to_async(User.objects.get)(telegram_id=call.from_user.id)
    userOrder, created = await sync_to_async(Order.objects.get_or_create)(user=user, status="active")
    await userOrder.asave()
    
    product = await sync_to_async(Product.objects.get)(id=product_id)
    orderItem, created = await sync_to_async(OrderItem.objects.get_or_create)(order=userOrder, product=product, defaults={"quantity": quantity})
    # orderItem.quantity = quantity
    await orderItem.asave()
    
    await call.message.answer(f"'{product.name}' dan {quantity} tasi  savatga qo'shildi")
    await categories(call, state=FSMContext)


@router.callback_query(F.data == "mycart")
async def my_cart(call: types.CallbackQuery, state=FSMContext):
    user_tg_id = call.from_user.id
    await call.message.delete()
    
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await call.message.answer("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
    
    if not orderItems:
        await call.message.answer("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
        
    total_price = 0
    text = "Sizning Savatingizda: \n\n"
    for index, item in enumerate(orderItems, 1):
        text += f"""{index}. {item.get("product__name")} dan\n """
        text += f"""|>  {item.get("product__price")} * {item.get("quantity")} ta => {item.get("total_price")} so'm\n\n"""
        total_price += item.get("total_price")
        
    text += f"Jami: {total_price} so'm"
    
    await call.message.answer(text, reply_markup=inline.cart_btn(empty=False))
        


    
    
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from tgbot.bot.handlers.users.payment import create_invoice, payment_to_order
from tgbot.bot.handlers.users.utils import get_cart_items_text
from tgbot.bot.loader import bot, STICERS
from tgbot.bot.handlers.users.main import my_cart_message
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.bot.states.main import CreateOrderState
from tgbot.bot.utils.all_texts import BOT_WORDS, REGISTER_TEXTS
from tgbot.utils import get_address
from tgbot.models import Branch, User, Category, Product, Order, OrderItem
from PIL import Image
from io import BytesIO

from tgbot.bot.utils.all_texts import BUTTON_TEXTS

router = Router()    


@router.callback_query(F.data == "categories") 
async def categories(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    await call.message.delete()
    text = f"{REGISTER_TEXTS['choose_ctg'].get(user_language)}"
    user_cart = False
    
    user_tg_id = call.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    if userOrder:
        orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
        if orderItems:
            text = await get_cart_items_text(list(enumerate(orderItems, 1)), user_language=user_language)
            user_cart = True
            
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.answer(text, reply_markup=builders.get_categories_btn(categories, f"category_{0}", user_cart, lang=user_language), parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("category_"))
async def get_subcategories(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    category_id = int(call.data.split("_")[1])
    await call.message.delete()
    if category_id == 0:
        await call.message.answer(f"{BOT_WORDS['main_sentence'].get(user_language)} \n\n<a href='{BOT_WORDS['menu_link'].get(user_language)}'>Donar House Menu </a>", reply_markup=inline.main_btn(lang=user_language), parse_mode=ParseMode.HTML)
        return True
    
    sub_categories = await sync_to_async(list)(Category.objects.sub_ctg(id=category_id))
    category = await Category.objects.aget(id=category_id)
        
    photo = FSInputFile(category.image.path)  
    if sub_categories:
        if sub_categories[0].level == 1:
            await call.message.answer_photo(photo=photo, caption=f"{REGISTER_TEXTS['choose_ctg'].get(user_language)}", reply_markup=builders.get_categories_btn(sub_categories, f"categories", lang=user_language))
        else:
            await call.message.answer_photo(photo=photo, caption=f"{REGISTER_TEXTS['choose_ctg'].get(user_language)}", reply_markup=builders.get_categories_btn(sub_categories, f"category_{sub_categories[0].parent_id}", lang=user_language))
        return True
    
    products = await sync_to_async(list)(Product.objects.get_ctg_products(category_id=category_id))
    if products:
        if products[0].get("category__parent_id"):
            await call.message.answer_photo(photo=photo, caption=f"{REGISTER_TEXTS['choose_product'].get(user_language)}", reply_markup=builders.get_products_btn(products, f"category_{products[0].get('category__parent_id')}", lang=user_language))
        else:
            await call.message.answer_photo(photo=photo, caption=f"{REGISTER_TEXTS['choose_product'].get(user_language)}", reply_markup=builders.get_products_btn(products, f"categories", lang=user_language))
        return True
    
    await call.answer(f"{REGISTER_TEXTS['404_product'].get(user_language)}")
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.answer(f"{REGISTER_TEXTS['choose_ctg'].get(user_language)}", reply_markup=builders.get_categories_btn(categories, f"category_0", lang=user_language))


@router.callback_query(F.data.startswith("product_"))
async def get_product(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    product_id = int(call.data.split("_")[1])
    await call.message.delete()
    product = await sync_to_async(Product.objects.get)(id=product_id)
    caption = f"{REGISTER_TEXTS['name'].get(user_language)}: <b>{product.name}</b> \n"
    caption += f"{REGISTER_TEXTS['description'].get(user_language)}: {product.description}\n"
    caption += f"{REGISTER_TEXTS['price'].get(user_language)}: {product.price} UZS"
    if product.image:
        try:
            photo = FSInputFile(product.image.path)  
            await call.message.answer_photo(photo=photo, caption=caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id, user_language))
        except Exception as error:
            await call.message.answer(text=caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id, user_language))
    else:
        await call.message.answer(caption, reply_markup=fabrics.value_compressor(1, product.id, product.category_id, user_language))
        

@router.callback_query(fabrics.ProductValue.filter(F.action.in_(['addcart'])))
async def add_cart(call: types.CallbackQuery, callback_data: fabrics.ProductValue, user_language: str = 'uz'):
    await call.answer()
    quantity = int(callback_data.count)
    product_id = int(callback_data.product_id)
    # action = callback_data.action
    
    user = await sync_to_async(User.objects.get)(telegram_id=call.from_user.id)
    userOrder, created = await sync_to_async(Order.objects.get_or_create)(user=user, status="active")
    await userOrder.asave()
    
    product = await sync_to_async(Product.objects.get)(id=product_id)
    orderItem, created = await sync_to_async(OrderItem.objects.get_or_create)(order=userOrder, product=product, defaults={"quantity": quantity})
    orderItem.quantity = quantity
    await orderItem.asave()
    
    # await call.message.answer(f"'{product.name}' dan {quantity} tasi  savatga qo'shildi")
    await call.message.answer(f"{REGISTER_TEXTS['added_cart'].get(user_language)}".format(product=product.name, quantity=quantity))
    await categories(call, state=FSMContext)


@router.callback_query(F.data == "mycart")
async def my_cart(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    user_tg_id = call.from_user.id
    
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await call.message.edit_text(f"{REGISTER_TEXTS['empty'].get(user_language)}", reply_markup=inline.cart_btn(empty=True, lang=user_language))
        return True
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
    
    if not orderItems:
        await call.message.edit_text(f"{REGISTER_TEXTS['empty'].get(user_language)}", reply_markup=inline.cart_btn(empty=True, lang=user_language))
        return True
    
    if userOrder.is_all_order_info_filled:
        order = userOrder 
    else:
        order = None
        
    text = await get_cart_items_text(list(enumerate(orderItems, 1)), order, user_language)
        
    # total_price = 0
    # text = "Sizning savatingizda quidagilar mavjud: \n\n"
    # for index, item in enumerate(orderItems, 1):
    #     text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> dan\n """
    #     text += f"""  >  {int(item.get("product__price"))} x {item.get("quantity")} ta => {item.get("total_price")} UZS\n\n"""
    #     total_price += item.get("total_price")
        
    # text += f"<b>Jami: {total_price} UZS </b>"
    not_fill_field = True
    if userOrder.is_all_order_info_filled:
        not_fill_field = False
    
    await call.message.edit_text(text, reply_markup=inline.cart_btn(empty=False, lang=user_language, order_id=userOrder.id, not_fill_field=not_fill_field), parse_mode=ParseMode.HTML)
        


@router.callback_query(F.data.startswith("changeproducts_"))
async def change_products(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    user_tg_id = call.from_user.id
    cart_id = int(call.data.split("_")[1])
    userOrder = await sync_to_async(Order.objects.get)(id=cart_id)
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=cart_id))
    
    if not orderItems:
        await call.message.edit_text(f"{REGISTER_TEXTS['empty'].get(user_language)}", reply_markup=inline.cart_btn(empty=True, lang=user_language))
        return True
    
    # orderItems = list(enumerate(orderItems, 1))
    # if userOrder.is_all_order_info_filled:
    #     order = userOrder 
    # else:
    #     order = None
        
    text = await get_cart_items_text(list(enumerate(orderItems, 1)), user_language=user_language)
    
    await call.message.edit_text(text, reply_markup=fabrics.change_values(list(enumerate(orderItems, 1)), cart_id, lang=user_language), parse_mode=ParseMode.HTML)
    
    
@router.callback_query(F.data == "clearOrder")
async def clear_order(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    user_tg_id = call.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    await sync_to_async(userOrder.delete)()
    
    await call.message.edit_text(f"{REGISTER_TEXTS['empty'].get(user_language)}", reply_markup=inline.cart_btn(empty=True, lang=user_language))


@router.callback_query(F.data.startswith("createToOrder_"))
async def create_to_order(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    await state.clear()
    orderId = int(call.data.split("_")[1])
    user_tg_id = call.from_user.id
    order = await sync_to_async(Order.objects.get)(id=orderId)
    if order.is_all_order_info_filled:
        await payment_to_order(call, order)
        # TODO: Order is already created, go to payment
        return True  
    
    await call.message.edit_text(f"{REGISTER_TEXTS['choose_delivery_type'].get(user_language)}", reply_markup=inline.delivery_type_btn(user_language))
    await state.update_data(orderId= orderId)
    await state.set_state(CreateOrderState.delivery_type)
    

@router.callback_query(StateFilter(CreateOrderState.delivery_type, F.data in ['DeliveryPickUp', 'DeliveryByCourier']))
async def get_delivery_type(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    delivery_type = call.data
    await state.update_data(delivery_type= delivery_type)
    await call.message.delete()
    
    if delivery_type == 'DeliveryPickUp':
        branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
        await call.message.answer(f"{REGISTER_TEXTS['choose_delivery_type'].get(user_language)}", reply_markup=builders.get_brancches_btn(branches, lang=user_language))
        await state.set_state(CreateOrderState.branch)
        return True
    
    await call.message.answer(f"{REGISTER_TEXTS['send_location'].get(user_language)}", reply_markup=reply.get_address_btn(user_language))
    await state.set_state(CreateOrderState.location)
    
    
@router.message(StateFilter(CreateOrderState.location), F.location)
async def get_location_func(message: types.Message, state: FSMContext, user_language: str = 'uz'):
    location = message.location
    location_url = f"https://maps.google.de/maps?q={location.latitude},{location.longitude}&z=17&t=m"
    try:
        address = await get_address(location.latitude, location.longitude)
    except Exception as error:
        await message.answer(f"{REGISTER_TEXTS['location_error'].get(user_language)} {error}", reply_markup=reply.get_address_btn(user_language))
        await state.set_state(CreateOrderState.location)
        return True
    
    await state.update_data(
        location=location_url,
        address=address,
        latitude=location.latitude,
        longitude=location.longitude
    )
    
    await message.answer(f"{REGISTER_TEXTS['confirm_location'].get(user_language)}".format(address=address), reply_markup=reply.address_confirmation(user_language))
    await state.set_state(CreateOrderState.address)


@router.message(StateFilter(CreateOrderState.location), ~F.location)
async def get_not_location_func(message: types.Message, state: FSMContext, user_language: str = 'uz'):
    await message.answer(f"{REGISTER_TEXTS['send_location'].get(user_language)}", reply_markup=reply.get_address_btn(user_language))
    await state.set_state(CreateOrderState.location)
    

@router.message(StateFilter(CreateOrderState.address), F.text )
async def address_confirm_func(message: types.Message, state: FSMContext, user_language: str = 'uz'):
    
    if message.text in (BUTTON_TEXTS["correct"]['ru'], BUTTON_TEXTS["correct"]['uz']):
        await message.answer(f"{REGISTER_TEXTS['addedtional_input'].get(user_language)}", reply_markup=reply.back_btn(user_language))
        await state.set_state(CreateOrderState.addention)
        return True
    
    if message.text in (BUTTON_TEXTS["incorrect"]['ru'], BUTTON_TEXTS["incorrect"]['uz']):
        await get_not_location_func(message, state)
        return True  
    
    await message.answer(f"{REGISTER_TEXTS['address_confirmation'].get(user_language)}", reply_markup=reply.address_confirmation(user_language))
    await state.set_state(CreateOrderState.address)


@router.message(StateFilter(CreateOrderState.addention), F.text)
async def address_addention_func(message: types.Message, state: FSMContext, user_language: str = 'uz'):
    addention = message.text
    await state.update_data(addention= addention)
    await state.set_state(CreateOrderState.phone)
    await message.answer(f"{REGISTER_TEXTS['send_phone'].get(user_language)}", reply_markup=reply.phone_btn(user_language))
    
    
@router.callback_query(StateFilter(CreateOrderState.branch), F.data.startswith('branch_'))
async def get_order_branch(call: types.CallbackQuery, state=FSMContext, user_language: str = 'uz'):
    await call.message.delete()
    branch_id = call.data.split('_')[-1]
    if str(branch_id) == '0':
        await state.clear()
        await my_cart(call, state)
        return True
    
    await state.update_data(branch=branch_id)
    await state.set_state(CreateOrderState.phone)
    await call.message.answer(f"{REGISTER_TEXTS['send_phone'].get(user_language)}", reply_markup=reply.phone_btn(user_language))
    

@router.message(StateFilter(CreateOrderState.phone), F.contact)
async def set_phone(message: types.Message, state: FSMContext, user_language: str = 'uz'):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    
    await state.set_state(CreateOrderState.full_name)
    await message.answer(f"{REGISTER_TEXTS['enter_name'].get(user_language)}", reply_markup=reply.rmk)
    
    
@router.message(StateFilter(CreateOrderState.phone), ~F.contact)
async def not_phone(message: types.Message, state=FSMContext, user_language: str = 'uz'):
    phone_text = message.text
    # if len
    await message.answer(f"{REGISTER_TEXTS['send_phone'].get(user_language)}", reply_markup=reply.phone_btn(user_language))
    

@router.message(StateFilter(CreateOrderState.full_name), F.text)
async def get_full_name(message: types.Message, state=FSMContext, user_language: str = 'uz'):
    full_name = message.text
    await state.update_data(full_name=full_name)
    data = await state.get_data()
    
    # print(data)
    text = f"{REGISTER_TEXTS['confirm_order'].get(user_language)}\n\n"
    if data.get('delivery_type') == 'DeliveryPickUp':
        branch = await sync_to_async(Branch.objects.get)(id=data.get('branch'))
        text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>{BOT_WORDS['pickup'].get(user_language)}</b>\n"
        text += f"{BOT_WORDS['branch'].get(user_language)}: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
        text += f"{BOT_WORDS['order_user'].get(user_language)}: <b>{full_name}</b>\n"
        text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{data.get('phone')}</b>\n"
    else:
        text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>Yetkazib berish</b>\n"
        text += f"{BOT_WORDS['order_user_input'].get(user_language)}: <b>{full_name}</b>\n"
        text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{data.get('phone')}</b>\n"
        text += f"{BOT_WORDS['order_address'].get(user_language)}: <b>{data.get('address')}</b>\n"
        text += f"{BOT_WORDS['order_addention'].get(user_language)}: <b>{data.get('addention')}</b>\n"
    
    await message.answer(text, reply_markup=reply.address_confirmation(user_language))
    await state.set_state(CreateOrderState.confirm)
    
    
@router.message(StateFilter(CreateOrderState.confirm))
async def confirm_data_func(message: types.Message, state=FSMContext, user_language: str = 'uz'):
    data = await state.get_data()
    await state.clear()
    
    if message.text in (BUTTON_TEXTS["correct"]['ru'], BUTTON_TEXTS["correct"]['uz']):
        # user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
        # print(data)
        orderId = data.get("orderId")
        if data.get('branch'):
            branch = await sync_to_async(Branch.objects.get)(id=data.get('branch'))
        else:
            branch = None
        # print(branch)
        order = await sync_to_async(Order.objects.get)(id=orderId)
        order.branch = branch
        order.delivery = data.get("delivery_type")
        order.address = data.get("address")
        order.location = data.get("location")
        order.longitude = data.get("longitude")
        order.latitude = data.get("latitude")
        order.full_name = data.get("full_name")
        order.phone = data.get("phone")
        order.addention = data.get("addention")
        order.is_all_order_info_filled = True
        await order.asave()
        
        orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=order.id))
        order_info = await get_cart_items_text(list(enumerate(orderItems, 1)), order, user_language)
        await message.answer(order_info, reply_markup=reply.rmk)
        
        await message.answer(f"{BOT_WORDS['choose_payment_type'].get(user_language)}", reply_markup=inline.payment_type(order.id, user_language))
        
    else:
        
        await message.answer(f"{BOT_WORDS['payment_will_be_cancel'].get(user_language)}", reply_markup=reply.rmk)    
        await my_cart_message(message, state)
        return True
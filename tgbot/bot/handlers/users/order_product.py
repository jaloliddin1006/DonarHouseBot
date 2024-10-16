from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from tgbot.bot.handlers.users.payment import create_invoice, payment_to_order
from tgbot.bot.loader import bot, STICERS
from tgbot.bot.handlers.users.main import my_cart_message
from tgbot.bot.keyboards import reply, inline, builders, fabrics
from tgbot.bot.states.main import CreateOrderState
from tgbot.utils import get_address
from tgbot.models import Branch, User, Category, Product, Order, OrderItem
from PIL import Image
from io import BytesIO


router = Router()    

async def get_cart_items_text(orderItems: list, order: Order = None):
    total_price = 0
    text = "Sizning savatingizda quidagilar mavjud: \n\n"
    for index, item in orderItems:
        text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> dan\n """
        text += f"""  >  {item.get("quantity")} ta  x  {int(item.get("product__price"))} so'm => {item.get("total_price")} so'm\n\n"""
        total_price += item.get("total_price")
        
    text += f"<b>Jami: {total_price} so'm </b>\n\n"
    
    if order:
        text += "Buyurtma ma'lumotlari:\n\n"
        if order.delivery == 'pickup':
            branch = await sync_to_async(Branch.objects.get)(id=order.branch_id)
            
            text += f"Buyurtma turi: <b>Olib ketish</b>\n"
            text += f"Filial: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
            text += f"Olib ketuvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
        else:
            text += f"Buyurtma turi: <b>Yetkazib berish</b>\n"
            text += f"Qabul qiluvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
            text += f"Manzil: <b>{order.address}</b>\n"
            text += f"Qo'shimcha: <b>{order.addention}</b>\n"
        text += "Buyurtma holati: <b>To'lov kutilmoqda</b>"
    
    return text


@router.callback_query(F.data == "categories") 
async def categories(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    text = "Kategoriyalardan birini tanlang"
    user_cart = False
    
    user_tg_id = call.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    if userOrder:
        orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
        if orderItems:
            text = await get_cart_items_text(enumerate(orderItems, 1))
            user_cart = True
            
    categories = await sync_to_async(list)(Category.objects.get_parent_categories(lvl=0))
    await call.message.answer(text, reply_markup=builders.get_categories_btn(categories, f"category_{0}", user_cart), parse_mode=ParseMode.HTML)

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
    await call.message.answer("Kategoriyalardan birini tanlang", reply_markup=builders.get_categories_btn(categories, f"category_0"))


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
    orderItem.quantity = quantity
    await orderItem.asave()
    
    await call.message.answer(f"'{product.name}' dan {quantity} tasi  savatga qo'shildi")
    await categories(call, state=FSMContext)


@router.callback_query(F.data == "mycart")
async def my_cart(call: types.CallbackQuery, state=FSMContext):
    user_tg_id = call.from_user.id
    
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    if not userOrder:
        await call.message.edit_text("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
    
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=userOrder.id))
    
    if not orderItems:
        await call.message.edit_text("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
    
    if userOrder.is_all_order_info_filled:
        order = userOrder 
    else:
        order = None
        
    text = await get_cart_items_text(enumerate(orderItems, 1), order)
        
    # total_price = 0
    # text = "Sizning savatingizda quidagilar mavjud: \n\n"
    # for index, item in enumerate(orderItems, 1):
    #     text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> dan\n """
    #     text += f"""  >  {int(item.get("product__price"))} x {item.get("quantity")} ta => {item.get("total_price")} so'm\n\n"""
    #     total_price += item.get("total_price")
        
    # text += f"<b>Jami: {total_price} so'm </b>"
    not_fill_field = True
    if userOrder.is_all_order_info_filled:
        not_fill_field = False
    
    await call.message.edit_text(text, reply_markup=inline.cart_btn(empty=False, order_id=userOrder.id, not_fill_field=not_fill_field), parse_mode=ParseMode.HTML)
        


@router.callback_query(F.data.startswith("changeproducts_"))
async def change_products(call: types.CallbackQuery, state=FSMContext):
    user_tg_id = call.from_user.id
    cart_id = int(call.data.split("_")[1])
    userOrder = await sync_to_async(Order.objects.get)(id=cart_id)
    orderItems = await sync_to_async(list)(OrderItem.objects.items(cart_id=cart_id))
    
    if not orderItems:
        await call.message.edit_text("Savat bo'sh", reply_markup=inline.cart_btn(empty=True))
        return True
    
    orderItems = list(enumerate(orderItems, 1))
    if userOrder.is_all_order_info_filled:
        order = userOrder 
    else:
        order = None
        
    text = await get_cart_items_text(orderItems)
    
    await call.message.edit_text(text, reply_markup=fabrics.change_values(orderItems, cart_id), parse_mode=ParseMode.HTML)
    
    
@router.callback_query(F.data == "clearOrder")
async def clear_order(call: types.CallbackQuery, state=FSMContext):
    user_tg_id = call.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=user_tg_id)
    userOrder = await sync_to_async(lambda: Order.objects.filter(user=user, is_active=True, status='active').last())()
    
    await sync_to_async(userOrder.delete)()
    
    await call.message.edit_text("Savat bo'shatildi", reply_markup=inline.cart_btn(empty=True))


@router.callback_query(F.data.startswith("createToOrder_"))
async def create_to_order(call: types.CallbackQuery, state=FSMContext):
    await state.clear()
    orderId = int(call.data.split("_")[1])
    user_tg_id = call.from_user.id
    order = await sync_to_async(Order.objects.get)(id=orderId)
    if order.is_all_order_info_filled:
        await payment_to_order(call, order)
        # TODO: Order is already created, go to payment
        return True  
    
    await call.message.edit_text("Buyurtmani qanday holatda olishni istaysiz?", reply_markup=inline.delivery_type_btn)
    await state.update_data(orderId= orderId)
    await state.set_state(CreateOrderState.delivery_type)
    

@router.callback_query(StateFilter(CreateOrderState.delivery_type, F.data in ['pickup', 'delivery']))
async def get_delivery_type(call: types.CallbackQuery, state=FSMContext):
    delivery_type = call.data
    await state.update_data(delivery_type= delivery_type)
    await call.message.delete()
    
    if delivery_type == 'pickup':
        branches = await sync_to_async(list)(Branch.objects.filter(is_active=True))
        await call.message.answer("O'zingizga qulay filialni tanlang. ", reply_markup=builders.get_brancches_btn(branches))
        await state.set_state(CreateOrderState.branch)
        return True
    
    await call.message.answer("<b>Eltib berish</b> uchun <b>geo-joylashuvni</b> jo'nating:", reply_markup=reply.get_address_btn)
    await state.set_state(CreateOrderState.location)
    
    
@router.message(StateFilter(CreateOrderState.location), F.location)
async def get_location_func(message: types.Message, state: FSMContext):
    location = message.location
    location_url = f"https://maps.google.de/maps?q={location.latitude},{location.longitude}&z=17&t=m"
    address = await get_address(location.latitude, location.longitude)
    await state.update_data(
        location= location_url,
        address= address
    )
    
    await message.answer(f"Buyurtma qilmoqchi bo'lgan manzilingiz\n<b>{address}</b>\n\n Ushbu manzilni tasdiqlaysizmi?", reply_markup=reply.address_confirmation)
    await state.set_state(CreateOrderState.address)


@router.message(StateFilter(CreateOrderState.location), ~F.location)
async def get_not_location_func(message: types.Message, state: FSMContext):
    await message.answer("<b>Eltib berish</b> uchun <b>geo-joylashuvni</b> jo'nating:", reply_markup=reply.get_address_btn)
    await state.set_state(CreateOrderState.location)
    

@router.message(StateFilter(CreateOrderState.address), F.text )
async def address_confirm_func(message: types.Message, state: FSMContext):
    
    if message.text == "✅ To'g'ri":
        await message.answer("Manzil bo'yicha qo'shimcha ma'lumotingizni kiriting.\nMisol uchun: Podyezd №, qavat №, eshik kodi №, kv №..", reply_markup=reply.back_btn)
        await state.set_state(CreateOrderState.addention)
        return True
    
    if message.text == "❌ Noto'g'ri":
        await get_not_location_func(message, state)
        return True  
    
    await message.answer(f"Yuqoridagi manzilning to'g'riligini tasdiqlang?", reply_markup=reply.address_confirmation)
    await state.set_state(CreateOrderState.address)


@router.message(StateFilter(CreateOrderState.addention), F.text)
async def address_addention_func(message: types.Message, state: FSMContext):
    addention = message.text
    await state.update_data(addention= addention)
    await state.set_state(CreateOrderState.phone)
    await message.answer("Telefon raqamingizni yuboring", reply_markup=reply.phone_btn)
    
    
@router.callback_query(StateFilter(CreateOrderState.branch), F.data.startswith('branch_'))
async def get_order_branch(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    branch_id = call.data.split('_')[-1]
    if str(branch_id) == '0':
        await state.clear()
        await my_cart(call, state)
        return True
    
    await state.update_data(branch=branch_id)
    await state.set_state(CreateOrderState.phone)
    await call.message.answer("Telefon raqamingizni yuboring", reply_markup=reply.phone_btn)
    

@router.message(StateFilter(CreateOrderState.phone), F.contact)
async def set_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    
    await state.set_state(CreateOrderState.full_name)
    await message.answer("Ismingizni kiriting", reply_markup=reply.rmk)
    
    
@router.message(StateFilter(CreateOrderState.phone), ~F.contact)
async def not_phone(message: types.Message, state=FSMContext):
    phone_text = message.text
    # if len
    await message.answer("Telefon raqamingizni yuboring", reply_markup=reply.phone_btn)
    

@router.message(StateFilter(CreateOrderState.full_name), F.text)
async def get_full_name(message: types.Message, state=FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    data = await state.get_data()
    
    # print(data)
    text = f"Buyurtma ma'lumotlari to'g'riligini tasdiqlang\n\n"
    if data.get('delivery_type') == 'pickup':
        branch = await sync_to_async(Branch.objects.get)(id=data.get('branch'))
        text += f"Buyurtma turi: <b>Olib ketish</b>\n"
        text += f"Filial: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
        text += f"Olib ketuvchi: <b>{full_name}</b>\n"
        text += f"Telefon raqam: <b>{data.get('phone')}</b>\n"
    else:
        text += f"Buyurtma turi: <b>Yetkazib berish</b>\n"
        text += f"Qabul qiluvchi: <b>{full_name}</b>\n"
        text += f"Telefon raqam: <b>{data.get('phone')}</b>\n"
        text += f"Manzil: <b>{data.get('address')}</b>\n"
        text += f"Qo'shimcha: <b>{data.get('addention')}</b>\n"
    
    await message.answer(text, reply_markup=reply.address_confirmation)
    await state.set_state(CreateOrderState.confirm)
    
    
@router.message(StateFilter(CreateOrderState.confirm))
async def confirm_data_func(message: types.Message, state=FSMContext):
    data = await state.get_data()
    await state.clear()
    
    if message.text == "✅ To'g'ri":
        user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
        print(data)
        orderId = data.get("orderId")
        if data.get('branch'):
            branch = await sync_to_async(Branch.objects.get)(id=data.get('branch'))
        else:
            branch = None
        print(branch)
        order = await sync_to_async(Order.objects.get)(id=orderId)
        order.branch = branch
        order.delivery = data.get("delivery_type")
        order.address = data.get("address")
        order.location = data.get("location")
        order.full_name = data.get("full_name")
        order.phone = data.get("phone")
        order.addention = data.get("addention")
        order.is_all_order_info_filled = True
        await order.asave()
        
        
        text = f"Buyurtma ma'lumotlari saqlandi. To'lovni amalga oshirishingiz bilan buyurtma faollashadi.\n\n"
        if order.delivery == 'pickup':
            text += f"Buyurtma turi: <b>Olib ketish</b>\n"
            text += f"Filial: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
            text += f"Olib ketuvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
        else:
            text += f"Buyurtma turi: <b>Yetkazib berish</b>\n"
            text += f"Qabul qiluvchi: <b>{order.full_name}</b>\n"
            text += f"Telefon raqam: <b>{order.phone}</b>\n"
            text += f"Manzil: <b>{order.address}</b>\n"
            text += f"Qo'shimcha: <b>{order.addention}</b>\n\n"
        text += "Buyurtma holati: <b>To'lov kutilmoqda</b>"
        await message.answer(text, reply_markup=reply.rmk)
        invoice = await create_invoice(order, user.isQrCode)
        await message.answer_invoice(**invoice.generate_invoice(), name='alibobo', payload=f"{order.id}")
    else:
        
        await message.answer("Buyurtma ma'lumotlari bekor qilindi.", reply_markup=reply.rmk)    
        await my_cart_message(message, state)
        return True
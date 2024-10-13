from django.conf import settings
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.filters.state import StateFilter
from asgiref.sync import sync_to_async
from tgbot.utils import get_address
from tgbot.bot.keyboards import reply, inline
from tgbot.models import User
from tgbot.bot.loader import bot
from tgbot.bot.utils.extra_datas import make_title
from tgbot.bot.states.main import RegistrationState


router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message, state: FSMContext):
    await state.clear()
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Assalomu alaykum {full_name}! ", parse_mode=ParseMode.MARKDOWN)
    user, created = await User.objects.aget_or_create(
        telegram_id=telegram_id,
        full_name=full_name,
        username=message.from_user.username
    )
    if created:
        count = await User.objects.acount()
        msg = (f"[{make_title(user.full_name)}](tg://user?id={user.telegram_id}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
        if not user.is_active:
            await sync_to_async(User.objects.filter(telegram_id=telegram_id).update)(is_active=True)
            
    for admin in settings.ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
            
    if created:
        await state.set_state(RegistrationState.language)
        await message.answer("Muloqot tilini tanlang", reply_markup=inline.language_btn)
    else:
        await message.answer("Biz bilan birga buyurtma qilishga tayyormisiz? ", reply_markup=inline.main_btn)
        


@router.callback_query(StateFilter(RegistrationState.language))
async def set_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    await state.update_data(language_code=language)
    await call.message.delete()
    await state.set_state(RegistrationState.location)
    await call.message.answer("Lokatsiyangizni yuboring", reply_markup=reply.location_btn)
    await call.answer()


@router.message(StateFilter(RegistrationState.location), F.location)
async def set_location(message: types.Message, state: FSMContext):
    location = message.location
    location_url = f"https://maps.google.de/maps?q={location.latitude},{location.longitude}&z=17&t=m"
    address = await get_address(location.latitude, location.longitude)
    await state.update_data({
        "location": location_url,
        "address": address
    })
    await state.set_state(RegistrationState.phone)
    await message.answer("Telefon raqamingizni yuboring", reply_markup=reply.phone_btn)
    
    
@router.message(StateFilter(RegistrationState.location), ~F.location)
async def not_location(message: types.Message):
    await message.answer("Lokatsiyangizni yuboring", reply_markup=reply.location_btn)


@router.message(StateFilter(RegistrationState.phone), F.contact)
async def set_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()
    # user = await User.objects.aget(telegram_id=message.from_user.id)
    await sync_to_async(User.objects.filter(telegram_id=message.from_user.id).update)(
        phone=data.get("phone"),
        address=data.get("address"),
        location=data.get("location"),
        language_code=data.get("language_code")
    )
    await state.clear()
    await message.answer("Marhamat botdan foydalanib buyurtma berishingiz mumkin.", reply_markup=reply.rmk)
    await message.answer("Biz bilan birga buyurtma qilishga tayyormisiz? ", reply_markup=inline.main_btn)
    
    
@router.message(StateFilter(RegistrationState.phone), ~F.contact)
async def not_phone(message: types.Message):
    await message.answer("Telefon raqamingizni yuboring", reply_markup=reply.phone_btn)
    
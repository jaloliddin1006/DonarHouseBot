import asyncio
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.session.middlewares.request_logging import logger
from asgiref.sync import sync_to_async

from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply
from tgbot.models import User
from tgbot.bot.states.main import MessageState


router = Router()


@router.message(F.text == '/users')
async def feedback_func(message: types.Message, state: FSMContext):
    all_users = await User.objects.acount()
    text = "Hurmatli admin!\n\n"
    text += f"Bot foydalanuvchilari soni: {all_users}"

    await message.reply(text)
    await message.answer("Adminning boshqa funksiyalari tez orada qo'shiladi :)")





@router.message(F.text=='/message')
async def message_format_func(message: types.Message, state=FSMContext):
    await state.set_state(MessageState.message)
    await state.update_data(format='HTML')
    
    await message.answer("Foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:", reply_markup=reply.rmk)


@router.message(MessageState.message, F.text)
async def message_format_func(message: types.Message, state=FSMContext):
    msg = message.text
    await message.answer("Xabar yuborildi!", reply_markup=reply.main)
    await state.clear()


@router.message(MessageState.message, ~F.text)
async def message_format_func(message: types.Message, state=FSMContext):
    await message.answer("Hozirda faqat matnli xabar yubora olasiz!!!", reply_markup=reply.main)
    await state.clear()


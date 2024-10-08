from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from tgbot.bot.keyboards import reply
from tgbot.models import User
from tgbot.bot.loader import bot
from django.conf import settings
from tgbot.bot.utils.extra_datas import make_title
from asgiref.sync import sync_to_async

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
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

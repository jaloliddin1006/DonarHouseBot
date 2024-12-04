from aiogram import BaseMiddleware
from aiogram.types import Message
from asgiref.sync import sync_to_async
from tgbot.models import User
from django.utils.translation import activate


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        telegram_id = event.from_user.id
        
        user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()
        
        if user and user.language_code:
            data['user_language'] = user.language_code
        else:
            data['user_language'] = 'uz'
        activate(data['user_language'])
        
        return await handler(event, data)

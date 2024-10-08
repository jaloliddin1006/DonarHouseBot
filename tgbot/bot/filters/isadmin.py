from aiogram.types import Message
from typing import List
from aiogram.filters import BaseFilter
from tgbot.utils import get_admins

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        ADMINS = await get_admins()
        return str(message.from_user.id) in ADMINS or message.from_user.id in ADMINS
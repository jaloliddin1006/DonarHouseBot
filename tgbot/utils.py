from django.conf import settings
from tgbot.models import BotAdmin
from asgiref.sync import sync_to_async


async def get_admins():
    ADMINS = []
    ADMINS += settings.ADMINS

    BOT_ADMINS = await sync_to_async(
        lambda: list(BotAdmin.objects.filter(is_active=True).values_list('user__telegram_id', flat=True)),
        thread_sensitive=True
    )()
    ADMINS += BOT_ADMINS

    return ADMINS

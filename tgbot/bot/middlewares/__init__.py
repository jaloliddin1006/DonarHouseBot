from aiogram import Dispatcher

from tgbot.bot.loader import dp
from .throttling import ThrottlingMiddleware
from .language import LanguageMiddleware


if __name__ == "middlewares":
    
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LanguageMiddleware())

from src.settings import API_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode


bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

STICERS = [0, "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

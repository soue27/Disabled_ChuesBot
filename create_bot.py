from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from Config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

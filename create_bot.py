from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os



Token = os.getenv('BOT_TOKEN')
bot = Bot(token=Token)
dp = Dispatcher(bot, storage)


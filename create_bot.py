import asyncio
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import dotenv_values
from data.bd import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage


config = dotenv_values(".env", encoding="utf-8")

ADMIN_ID = config['ADMIN_ID']
BOT_ID = config['BOT_ID']
STORAGE = MemoryStorage()
db = DataBase('data/database.db')
bot = Bot(token=BOT_ID, parse_mode='HTML')
dp = Dispatcher(bot, storage=STORAGE)

class BotFSM(StatesGroup):
    min_price = State()

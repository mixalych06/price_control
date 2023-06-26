import asyncio
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from data.bd import DataBase


config = dotenv_values(".env", encoding="utf-8")

ADMIN_ID = config['ADMIN_ID']
BOT_ID = config['BOT_ID']
db = DataBase('data/database.db')
bot = Bot(token=BOT_ID, parse_mode='HTML')
dp = Dispatcher(bot)

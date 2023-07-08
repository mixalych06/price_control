from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from data.bd import DataBase


config = dotenv_values(".env", encoding="utf-8")

dbname = config['db_name']
host = config['HOST']
user = config['USER']
password = config['PASSWORD']
ADMIN_ID = config['ADMIN_ID']
BOT_ID = config['BOT_ID']

db = DataBase(dbname, host, user, password)
bot = Bot(token=BOT_ID, parse_mode='HTML')
dp = Dispatcher(bot)



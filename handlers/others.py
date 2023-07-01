from aiogram import types, Dispatcher
from create_bot import bot, ADMIN_ID
from utils.filters import checks_exists_no_user
from utils.parsr import pars
from keyboards.kb_admin import keyboard_admin_main
from keyboards.kb_all import gen_markup_sellers, gen_seller_markup_, gen__markup_pagination
from create_bot import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_all(message: types.Message):
    '''срабатывает на любое сообщение от пользователей не в базе'''
    await message.delete()
    await message.answer(f'<b>Привет, {message.from_user.first_name}</b>\nБот работает только с зарегистрированными пользователями.\n'
                        'Для начала работы пришлите команду предоставленную администратором!')

async def requests_to_add_user(message: types.Message):
    '''запрос на регистрацию. доделать проверку существования суперюзера в базе'''
    su_admin = message.text.split(':')[1]
    su_admins = db.bd_get_su_admins()

    await bot.send_message(chat_id=su_admin, text=f'<b>Запрос на добавление нового пользователя.</b>\n'
                                                    f'<b>ID:</b>{message.from_user.id}:\n'
                                                    f'<b>Имя:</b>{message.from_user.first_name}',
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton(text=f'Администратор', callback_data='add_user:admin'),
                               InlineKeyboardButton(text=f'Пользователь', callback_data='add_user:user')))

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(requests_to_add_user, checks_exists_no_user, text = ['requests_to_add_user:1272037006'])
    dp.register_message_handler(start_all, checks_exists_no_user)


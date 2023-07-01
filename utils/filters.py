from create_bot import db, ADMIN_ID
from aiogram import types



async def checks_exists_no_user(message: types.Message):
    '''Пользователя нет в базу - True'''
    users = db.bd_get_all_users()
    print(message.from_user.id not in users)
    return message.from_user.id not in users

async def checks_exists_admin(message: types.Message):
    '''Пользователь в базе с правами админа - True'''
    admin = db.bd_get_su_admins()
    return message.from_user.id in admin or message.from_user.id in [int(ADMIN_ID)]

async def checks_exists_user(message: types.Message):
    '''Пользователь в базе с правами юзера - True'''
    users = db.bd_get_users()
    return message.from_user.id in users
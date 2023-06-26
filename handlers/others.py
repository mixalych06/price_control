
from aiogram import types, Dispatcher

async def start(message: types.Message):
    await message.reply('Привет')

async def message_all(message: types.Message):
    await message.reply(message.from_user.id)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(message_all)
from create_bot import db, bot
from keyboards.kb_users import keyboard_user_main
from utils.filters import checks_exists_user
from aiogram import types, Dispatcher


async def start_user(message: types.Message):
    await message.answer(text=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                              f'Твой ID: {message.from_user.id}\n'
                              f'<b>Ты можешь:</b>\n✅просматривать отслеживаемые магазины и товары\n'
                              f'✅получать уведомления о снижении цены ниже установленной.',
                         reply_markup=keyboard_user_main)
    await message.delete()


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start_user, checks_exists_user)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_admin_main: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
but_shop: KeyboardButton = KeyboardButton('Магазины и товары')
but_editing_admin: KeyboardButton = KeyboardButton('Администраторы')
but_editing_users: KeyboardButton = KeyboardButton('Пользователи')
but_help_admin: KeyboardButton = KeyboardButton('Помощь')
keyboard_admin_main.add(but_shop).add(but_editing_admin, but_editing_users).add(but_help_admin)








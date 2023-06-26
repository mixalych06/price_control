from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_admin_main: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
but_shop: KeyboardButton = KeyboardButton('Магазины и товары')
but_editing_admin: KeyboardButton = KeyboardButton('Администраторы')
but_editing_users: KeyboardButton = KeyboardButton('Пользователи')
but_help_admin: KeyboardButton = KeyboardButton('Помощь')
keyboard_admin_main.add(but_shop).add(but_editing_admin, but_editing_users).add(but_help_admin)


keyboard_order_admin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




but_category: KeyboardButton = KeyboardButton('Добавить категорию')
but_admin_orders: KeyboardButton = KeyboardButton('Заказы')



but_not_ready: KeyboardButton = KeyboardButton('На сборке')
but_ready: KeyboardButton = KeyboardButton('К выдаче')
but_paid_for: KeyboardButton = KeyboardButton('Оплаченые')
but_main_menu: KeyboardButton = KeyboardButton('Назад')
keyboard_order_admin.add(but_not_ready).add(but_ready).add(but_paid_for).add(but_main_menu)
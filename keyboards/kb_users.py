from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
keyboard_user_main: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
but_shop_user: KeyboardButton = KeyboardButton('Магазины и товары')
but_help_user: KeyboardButton = KeyboardButton('Помощь')
keyboard_user_main.add(but_shop_user).add(but_help_user)

async def gen__markup_pagination_for_user(page_number, seller_id, trecked, products_len):
    """Создаёт инлайн клавиатуру пагинации товаров
    page_number-порядковый номер товара, seller_id, trecked-1 отслеживается 0 нет, products_len - количество товаров в базе"""
    markup_pagination = InlineKeyboardMarkup(row_width=3)
    if products_len == 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data='null'),
            InlineKeyboardButton(text=f'{page_number+1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'null'))

    elif 0 < page_number < products_len - 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'u_track:{seller_id}:{trecked}:{page_number-1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'u_track:{seller_id}:{trecked}:{page_number+1}'))
    elif page_number == 0:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'u_track:{seller_id}:{trecked}:{products_len - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'u_track:{seller_id}:{trecked}:{page_number + 1}'))
    elif page_number == products_len - 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'u_track:{seller_id}:{trecked}:{page_number - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'u_track:{seller_id}:{trecked}:{0}'))

    return markup_pagination




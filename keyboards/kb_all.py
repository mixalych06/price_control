from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_markup_sellers(sellers: dict, inline):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, для показа магазинов"""
    markup_sellers = InlineKeyboardMarkup(row_width=1)
    x = []
    for key, value in sellers.items():
        x.append(InlineKeyboardButton(text=str(value), callback_data=f'{inline}:{key}:0'))
    markup_sellers.add(*x)

    return markup_sellers


async def gen_markup_del_sellers(sellers: dict, inline, id_message):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, для показа магазинов"""
    markup_sellers = InlineKeyboardMarkup(row_width=1)
    x = []
    for key, value in sellers.items():
        x.append(InlineKeyboardButton(text=str(value), callback_data=f'{inline}:{key}:{id_message}'))
    markup_sellers.add(*x)

    return markup_sellers


async def gen__markup_pagination(seller_id, products_len, page_number=0):
    """Создаёт инлайн клавиатуру пагинации товаров
    page_number-порядковый номер товара, seller_id, trecked-1 отслеживается 0 нет, products_len - количество товаров в базе"""
    markup_pagination = InlineKeyboardMarkup(row_width=3)

    if products_len == 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data='null'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'null'))
        return markup_pagination

    elif 0 < page_number < products_len - 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{page_number - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{page_number + 1}'))
        return markup_pagination
    elif page_number == 0:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{products_len - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{page_number + 1}'))
        return markup_pagination
    elif page_number == products_len - 1:
        markup_pagination.add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{page_number - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{0}'))

    return markup_pagination

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_markup_sellers(sellers: dict, inline):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, для показа магазинов"""
    markup_sellers = InlineKeyboardMarkup(row_width=1)
    x = []
    for key, value in sellers.items():
        x.append(InlineKeyboardButton(text=str(value), callback_data=f'{inline}:{key}'))
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

async def gen_seller_markup_(tracked_product, seller_id):
    """Создаёт инлайн клавиатуру для срабатывания хэндлера"""
    markup_seller = InlineKeyboardMarkup(row_width=1)
    markup_seller.add(InlineKeyboardButton(text=f'✅ Отслеживается\n({tracked_product[0]})', callback_data=f'track:{seller_id}:1:0'),
                      InlineKeyboardButton(text=f'❎ Не отслеживается\n({tracked_product[1]})', callback_data=f'track:{seller_id}:0:0'))

    return markup_seller

async def gen__markup_pagination(page_number, seller_id, trecked, products_len, prod_id):
    """Создаёт инлайн клавиатуру пагинации товаров
    page_number-порядковый номер товара, seller_id, trecked-1 отслеживается 0 нет, products_len - количество товаров в базе"""
    markup_pagination = InlineKeyboardMarkup(row_width=3)
    text_btn = {1: ('🔕Не отслеживать', 'noTr'), 0: ('Отслеживать', 'startTr')}

    if products_len == 1:
        markup_pagination.add(InlineKeyboardButton(text=f'{text_btn[trecked][0]}',
                                                   callback_data=f'{text_btn[trecked][1]}:{seller_id}:{trecked}:'
                                                                 f'{0}:{prod_id}')).add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data='null'),
            InlineKeyboardButton(text=f'{page_number+1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'null'))
        return markup_pagination

    elif 0 < page_number < products_len - 1:
        markup_pagination.add(InlineKeyboardButton(text=f'{text_btn[trecked][0]}',
                                                   callback_data=f'{text_btn[trecked][1]}:{seller_id}:{trecked}:'
                                                                 f'{page_number}:{prod_id}')).add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{trecked}:{page_number-1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{trecked}:{page_number+1}'))
        return markup_pagination
    elif page_number == 0:
        markup_pagination.add(InlineKeyboardButton(text=f'{text_btn[trecked][0]}',
                                                   callback_data=f'{text_btn[trecked][1]}:{seller_id}:{trecked}:'
                                                                 f'{page_number}:{prod_id}')).add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{trecked}:{products_len - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{trecked}:{page_number + 1}'))
        return markup_pagination
    elif page_number == products_len - 1:
        markup_pagination.add(InlineKeyboardButton(text=f'{text_btn[trecked][0]}',
                                                   callback_data=f'{text_btn[trecked][1]}:{seller_id}:{trecked}:'
                                                                 f'{0}:{prod_id}')).add(
            InlineKeyboardButton(text=f'⬅️⬅️⬅️', callback_data=f'track:{seller_id}:{trecked}:{page_number - 1}'),
            InlineKeyboardButton(text=f'{page_number + 1}/{products_len}', callback_data=f'null'),
            InlineKeyboardButton(text=f'➡️➡️➡️', callback_data=f'track:{seller_id}:{trecked}:{0}'))

    return markup_pagination

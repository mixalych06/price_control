from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_markup_sellers(sellers: dict):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, знчение-для срабатывания хэндлера"""
    markup_sellers = InlineKeyboardMarkup(row_width=1)
    x = []
    for key, value in sellers.items():
        x.append(InlineKeyboardButton(text=str(value), callback_data=f'moreSeller:{key}'))
    markup_sellers.add(*x)

    return markup_sellers

async def gen_seller_markup_(tracked_product, seller_id):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, знчение-для срабатывания хэндлера"""
    markup_seller = InlineKeyboardMarkup(row_width=2)
    markup_seller.add(InlineKeyboardButton(text=f'Отслеживается\n({tracked_product[0]})', callback_data=f'track:{seller_id}:1:0'),
                      InlineKeyboardButton(text=f'Не отслеживается\n({tracked_product[1]})', callback_data=f'not_track:{seller_id}:0:0'))\
        .add(InlineKeyboardButton(text=f'Удалить магазин', callback_data=f'delSel:{seller_id}'))

    return markup_seller
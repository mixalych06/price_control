import re
from aiogram import types, Dispatcher
from create_bot import ADMIN_ID
from utils.main import pars
from keyboards.kb_admin import keyboard_admin_main
from keyboards.kb_all import gen_markup_sellers, gen_seller_markup_, gen__markup_pagination
from create_bot import db

async def start_admin(message: types.Message):
    await message.reply('Привет, admin', reply_markup=keyboard_admin_main)

async def message_all(message: types.Message):
    '''Принимает ссылку или id одного или нескольких магазинов вылеляет, передаёт id парсеру'''
    url = message.text
    try:
        id_seller = re.findall(r'\d{5,6}', url)
        if id_seller:
            await message.reply(f'Продавец: {id_seller}', reply_markup=keyboard_admin_main)
            await pars(id_seller, message.chat.id)
    except IndexError:
        await message.reply(f'Не верный формат')
    except AttributeError:
        await message.reply(f'Не верный формат')

async def shows_sellers(message: types.Message):
    '''Обрабатывает кнопку магазины и товары'''
    sellers = db.bd_get_all_sellers()
    sellers = {str(id): seller for id, seller in sellers}
    await message.delete()
    if sellers:
        await message.answer(text='👇<b>Выберите продавца</b>👇', reply_markup=await gen_markup_sellers(sellers))
    else:
        await message.answer(text=f'<b>В базе данных нет ни одного продавца.</b>\n'
                                  f'Для добавления продавца отправьте одну или несколько ссылок на магазины или ID продавца.', reply_markup=keyboard_admin_main)


async def show_seller(cq: types.CallbackQuery):
    '''Обрабатывает инлайн кнопки выбора продавца'''
    inl_com = cq.data.split(':')
    name_seller = db.bd_get_seller_info(int(inl_com[1]))
    count_tracked = db.bd_get_amount_tracked_products(inl_com[1])
    await cq.message.edit_text(text=f'<b>Seller:</b> {name_seller[0]}\n'
                                    f'<b>ID_seller:</b> {name_seller[1]}\n'
                                    f'<b>Товаров в базе:</b> {sum(count_tracked)}',
                               reply_markup=await gen_seller_markup_(count_tracked, inl_com[1]))

async def pagination_product(cq: types.CallbackQuery):
    '''Обрабатывает инлайн кнопки выбора продавца'''
    inl_com = cq.data.split(':')
    page = int(inl_com[3])
    products = db.bd_get_tracked_products(inl_com[1], int(inl_com[2]))
    if len(products):
        print(products)
        await cq.message.edit_text(text=f'<b>Seller:</b> {products[page][0]}\n'
                                        f'<b>Name:</b> {products[page][2]}\n'
                                        f'<b>ID_prod:</b> {products[page][1]}\n'
                                        f'<b>Price:</b> {products[page][3]}\n'
                                        f'<b>min_price:</b> {products[page][4]}',
                                   reply_markup=await gen__markup_pagination(page, inl_com[1], int(inl_com[2]), len(products)))
    else:
        await cq.answer(text='Нет данных', cache_time=1, show_alert=True)






def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(shows_sellers, text=['Магазины и товары'])
    dp.register_message_handler(start_admin, lambda message: str(message.from_user.id) in ADMIN_ID, text=['старт', 'Старт', '/start'])
    dp.register_message_handler(message_all, lambda message: str(message.from_user.id) in ADMIN_ID)

    dp.register_callback_query_handler(show_seller, lambda x: x.data.startswith('moreSeller'))
    dp.register_callback_query_handler(pagination_product, lambda x: x.data.startswith('track'))

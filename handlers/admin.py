import re
from aiogram import types, Dispatcher
from create_bot import ADMIN_ID, bot
from utils.filters import checks_exists_admin
from utils.parsr import pars
from keyboards.kb_admin import keyboard_admin_main
from keyboards.kb_all import gen_markup_sellers, gen_seller_markup_, gen__markup_pagination
from create_bot import db

async def start_suadmin(message: types.Message):
    await message.reply('Привет, admin', reply_markup=keyboard_admin_main)

async def message_all(message: types.Message):
    '''Принимает ссылку одного, или нескольких магазинов вылеляет, передаёт id парсеру'''
    url = message.text
    print(123, url)
    if 'wildberries' in url and 'seller' in url:
        print(123, url)
        try:
            id_seller = re.findall(r'\d{5,6}', url)
            print(id_seller)
            await message.reply(text=f'Вы рередали ссылки на продавцов: {id_seller}\n'
                                 f'Дождитесь сообщения о количестве товаров каждого продавца...', reply_markup=keyboard_admin_main)
            await pars(id_seller, user_id=message.chat.id)
        except:
            pass
    else:
        await message.reply(f'Не удалось найти id продавца', reply_markup=keyboard_admin_main)


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

async def add_user_or_admin(cq: types.CallbackQuery):
    '''добавляем админа или пользователя'''
    inl_com = cq.data.split(':')
    id = cq.message.text.split(':')[1]
    name = cq.message.text.split(':')[-1]
    db.bd_adds_user(int(id), name, inl_com[1])
    await cq.answer(text=f'Пользователь {name}, id {id}\n Добавлен с правами {inl_com[1]}', show_alert=True)
    text_privilege = {'admin': 'Вы можете:</b>\n✅добавлять/удалять пользователей;\n'
                               '✅установливать и редактировать цену для отслеживания\n'
                               '✅добавлять/удалять продавцов\n'
                               '✅получать уведомления о снижении цены ниже установленной\n'
                               '✅просматривать отслеживаемые магазины и товары',
                      'user': 'Вы можете:</b>\n✅просматривать отслеживаемые магазины и товары\n'
                              '✅получать уведомления о снижении цены ниже установленной\n' }
    await bot.send_message(id, text=f'<b>Вы добавлены с правами {inl_com[1]}\n{text_privilege[inl_com[1]]}')
    await cq.message.delete()

async def shows_users(message: types.Message):
    '''Обрабатывает кнопку Администраторы'''
    sellers = db.bd_get_all_sellers()
    sellers = {str(id): seller for id, seller in sellers}
    await message.delete()





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(shows_sellers, checks_exists_admin, text=['Магазины и товары'])
    dp.register_message_handler(start_suadmin, lambda message: str(message.from_user.id) in ADMIN_ID, text=['старт', 'Старт', '/start'])
    dp.register_message_handler(message_all, checks_exists_admin)

    dp.register_callback_query_handler(show_seller, lambda x: x.data.startswith('moreSeller'))
    dp.register_callback_query_handler(pagination_product, lambda x: x.data.startswith('track'))
    dp.register_callback_query_handler(add_user_or_admin, lambda x: x.data.startswith('add_user'))

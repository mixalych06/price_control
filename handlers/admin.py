import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import ADMIN_ID, bot
from utils.filters import checks_exists_admin, checks_exists_all_users
from utils.parsr import pars
from keyboards.kb_admin import keyboard_admin_main
from keyboards.kb_all import gen_markup_sellers, gen__markup_pagination, gen_markup_del_sellers
from create_bot import db, BotFSM


async def start_suadmin(message: types.Message):
    '''Срабатывает на команду старт проверяет наличие и записывает id ADMIN  в базу'''
    if message.from_user.id not in db.bd_get_su_admins():
        db.bd_adds_user(message.from_user.id, message.from_user.first_name, index='admin')
    await message.reply('Привет, admin', reply_markup=keyboard_admin_main)


async def message_all(message: types.Message):
    '''Принимает ссылку одного, или нескольких магазинов вылеляет, передаёт id парсеру'''
    url = message.text
    if 'wildberries' in url and 'seller' in url:
        try:
            id_seller = re.findall(r'\d{5,6}', url)
            await message.answer(text=f'<b>Начало парсинга магазинов.</b>\n ID: {str(id_seller)}\n'
                                      f'<i>Дождитесь сообщения о количестве товаров каждого продавца...</i>',
                                 reply_markup=keyboard_admin_main)
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
        await message.answer(text='⬇️<b>Выбери продавца</b>⬇️',
                             reply_markup=await gen_markup_sellers(sellers, 'track'))
    else:
        await message.answer(text=f'❗️❗<b>В базе данных нет ни одного продавца.</b>\n'
                                  f'Для добавления продавца отправь одну или несколько ссылок на магазин.',
                             reply_markup=keyboard_admin_main)



async def pagination_product(cq: types.CallbackQuery):
    '''Обрабатывает инлайн кнопки выбора продавца включает пагинацию'''
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    page = int(inl_com[2])
    products = db.bd_get_tracked_products(inl_com[1])
    if len(products):
        try:
            await cq.message.edit_text(text=f'<b>Продавец:</b> {products[page][0]}\n'
                                                f'<b>Название:</b> {products[page][2]}\n'
                                                f'<b>ID_прод.:</b> {products[page][1]}\n'
                                                f'<b>Стартовая цена:</b> {products[page][3]} руб.\n'
                                                f'<b>Текущая цена:</b> {products[page][4]} руб.',
                                           reply_markup=await gen__markup_pagination(inl_com[1], len(products), page))
        except:
            print(99999)
            await bot.answer_callback_query(cq.id)

    else:
        await cq.answer(text='Нет данных', cache_time=1, show_alert=True)


async def add_user_or_admin(cq: types.CallbackQuery):
    '''добавляем админа или пользователя'''
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    id = cq.message.text.split(':')[1]
    name = cq.message.text.split(':')[-1]
    db.bd_adds_user(int(id), name, inl_com[1])
    await cq.answer(text=f'Пользователь {name}, id {id}\n Добавлен с правами {inl_com[1]}', show_alert=True)
    text_privilege = {'admin': 'Ты можешь:</b>\n✅добавлять/удалять пользователей;\n'
                               '✅добавлять/удалять продавцов\n'
                               '✅получать уведомления о снижении цены ниже установленной\n'
                               '✅просматривать отслеживаемые магазины и товары',
                      'user': 'Ты можешь:</b>\n✅просматривать отслеживаемые магазины и товары\n'
                              '✅получать уведомления о снижении цены ниже установленной\n'}
    await bot.send_message(id, text=f'<b>Вы добавлены с правами {inl_com[1]}\n{text_privilege[inl_com[1]]}')
    await cq.message.delete()


async def shows_users(message: types.Message):
    '''Обрабатывает кнопку Администраторы и пользователи'''
    if 'Администраторы' in message.text:
        admins = db.bd_get_su_admins_all()
        if admins:
            for admin in admins:
                await message.answer(text=f'<b>Администратор {admin[1]}</b>\nID: {admin[0]}',
                                     reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                         InlineKeyboardButton(text='Удалить', callback_data=f'del_admin:{admin[0]}'),
                                         InlineKeyboardButton(text='Уменьшить права', callback_data=f'change:0:1:{admin[0]}')))
        else:
            await message.answer(text=f'Нет администраторов')
    elif 'Пользователи' in message.text:
        users = db.bd_get_users_all()
        if users:
            for user in users:
                await message.answer(text=f'<b>Пользователь {user[1]}</b>\nID: {user[0]}',
                                     reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                         InlineKeyboardButton(text='Удалить', callback_data=f'del_user:{user[0]}'),
                                         InlineKeyboardButton(text='Расширить права', callback_data=f'change:1:0:{user[0]}')))
        else:
            await message.answer(text=f'Нет пользователей')
    await message.delete()


async def del_user(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    db.bd_delete_user(int(inl_com[1]))
    await cq.message.delete()


async def del_admin(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    db.bd_delete_admin(int(inl_com[1]))
    await cq.message.delete()

async def changes_access(cq: types.CallbackQuery):
    '''изменение прав доступа'''
    inl_com = cq.data.split(':')
    inl_com = list(map(int, inl_com[1:]))
    db.changes_access(inl_com)


async def del_shop_menu(message: types.Message):
    '''Вызавает список магазинов для удаления'''
    shops = db.bd_get_all_sellers()
    if shops:
        shops_dict = {id[0]: id[1] for id in shops}
        await message.answer(text=f'Для удаления, выберите магазин.\n'
                                  f'⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️', reply_markup=await gen_markup_sellers(shops_dict, 'delshop'))
    else:
        await message.answer(text=f'Нет магазинов для удаления')
    await message.delete()


async def del_shop(cq: types.CallbackQuery):
    '''вызывает функцию удаления магазина, после удаления меняет количество кнопок магазинов'''
    inl_com = cq.data.split(':')
    db.bd_delete_shop(int(inl_com[1]))
    await cq.answer(text=f'Магазин с ID: {inl_com[1]} удален.', show_alert=True)
    shops = db.bd_get_all_sellers()
    try:
        if shops:
            shops_dict = {id[0]: id[1] for id in shops}
            await cq.message.edit_reply_markup(reply_markup=await gen_markup_sellers(shops_dict, 'delshop'))
        else:
            await cq.message.delete()
    except:
        pass


async def creates_team(message: types.Message):
    '''генерирует команду для запроса добавления пользователя, для каждого
    админа генерируется своя команда'''
    team = f'requests_to_add_user:{message.from_user.id}'
    await message.answer('Для добавления, пользователь должен отправить боту команду\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️')
    await message.answer(team)
    await message.delete()


async def disable_tracking(cq: types.CallbackQuery):
    '''Прекращает отслеживать мин цену'''
    try:
        inl_com = cq.data.split(':')
        db.bd_changes_min_price(int(inl_com[4]), 0)
        product = db.bd_get_amount_tracked_products(inl_com[1])
        if product[0] == 0:
            await cq.message.delete()
        else:
            await pagination_product(cq)
    except:
        await cq.answer('Ошибка чтения из базы', show_alert=True)


async def enable_tracking(cq: types.CallbackQuery, state: FSMContext):
    '''Прекращает отслеживать мин цену'''
    await cq.message.edit_text(f'<b>Введите min цену товара.</b>\n{cq.message.text}',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(text='Отмена', callback_data='cancelFSM')))
    async with state.proxy() as data:
        data['cq'] = cq
    await BotFSM.min_price.set()


async def add_min_prise(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = message.text
        inl_com = data['cq']
        inl_com = inl_com.data.split(':')
        try:
            db.bd_changes_min_price(int(inl_com[4]), int(data['min_price']))
        except:
            await message.answer(text=f'min цена=Ошибка ввода. Попробуйте ещё раз или нажмите отмена"]')
        await message.answer(text=f'min цена={data["min_price"]} руб. установлена')
        await message.delete()
        await pagination_product(data['cq'])
        await state.finish()


async def cancelFSM(cq: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await cq.answer(text='Отменено', show_alert=True)
    await cq.message.delete()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(shows_sellers, checks_exists_all_users, text=['Магазины и товары'])
    dp.register_message_handler(shows_users, checks_exists_admin, text=['Администраторы'])
    dp.register_message_handler(shows_users, checks_exists_admin, text=['Пользователи'])
    dp.register_message_handler(creates_team, checks_exists_admin, text=['Добавить пользователя'])
    dp.register_message_handler(del_shop_menu, checks_exists_admin, text=['Удалить магазин'])
    dp.register_message_handler(start_suadmin, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text=['старт', 'Старт', '/start'])
    dp.register_message_handler(add_min_prise, content_types=['text'], state=BotFSM.min_price)
    dp.register_message_handler(message_all, checks_exists_admin)
    dp.register_callback_query_handler(pagination_product, lambda x: x.data.startswith('track'))
    dp.register_callback_query_handler(add_user_or_admin, lambda x: x.data.startswith('add_user'))
    dp.register_callback_query_handler(del_user, lambda x: x.data.startswith('del_user'))
    dp.register_callback_query_handler(del_admin, lambda x: x.data.startswith('del_admin'))
    dp.register_callback_query_handler(changes_access, lambda x: x.data.startswith('change'))
    dp.register_callback_query_handler(del_shop, lambda x: x.data.startswith('delshop'))
    dp.register_callback_query_handler(disable_tracking, lambda x: x.data.startswith('noTr'))
    dp.register_callback_query_handler(enable_tracking, lambda x: x.data.startswith('startTr'), state=None)
    dp.register_callback_query_handler(cancelFSM, lambda x: x.data.startswith('cancelFSM'), state='*')

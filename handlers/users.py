from create_bot import db, bot
from keyboards.kb_users import keyboard_user_main, gen__markup_pagination_for_user, gen_seller_markup_user
from keyboards.kb_all import gen_markup_sellers
from utils.filters import checks_exists_user
from aiogram import types, Dispatcher

async def start_user(message: types.Message):
    await message.answer(text=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                             f'Твой ID: {message.from_user.id}\n'
                             f'<b>Ты можешь:</b>\n✅просматривать отслеживаемые магазины и товары\n'
                             f'✅получать уведомления о снижении цены ниже установленной.',
                        reply_markup=keyboard_user_main)
    await message.delete()

async def shows_sellers_user(message: types.Message):
    '''Обрабатывает кнопку продавцы и товары'''
    sellers = db.bd_get_all_sellers()
    sellers = {str(id): seller for id, seller in sellers}
    await message.delete()
    if sellers:
        await message.answer(text='👇<b>Выберите продавца</b>👇', reply_markup=await gen_markup_sellers(sellers, 'u_moreSeller'))
    else:
        await message.answer(text=f'<b>В базе данных нет ни одного продавца.</b>', reply_markup=keyboard_user_main)


async def show_seller_user(cq: types.CallbackQuery):
    '''Обрабатывает инлайн кнопки выбора продавца'''
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    name_seller = db.bd_get_seller_info(int(inl_com[1]))
    count_tracked = db.bd_get_amount_tracked_products(inl_com[1])
    await cq.message.edit_text(text=f'<b>Seller:</b> {name_seller[0]}\n'
                                    f'<b>ID_seller:</b> {name_seller[1]}\n'
                                    f'<b>Товаров в базе:</b> {sum(count_tracked)}',
                               reply_markup=await gen_seller_markup_user(count_tracked, inl_com[1]))

async def pagination_product_user(cq: types.CallbackQuery):
    '''Обрабатывает инлайн кнопки выбора продавца'''
    await bot.answer_callback_query(cq.id)
    inl_com = cq.data.split(':')
    page = int(inl_com[3])
    products = db.bd_get_tracked_products(inl_com[1], int(inl_com[2]))
    if len(products):
        try:
            await cq.message.edit_text(text=f'<b>Seller:</b> {products[page][0]}\n'
                                            f'<b>Name:</b> {products[page][2]}\n'
                                            f'<b>ID_prod:</b> {products[page][1]}\n'
                                            f'<b>Price:</b> {products[page][3]}\n'
                                            f'<b>min_price:</b> {products[page][4]}',
                                       reply_markup=await gen__markup_pagination_for_user(page, inl_com[1], int(inl_com[2]), len(products)))
        except:
            pass
    else:
        await cq.answer(text='Нет данных', cache_time=1, show_alert=True)

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(shows_sellers_user, checks_exists_user, text=['Продавцы и товары'])
    dp.register_message_handler(start_user, checks_exists_user)
    dp.register_callback_query_handler(show_seller_user, lambda x: x.data.startswith('u_moreSeller'))
    dp.register_callback_query_handler(pagination_product_user, lambda x: x.data.startswith('u_track'))
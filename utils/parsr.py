import requests
from create_bot import bot, db, ADMIN_ID
from fake_useragent import UserAgent
import asyncio
import threading
from datetime import datetime




async def pars(id_sellers: list, user_id='', parsing = True):
    '''Парсер магазина, выбирает все товары и записывает в БД'''
    headers = {'User-Agent': UserAgent().chrome}
    for seller in id_sellers:
        db.bd_delete_shop(seller)
        b = requests.get(url=f'https://www.wildberries.ru/webapi/seller/data/short/{seller}',
                         headers=headers).json()
        if parsing:
            await bot.send_message(chat_id=user_id, text=f' <b>Продавец:</b> {b["name"]}, id: {b["id"]}')
        lengh = 0
        for j in range(30):
            a = requests.get(url=f'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-1257786&page={j+1}'
                                 f'&sort=popular&spp=0&supplier={seller}', headers=headers)
            if len(a.json()['data']['products']) > 0:
                lengh += len(a.json()['data']['products'])
                for i in a.json()['data']['products']:
                    db.bd_adds_products(b["id"], b["name"], i["id"], i["name"], i["salePriceU"]/100)
            else:
                if parsing:
                    await bot.send_message(chat_id=user_id, text=(f'<b>Всего товаров:</b> {lengh}'))
                break
    if not parsing:
        await bot.send_message(chat_id=user_id, text=(f'<b>База данных обновлена</b>'))


def thread_2():
    """Парсит цены.Работает отдельным потоком"""
    headers = {'User-Agent': UserAgent().chrome}
    sellers = db.bd_get_all_sellers()
    id_sellers = [id[0] for id in sellers]
    if id_sellers:
        for seller in id_sellers:
            for j in range(30):
                try:
                    a = requests.get(
                        url=f'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-1257786&page={j + 1}'
                            f'&sort=popular&spp=0&supplier={seller}', headers=headers)
                    if len(a.json()['data']['products']) > 0:
                        for product in a.json()['data']['products']:
                            #  записываем в базу текущую цену
                            db.bd_changes_current_price(product["id"], product["salePriceU"] / 100)
                    else:
                        break
                except:
                    pass

async def parsing_price(wait_for):
    """Запускает новый поток для парсинга"""
    while True:
        await asyncio.sleep(wait_for)
        parsing = threading.Thread(target=thread_2)
        parsing.start()


async def parsing_price2(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        products_for_message = db.bd_get_products_for_parsing() #все товары с низкой ценой
        if products_for_message:
            all_users = db.bd_get_all_users() #все пользователи
            for product in products_for_message:
                for user in all_users:
                    # сообщает пользователям о всех товарах со сниженной ценой. Уравнивыет значение текущей и предыдущей цены
                    try:
                        await bot.send_message(chat_id=user, text=(f'‼️‼️<b>Внимание</b>‼️‼️\n'
                                                                   f'{product[2]}\n'
                                                                   f'<b><i>"{product[4]}"</i></b>\n'
                                                                   f'ID:{product[3]}\n'
                                                                   f'Стартовая цена: {product[5]} руб.\n'
                                                                   f'Текущая цена: {product[7]} руб.\n'
                                                                   f'Меньше стартовой на '
                                                                   f'{(((product[5] - product[7])/product[5]) * 100)//1} %.'))
                    except:
                        pass
        db.bd_changes_current_price_all()

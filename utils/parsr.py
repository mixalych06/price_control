import requests
from create_bot import bot
from create_bot import db
from fake_useragent import UserAgent
import asyncio

async def pars(id_sellers: list, user_id='', parsing = True):
    '''Парсер магазина, выбирает все товары и записывает в БД'''
    headers = {'User-Agent': UserAgent().chrome}
    for seller in id_sellers:
        b = requests.get(url=f'https://www.wildberries.ru/webapi/seller/data/short/{seller}', headers=headers).json()
        if parsing:
            await bot.send_message(chat_id=user_id, text=f' <b>Продавец:</b> {b["name"]}, id: {b["id"]}')
        lengh = 0
        for j in range(50):
            a = requests.get(url=f'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-1257786&page={j+1}'
                                 f'&sort=popular&spp=0&supplier={seller}', headers=headers)
            if len(a.json()['data']['products']) > 0:
                lengh += len(a.json()['data']['products'])
                for i in a.json()['data']['products']:
                    db.bd_adds_products([b["id"], b["name"], i["id"], i["name"], i["salePriceU"]])
                    db.bd_changes_the_current_price(int(i["id"]), int(i["salePriceU"]))
            else:
                if parsing:
                    await bot.send_message(chat_id=user_id, text=(f'<b>Всего товаров:</b> {lengh}'))
                break


async def parsing_price(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        id_seller = [id[0] for id in db.bd_get_all_sellers()]
        if id_seller:
            await pars(id_seller, parsing=False)
            products_for_message = db.bd_get_products_for_parsing()
            for product in products_for_message:
                await bot.send_message(chat_id=1272037006, text=(f'Тревога\n{product}'))
                db.bd_changes_min_price(product[3], 0)
        else:
            await bot.send_message(chat_id=1272037006, text='Нет товаров для отслеживания')










#
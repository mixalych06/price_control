import requests
from create_bot import bot
from create_bot import db
from fake_useragent import UserAgent

async def pars(id_sellers: list, user_id: str):
    '''Парсер магазина, выбирает все товары и записывает в БД'''
    headers = {'User-Agent': UserAgent().chrome}
    for seller in id_sellers:
        page = 1
        b = requests.get(url=f'https://www.wildberries.ru/webapi/seller/data/short/{seller}', headers=headers).json()
        await bot.send_message(chat_id=user_id, text=f'продавец: {b["name"]}, id: {b["id"]}')
        lengh = 0
        for j in range(50):
            a = requests.get(url=f'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-1257786&page={page}&sort=popular&spp=0&supplier={seller}')
            if len(a.json()['data']['products']) > 0:
                lengh += len(a.json()['data']['products'])
                page += 1
                for i in a.json()['data']['products']:
                    db.bd_adds_products([b["id"], b["name"], i["id"], i["name"], i["salePriceU"]])
                    db.bd_changes_the_current_price(int(i["id"]), int(i["salePriceU"]))
            else:
                await bot.send_message(chat_id=user_id, text=(f'Всего товаров: {lengh}'))
                break



#pars([145641, 415033, 902995 ]468681)644763

#
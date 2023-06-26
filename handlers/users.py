import re

def message_all(message):
    url = message
    id_seller = re.findall(r'\d{5,6}', url)
    print(id_seller)

message_all('https://www.wildberries.ru/seller/46346fgjfgj, 56789, 435455 https://www.wildberries.ru/seller/415033')
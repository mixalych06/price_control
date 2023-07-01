from create_bot import dp
from utils.parsr import parsing_price

from handlers.others import register_handlers_other
from handlers.admin import register_handlers_admin
from handlers.users import register_handlers_user

from aiogram import executor
import asyncio
from time import sleep


register_handlers_admin(dp)
register_handlers_user(dp)
register_handlers_other(dp)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    loop.create_task(parsing_price(10))
    executor.start_polling(dp, skip_updates=True)


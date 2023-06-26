from create_bot import dp

from handlers.others import register_handlers_other
from handlers.admin import register_handlers_admin

from aiogram import executor


register_handlers_admin(dp)
register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

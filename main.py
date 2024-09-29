import logging
from aiogram.utils import executor
from buttons import start
from config import bot, dp, admin
from handlers import (commands, FSM_enter, FSM_order)
from db import db_main


async def on_startup(_):
    for i in admin:
        await bot.send_message(chat_id=i, text="Бот включен!",
                               reply_markup=start)
        await db_main.sql_create()


commands.register_commands(dp)
FSM_enter.register_FSM_enter(dp)
FSM_order.register_FSM_order(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
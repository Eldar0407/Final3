from aiogram import types, Dispatcher
from db import db_main
from config import bot
from buttons import start

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Hello!',
                           reply_markup=start)
async def info_handler(message: types.Message):
    await message.reply("Я бот для управления товарами и заказами. Могу принимать заказы и управлять товарами.")

async def products_handler(message: types.Message):
    db_main.cursor.execute("SELECT * FROM products")
    products = db_main.cursor.fetchall()
    for product in products:
        response =  (f"Название: {product[1]},"
                     f" Категория: {product[2]},"
                     f" Размер: {product[3]},"
                     f" Цена: {product[4]},"
                     f" Артикул: {product[5]}\n"
                     )
        await message.answer_photo(product[6])
        await message.answer(response)

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(products_handler, commands=['products'])


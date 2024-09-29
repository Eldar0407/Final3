from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import config
from buttons import sizes, submit_button
from aiogram.types import ReplyKeyboardRemove

class FSM_order(StatesGroup):
    article = State()
    size = State()
    quantity = State()
    contact = State()
    order = State()

size = ['XL','L', 'M']

async def start_order(message: types.Message):
    await FSM_order.article.set()
    await message.reply("Введите артикул товара.")

async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text


    await message.answer('Введите размер: ',reply_markup= sizes)
    await FSM_order.next()

async def load_size(message: types.Message, state: FSMContext):
    if message.text in size:
        async with state.proxy() as data:
            data['size'] = message.text

        await message.answer('Введите количество: ', reply_markup=types.ReplyKeyboardRemove())
        await FSM_order.next()
    else:
        await message.answer('Нажимайте на кнопки!')

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await message.answer('Введите контактный номер: ')
    await FSM_order.next()

async def load_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
    await message.answer('Верные ли данные ?')
    await message.answer(f'Артикул: {data["article"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Количество: {data["quantity"]}\n'
                f'Контактный номер: {data["contact"]}\n',
        reply_markup=submit_button)

    await FSM_order.next()


async def order(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:
            await message.answer('Отлично, заказ принят!', reply_markup=kb)
            order_info = (f"Артикул: {data['article']}\n"
                          f"Размер: {data['size']}\n"
                          f"Количество: {data['quantity']}\n"
                          f"Контакт: {data['contact']}")
            for user_id in config.staff:
                await config.bot.send_message(user_id, f"Новый заказ:\n{order_info}")

    await state.finish()

def register_FSM_order(dp: Dispatcher):
    dp.register_message_handler(start_order, commands=['order'])
    dp.register_message_handler(load_article, state=FSM_order.article)
    dp.register_message_handler(load_size, state=FSM_order.size)
    dp.register_message_handler(load_quantity, state=FSM_order.quantity)
    dp.register_message_handler(load_contact, state=FSM_order.contact)
    dp.register_message_handler(order, state=FSM_order.order)
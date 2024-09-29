from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import config
from buttons import sizes, submit_button
from aiogram.types import ReplyKeyboardRemove
from db import db_main

class FSM_enter(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()
    article = State()
    photo = State()
    submit = State()

size = ['XL','L', 'M']

async def start_product(message: types.Message):
    if message.from_user.id not in config.staff:
        return await message.reply("Эта команда доступна только сотрудникам.")
    await FSM_enter.name.set()
    await message.reply("Введите название продукта.")

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Введите категорию:')
    await FSM_enter.next()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Введите размер: ',reply_markup= sizes)
    await FSM_enter.next()


async def load_size(message: types.Message, state: FSMContext):
    if message.text in size:
        async with state.proxy() as data:
            data['size'] = message.text

        await message.answer('Введите цену: ')
        await FSM_enter.next()
    else:
        await message.answer('Нажимайте на кнопки!')

async def load_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['price'] = message.text

        await message.answer('Введите артикль: ')
        await FSM_enter.next()
    else:
        await message.answer('Вводите числа!')

async def load_article(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['article'] = message.text
        await message.answer('Отправьте фото: ')
        await FSM_enter.next()
    else:
        await message.answer('Вводите числа!')
async def load_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo'] = photo

    await message.answer('Верные ли данные ?')
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Название: {data["name"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Категория товара: {data["category"]}\n'
                f'Стоимость: {data["price"]}\n'
                f'Артикул: {data["article"]}\n',
        reply_markup=submit_button)

    await FSM_enter.next()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:
            await message.answer('Отлично, Данные в базе!', reply_markup=kb)
            await db_main.sql_insert_products(
                name_product=data['name'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                article=data['article'],
                photo=data['photo']
            )
            await state.finish()
    elif message.text == 'Нет':
        await message.answer('Хорошо, заполнение анкеты завершено!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer('Выберите "Да" или "Нет"')


def register_FSM_enter(dp: Dispatcher):
    dp.register_message_handler(start_product, commands=['enter_product'])
    dp.register_message_handler(load_name, state=FSM_enter.name)
    dp.register_message_handler(load_category, state=FSM_enter.category)
    dp.register_message_handler(load_price, state=FSM_enter.price)
    dp.register_message_handler(load_size, state=FSM_enter.size)
    dp.register_message_handler(load_article, state=FSM_enter.article)
    dp.register_message_handler(load_photo, state=FSM_enter.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_enter.submit)

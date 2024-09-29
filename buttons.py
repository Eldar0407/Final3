from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# ===============================================================
start = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
    ).add(
KeyboardButton('/start')
)
# ===============================================================
sizes = ReplyKeyboardMarkup(resize_keyboard=True,
                            row_width=3).add(
    KeyboardButton(text='XL'),
    KeyboardButton(text='L'),
    KeyboardButton(text='M')
)

submit_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет'))
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Занятия"), KeyboardButton(text="Тех поддержка")
        ],
    ],
    resize_keyboard=True
)
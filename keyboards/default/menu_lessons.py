from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_lessons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Справочные материалы"), KeyboardButton(text="Перейти в чат")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)
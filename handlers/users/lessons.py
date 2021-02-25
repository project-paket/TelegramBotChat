from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.default import menu_lessons, menu
from loader import dp
from utils.misc import rate_limit


@rate_limit(2, 'lessons')
@dp.message_handler(Command("lessons"))
async def show_lessons(message: types.Message):
    await message.answer("Вы перешли в раздел занятия\n"
                         "Выберите следующее действие.", reply_markup=menu_lessons)


@rate_limit(5, 'Справочные материалы')
@dp.message_handler(text="Справочные материалы")
async def show_tp(message: types.Message):
    await message.answer("Вы нажали кнопку справочные материалы\n"
                         "Чтобы продолжить нажмите {}refMaterial".format('/'))


@rate_limit(5, 'Перейти в чат')
@dp.message_handler(text="Перейти в чат")
async def show_lessons(message: types.Message):
    await message.answer("Вы нажали на кнопку перейти в чат.\n"
                         "Чтобы продолжить нажмите {}chat.".format('/'))


@dp.message_handler(text="Назад")
async def show_tp(message: types.Message):
    await message.answer('Вы вернулись в меню', reply_markup=menu)
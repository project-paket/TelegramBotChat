from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp, db
from utils.misc import rate_limit

@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=menu)
    if not await db.check_id(message.from_user.id):
        await db.add_user(id=message.from_user.id, name=message.from_user.full_name, status='default')
    else:
        print()

@rate_limit(5, 'Тех поддержка')
@dp.message_handler(text="Тех поддержка")
async def show_tp(message: types.Message):
    await message.answer("Вы нажали кнопку тех поддержка\n"
                         "Чтобы продолжить нажмите {}tp".format('/'))

@rate_limit(2, 'Занятия')
@dp.message_handler(text="Занятия")
async def show_lessons(message: types.Message):
    await message.answer("Вы нажали на кнопку занятия.\n"
                         "Чтобы продолжить нажмите {}lessons.".format('/'))

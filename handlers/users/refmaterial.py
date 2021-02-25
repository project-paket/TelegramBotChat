from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.choice_buttons import choice
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'refmaterial')
@dp.message_handler(Command("refmaterial"))
async def show_tp(message: types.Message):
    await message.answer("Вы перешли в раздел справочных материалов\n"
                         "Ниже находится список со всеми временными правилами английского языка:\n"
                         "Разбирайтесь постепенно и не спешите!",
                         reply_markup=choice)
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.default import menu
from loader import dp, bot
from states import Tp
from data.config import admins
from utils.misc import rate_limit


@rate_limit(5, 'tp')
@dp.message_handler(Command("tp"))
async def show_tp(message: types.Message):
    await message.answer("Вы перешли в раздел тех поддержки\n"
                         "Напишите, с чем у вас возникли проблемы.")
    await Tp.tp_click.set()


@dp.message_handler(state=Tp.tp_click)
async def send_message_tp(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    await bot.send_message(chat_id=admins[0], text=f"-----------------------------\n"
                                                   f"id - {message.from_user.id}\n"
                                                   f"first name - {message.from_user.first_name}\n"
                                                   f"last name - {message.from_user.last_name}\n"
                                                   f"username - {message.from_user.username}\n"
                                                   f"message:\n {answer}\n"
                                                   f"-----------------------------\n".strip())

    await message.answer('Спасибо за ваше сообщение!\b'
                         'Мы скоро всё исправим (=', reply_markup=menu)
    await state.reset_state()

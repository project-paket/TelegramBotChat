from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import menu_lessons
from loader import dp, bot, db
from states import Chat
from utils.db_api import postgresql_psc2
from utils.misc import rate_limit


async def add_chat_user(id):
    mass = []
    if postgresql_psc2.count_begin_id()[0][0] == 2:
        await bot.send_message(chat_id=id, text="Комната создана:\n"
                                                "Ожидайте собеседника\n"
                                                "Если вы хотите прекратить поиск нажмите /end",
                                                reply_markup=ReplyKeyboardRemove())

        tmp = postgresql_psc2.search_begin_id('begin')

        for i in range(len(tmp)):
            mass.append(tmp[i][0])

        for i in range(len(mass)):
            if i % 2 == 0:
                if postgresql_psc2.check_id(mass[i])[0][0] == mass[i] \
                        and postgresql_psc2.search_begin_id('begin')[i][0] == mass[i]:
                    await postgresql_psc2.add_user_chat(id=int(mass[i]))

            elif i % 2 == 1:
                if postgresql_psc2.check_id(mass[i])[0][0] == mass[i] \
                        and postgresql_psc2.search_begin_id('begin')[i][0] == mass[i] \
                        and postgresql_psc2.user_chat_update()[0][0] == 'off':
                    postgresql_psc2.update_user_chat(id_second=int(mass[i]))

        if postgresql_psc2.check_user_status()[0][0] == 'off' \
                and postgresql_psc2.check_parametrs()[0][0] != 0 \
                and postgresql_psc2.check_parametrs()[0][1] != 0 \
                and postgresql_psc2.check_parametrs()[0][2] == 'ready':
            postgresql_psc2.update_user_chat_status()

            id_first, id_second = postgresql_psc2.search_ready_id_first('ready')[0][0], \
                                  postgresql_psc2.search_ready_id_sedcond('ready')[0][0],

            await bot.send_message(chat_id=mass[0], text='Мы нашли вам собеседника!\n'
                                                         'Можете начинать практиковаться!\n'
                                                         'Если вы хотите прекратить общение нажмите /end')
            await bot.send_message(chat_id=mass[1], text='Мы нашли вам собеседника!\n'
                                                         'Можете начинать практиковаться!\n'
                                                         'Если вы хотите прекратить общение нажмите /end')

            await Chat.get_id.set()

            await db.update_status('default', id_first)
            await db.update_status('default', id_second)
    else:
        await bot.send_message(chat_id=id, text="Комната создана:\n"
                                                "Ожидайте собеседника\n"
                                                "Если вы хотите прекратить поиска нажмите /end",
                                                reply_markup=ReplyKeyboardRemove())
        await Chat.get_id.set()


@rate_limit(5, 'chat')
@dp.message_handler(Command("chat"))
async def show_chat(message: types.Message):
    await message.answer("Вы перешли в раздел чат.\n"
                         "Чтобы начать поиск собеседника нажмите {}begin.\n".format("/") +
                         "Чтобы остановить поиск собеседника нажмите {}end".format("/"),
                         reply_markup=ReplyKeyboardRemove())


@rate_limit(5, 'chat')
@dp.message_handler(Command("begin"))
async def show_chat(message: types.Message):
    id = message.from_user.id

    await db.update_status('begin', id)
    await add_chat_user(id)


@dp.message_handler(state=Chat.get_id)
async def get_ready(message: types.Message, state: FSMContext):
    mass_1, mass_2 = [], []
    id_first, id_second = postgresql_psc2.search_ready_id_first('ready'), \
                          postgresql_psc2.search_ready_id_sedcond('ready')

    for i in range(len(id_first)):
        mass_1.append(id_first[i][0])

    for i in range(len(id_second)):
        mass_2.append(id_second[i][0])

    if message.from_user.id and message.text != '/end':

        for i in range(len(mass_1)):

            if mass_1[i] == message.from_user.id and message.text != '/end':
                await bot.send_message(chat_id=mass_2[i], text=message.text)

            elif mass_2[i] == message.from_user.id and message.text != '/end':
                await bot.send_message(chat_id=mass_1[i], text=message.text)


    elif message.text == '/end':

        for i in range(len(mass_1)):

            if mass_1[i] == message.from_user.id:

                await bot.send_message(chat_id=mass_1[i], text='Чат был завершён')
                await bot.send_message(chat_id=mass_2[i], text='Чат был завершён:\n'
                                                               'Нажмите /end, чтобы выйти из пустой комнаты.')
                postgresql_psc2.delete_ready(mass_1[i], mass_2[i])
                await state.finish()

            elif mass_2[i] == message.from_user.id:
                await bot.send_message(chat_id=mass_2[i], text='Чат был завершён')
                await bot.send_message(chat_id=mass_1[i], text='Чат был завершён:\n'
                                                               'Нажмите /end, чтобы выйти из пустой комнаты.')
                postgresql_psc2.delete_ready(mass_1[i], mass_2[i])
                await state.finish()

        else:
            await message.answer(text='Вы успешно вышли из комнаты.', reply_markup=menu_lessons)
            await state.finish()

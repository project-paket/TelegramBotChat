from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("tp", "Техническая поддержка"),
        types.BotCommand("lessons", "Занятия"),
        types.BotCommand("refmaterial", "Справочный материал по языку"),
        types.BotCommand("chat", "Переход в чат"),

    ])

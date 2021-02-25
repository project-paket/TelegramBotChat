from loader import db
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await db.create_table_users()
    await db.create_table_users_chat()
    await db.delete_users()
    await db.delete_user_chat()
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

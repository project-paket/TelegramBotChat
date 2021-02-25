import asyncio

import asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                dsn=config.PG_DSN,
                user=config.PG_USER,
                password=config.PG_PASSWORD,
                host=config.ip
            )
        )

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        status VARCHAR (255) NOT NULL,
        PRIMARY KEY (id))
        """
        await self.pool.execute(sql)

    async def create_table_users_chat(self):
        sql = """
        CREATE TABLE IF NOT EXISTS User_chat (
        id_first INT DEFAULT 0,
        id_second INT DEFAULT 0,
        text VARCHAR (255) DEFAULT 0,
        status VARCHAR (3) DEFAULT 'off')
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parametrs: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parametrs, start=1)
        ])
        return sql, tuple(parametrs.values())

    async def add_user(self, id: int, name: str, status: str):
        sql = "INSERT INTO Users (id, name, status) VALUES ($1, $2, $3)"
        await self.pool.execute(sql, id, name, status)

    async def check_id(self, id):
        sql = "SELECT id FROM Users WHERE id={}".format(id)
        return await self.pool.fetchrow(sql)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE True")

    async def delete_user_chat(self):
        await self.pool.execute("DELETE FROM User_chat WHERE True")

    async def update_status(self, status, id):
        sql = "UPDATE Users SET status = $1 WHERE id = $2"
        return await self.pool.execute(sql, status, id)
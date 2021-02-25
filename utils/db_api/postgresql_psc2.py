import psycopg2
from psycopg2 import sql

from data import config


def connect():
    con = psycopg2.connect(dbname=config.PG_DBNAME, user=config.PG_USER,
                            password=config.PG_PASSWORD, host=config.ip)
    con.autocommit = True
    return con


def check_id(id: int):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT id FROM Users WHERE id='{}'".format(id))

        cursor.execute(stmt)
        return cursor.fetchall()


def update_status(status, id):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("UPDATE Users SET status ='{}' WHERE id ='{}'".format(status, id))

        cursor.execute(stmt)
    return cursor.fetchall()


def update_user_chat(id_second):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("UPDATE User_chat SET id_second ='{}', text='ready' WHERE status='off'".format(id_second))

        cursor.execute(stmt)


def update_user_chat_status():
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("UPDATE User_chat SET status ='on' WHERE id_first IS NOT NULL AND id_second IS NOT NULL ")
        cursor.execute(stmt)


def search_begin_id(status):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT id FROM users WHERE status='{}'".format(status))

        cursor.execute(stmt)
        return cursor.fetchall()


def count_begin_id():
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT count(id) FROM users WHERE status='begin'")

        cursor.execute(stmt)
        return cursor.fetchall()


async def add_user_chat(id: int):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("INSERT INTO User_chat (id_first) VALUES ({})".format(id))
        cursor.execute(stmt)


def search_ready_id_first(text: str):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT id_first FROM User_chat WHERE text='{}'".format(text))

        cursor.execute(stmt)
        return cursor.fetchall()


def search_ready_id_sedcond(text: str):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT id_second FROM User_chat WHERE text='{}'".format(text))

        cursor.execute(stmt)
        return cursor.fetchall()


def delete_ready(id_first, id_second):
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("DELETE FROM User_chat WHERE id_first='{}' AND id_second='{}'".format(
            id_first, id_second))

        cursor.execute(stmt)


def user_chat_update():
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT status FROM user_chat WHERE id_second=0")

        cursor.execute(stmt)
        return cursor.fetchall()


def check_user_status():
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT status FROM user_chat WHERE status='off'")

        cursor.execute(stmt)
        return cursor.fetchall()


def check_parametrs():
    conn = connect()
    with conn.cursor() as cursor:
        stmt = sql.SQL("SELECT id_first, id_second, text FROM user_chat WHERE status='off'")

        cursor.execute(stmt)
        return cursor.fetchall()
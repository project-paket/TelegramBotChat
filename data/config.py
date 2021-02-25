import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PG_USER = str(os.getenv("PG_USER"))
PG_PASSWORD = str(os.getenv("PG_PASSWORD"))
PG_DSN = str(os.getenv("PG_DSN"))
PG_DBNAME = str(os.getenv("PG_DBNAME"))
admins = [
    978531111
]

ip = os.getenv("ip")

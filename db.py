import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

credenciales = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

class DataBase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(**credenciales, autocommit=True)
        self.cursor = self.conn.cursor()

    async def disconnect(self):
        await self.cursor.close()
        await self.conn.close()

db = DataBase()
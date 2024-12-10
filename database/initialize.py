import sqlite3
from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SQLITE_DB_PATH = getenv('SQLITE_DB_PATH')

def init_db():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    except sqlite3.Error as e:
        print(f'Error creating users table: {e}')
    finally:
        connection.commit()
        connection.close()
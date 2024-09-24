import sqlite3
import os
from dotenv import load_dotenv

load_dotenv('../.env')
DB_CONN = os.getenv('DB_CONN')
print(f"db connected -> {DB_CONN}")
db_file = DB_CONN.replace('sqlite:///', '')
print(f"db file -> {db_file}")
full_db_path = os.path.abspath(os.path.join("..", db_file))
print(f"db fullpath -> {full_db_path}")
conn = sqlite3.connect(full_db_path)
cur = conn.cursor()

# CREATE TABLEs
cur.execute('''
    CREATE TABLE IF NOT EXISTS chatbot (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        botname TEXT NOT NULL,
        display_name TEXT NOT NULL,
        useful_when TEXT NOT NULL,
        description TEXT,
        enable_version JSON,
        module_filename TEXT,
        classname TEXT
    );
''')

# chat_statusのENUMをTEXT型で代替
cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL,
        status TEXT CHECK(status IN ('waiting', 'in_progress', 'failed', 'completed')) NOT NULL,
        title TEXT,
        summary TEXT, 
        message_version TEXT NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_message_list (
        history_id TEXT NOT NULL,
        message_id TEXT NOT NULL,
        time TIMESTAMP,
        PRIMARY KEY (history_id, message_id)
    );
''')

# chat_typeのENUMをTEXT型で代替
cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_message (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL,
        time TIMESTAMP NOT NULL,
        sender_type TEXT CHECK(sender_type IN ('human', 'user_meta', 'chatbot', 'bots_meta')) NOT NULL,
        botname TEXT NOT NULL,
        agent TEXT,
        content TEXT,
        message_version TEXT NOT NULL
    );
''')

conn.commit()
conn.close()
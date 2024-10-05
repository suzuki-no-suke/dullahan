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

# ALTER TABLE
cur.execute('''
    ALTER TABLE chat_history ADD COLUMN created_at TIMESTAMP;
    ALTER TABLE chat_history ADD COLUMN updated_at TIMESTAMP;
''')

cur.execute('''
    UPDATE chat_history
    SET updated_at = COALESCE(
        (SELECT MAX(time)
        FROM chat_message_list
        WHERE chat_message_list.message_id = chat_history.id),
        '2024-10-01 00:00:00'
    );
''')

cur.execute('''
    UPDATE chat_history
    SET created_at = COALESCE(
        (SELECT MIN(time)
        FROM chat_message_list
        WHERE chat_message_list.message_id = chat_history.id),
        '2024-10-01 00:00:00'
    );
''')

conn.commit()
conn.close()
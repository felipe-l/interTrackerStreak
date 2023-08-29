import sqlite3

conn = sqlite3.connect("my_database.db")

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS game_data (
    id INTEGER PRIMARY KEY,
    player TEXT,
    win_streak INTEGER,
    loss_streak INTEGER,
    win INTEGER
)
'''

cursor.execute(create_table_query)
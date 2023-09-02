import sqlite3
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the database file
db_path = os.path.join(script_dir, 'my_database.db')

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

def createTable():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS player_data (
        id INTEGER PRIMARY KEY,
        summoner TEXT,
        win_streak TEXT,
        streak_count INTEGER,
        last_game_id TEXT,
        posted TEXT
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()

# Select user data by Discord ID
def selectUserData(summoner):
    cursor.execute('SELECT * FROM player_data WHERE summoner = ?', (summoner,))
    return cursor.fetchone()


def updateUserStreak(summoner, win_streak, streak_count, last_game_id, posted):
    cursor.execute('''
        UPDATE player_data
        SET win_streak = ?, streak_count = ?, last_game_id = ?, posted = ?
        WHERE summoner = ?
    ''', (win_streak, streak_count, last_game_id, posted, summoner))
    conn.commit()


# Insert a new user's data
def insertUserData(summoner, win_streak, streak_count, last_game_id, posted):
    cursor.execute('''
        INSERT OR REPLACE INTO player_data (summoner, win_streak, streak_count, last_game_id, posted)
        VALUES (?, ?, ?, ?, ?)
    ''', (summoner, win_streak, streak_count, last_game_id, posted))
    conn.commit()

def getNewStreakData(streakNum):
    cursor.execute('''
        SELECT * FROM player_data
        WHERE posted = 'false' AND streak_count = ?
    ''', (streakNum,))
    conn.commit()


# Select all user data
def selectAllUserData():
    cursor.execute('SELECT * FROM player_data')
    return cursor.fetchall()


# Close the database connection
def closeConnection():
    conn.close()

def initialize_database():
    createTable()

initialize_database()

import sqlite3
from sqlite3 import Error


def init_db():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
def add_move(move):
    clear()
    init_db()
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("insert into GAME values (?, ?, ?, ?, ?, ?)", move)
        conn.commit()
        print("move added to db")
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def getMove():

    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("select * from GAME")
        result = cur.fetchall()
        # print(result)
        # print(result[0])
        return result[0]

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()
def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

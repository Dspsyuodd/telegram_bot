import sqlite3
import secret


def init_db():
    conn = sqlite3.connect(secret.db_connection_string)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        feedback_message TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY,
        room_number TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        room_id INTEGER,
        request_string TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    )
    ''')

    conn.commit()
    conn.close()


def add_review(username, feedback_message):
    conn = sqlite3.connect(secret.db_connection_string)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (username, feedback_message) VALUES (?, ?)', (username, feedback_message))
    conn.commit()
    conn.close()


def __get_room_id(room_number):
    conn = sqlite3.connect(secret.db_connection_string)
    cursor = conn.cursor()
    cursor.execute('SELECT room_id FROM rooms WHERE room_number = ?', (room_number,))
    room = cursor.fetchone()
    conn.close()
    return room[0] if room else None


def create_room(room_number):
    conn = sqlite3.connect(secret.db_connection_string)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rooms (room_number) VALUES (?)', (room_number,))
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return room_id


def add_order(username, room_number, request_string):
    room_id = __get_room_id(room_number)
    if room_id is None:
        room_id = create_room(room_number)

    conn = sqlite3.connect(secret.db_connection_string)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (username, room_id, request_string) VALUES (?, ?, ?)',
                   (username, room_id, request_string))
    conn.commit()
    conn.close()
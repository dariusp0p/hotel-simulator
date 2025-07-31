import sqlite3



def create_hotel_model(connection):
    cursor = connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS floors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_id TEXT UNIQUE NOT NULL,
            element_type TEXT,
            floor_id INTEGER,
            capacity INTEGER,
            x INTEGER,
            y INTEGER,
            FOREIGN KEY (floor_id) REFERENCES floors(id)
        );
    """)
    connection.commit()



def get_all_floors(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * from floors
        """)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def get_floor_id(connection, floor_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id FROM floors WHERE name = ?
        """, (floor_name,))
        return cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        raise e

def get_elements_by_floor_id(connection, floor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM elements WHERE floor_id=?
        """, (floor_id,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def add_floor(connection, floor_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO floors (name) VALUES (?)
        """, (floor_name,))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def get_floor_by_name(connection, floor_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM floors WHERE name=?
        """, (floor_name,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def add_element(connection, element_id, element_type, floor_id, capacity, x, y):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO elements (element_id, element_type, floor_id, capacity, x, y) VALUES (?, ?, ?, ?, ?, ?)            
        """, (element_id, element_type, floor_id, capacity, x, y))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def get_element_by_element_id(connection, element_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM elements WHERE element_id=?
        """, (element_id,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def get_rooms_by_capacity(connection, capacity):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM elements WHERE element_type = 'room' AND capacity >= ?
        """, (capacity,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

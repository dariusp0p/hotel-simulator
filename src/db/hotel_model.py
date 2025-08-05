import sqlite3


def create_hotel_model(connection):
    cursor = connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS floors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            level INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_type TEXT NOT NULL,
            floor_id INTEGER NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            number TEXT,
            capacity INTEGER,
            price_per_night INTEGER,
            FOREIGN KEY (floor_id) REFERENCES floors(id)
        );
        
        CREATE TABLE IF NOT EXISTS connections (
            element_id_1 INTEGER NOT NULL,
            element_id_2 INTEGER NOT NULL,
            PRIMARY KEY (element_id_1, element_id_2),
            FOREIGN KEY (element_id_1) REFERENCES floor_elements(id),
            FOREIGN KEY (element_id_2) REFERENCES floor_elements(id)
        );
    """)
    connection.commit()



# Floors Table
def select_all_floors(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * from floors
        """)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e


def insert_floor(connection, name, level):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO floors (name, level) VALUES (?, ?)
        """, (name, level))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def update_floor_name(connection, floor_id, new_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE floors SET name = ? WHERE id = ?
        """, (new_name, floor_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def update_floor_level(connection, floor_id, new_level):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE floors SET level = ? WHERE id = ?
        """, (new_level, floor_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def delete_floor(connection, floor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM floors WHERE id = ?
        """, (floor_id,))
        connection.commit()
    except sqlite3.OperationalError as e:
        raise e



# Elements
def select_elements_by_floor_id(connection, floor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM elements WHERE floor_id=?
        """, (floor_id,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e


def insert_element(connection, type, floor_id, x, y, number, capacity, price_per_night):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO elements (type, floor_id, x, y, number, capacity, price_per_night) VALUES (?, ?, ?, ?, ?, ?, ?)            
        """, (type, floor_id, x, y, number, capacity, price_per_night))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def update_element_position(connection, element_id, new_x, new_y):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE elements SET x = ?, y = ? WHERE id = ?
        """, (new_x, new_y, element_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def update_element_capacity(connection, element_id, new_capacity):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE elements SET capacity = ? WHERE id = ?
        """, (new_capacity, element_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def delete_element(connection, element_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM elements WHERE id = ?
        """, (element_id,))
        connection.commit()
    except sqlite3.OperationalError as e:
        raise e



# Connections
def select_all_connections(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM connections
        """)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def insert_connection(connection, element_id_1, element_id_2):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO connections (element_id_1, element_id_2) VALUES (?, ?)
            """, (element_id_1, element_id_2))
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def delete_connection(connection, element_id_1, element_id_2):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM connections WHERE element_id_1 = ? AND element_id_2 = ?
            """, (element_id_1, element_id_2))
        connection.commit()
    except sqlite3.OperationalError as e:
        raise e

def delete_all_connections_by_element_id(connection, element_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM connections WHERE element_id_1 = ? OR element_id_2 = ?
        """, (element_id, element_id))
        connection.commit()
    except sqlite3.OperationalError as e:
        raise e

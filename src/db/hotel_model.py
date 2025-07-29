import sqlite3



def create_hotel_model(connection):
    cursor = connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS floors (
            name TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS elements (
            element_id TEXT PRIMARY KEY,
            element_type TEXT,
            floor_name TEXT,
            capacity INTEGER,
            x INTEGER,
            y INTEGER,
            FOREIGN KEY (floor_name) REFERENCES floors(name)
        );

        CREATE TABLE IF NOT EXISTS connections (
            id1 TEXT,
            id2 TEXT,
            PRIMARY KEY (id1, id2),
            FOREIGN KEY (id1) REFERENCES elements(element_id),
            FOREIGN KEY (id2) REFERENCES elements(element_id)
        )
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

def get_elements_from_floor(connection, floor_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM elements WHERE floor_name=?
        """, (floor_name,))
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e



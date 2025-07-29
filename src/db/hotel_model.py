import sqlite3



def create_hotel_model(connection):
    cursor = connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS floors (
            name TEXT PRIMARY KEY,
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
        );
    """)
    connection.commit()

def save_hotel(connection, hotel: Hotel):
    cursor = connection.cursor()
    cursor.execute("INSERT OR REPLACE INTO hotels (name) VALUES (?)", (hotel.name,))

    for floor_id, floor in hotel.floors.items():
        cursor.execute("INSERT OR REPLACE INTO floors (id, hotel_name) VALUES (?, ?)", (floor_id, hotel.name))
        for element in floor.elements.values():
            x, y = element.position
            cursor.execute("""
                INSERT OR REPLACE INTO elements (id, type, floor_id, hotel_name, x, y, capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (element.id, element.element_type, floor_id, hotel.name, x, y, getattr(element, "capacity", None)))

            for conn_id in element.connections:
                id1, id2 = sorted([element.id, conn_id])
                cursor.execute("INSERT OR IGNORE INTO connections (id1, id2) VALUES (?, ?)", (id1, id2))

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



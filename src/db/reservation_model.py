from .db_connection import get_connection
import sqlite3



def create_reservation_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                reservation_id TEXT UNIQUE NOT NULL, 
                room_number TEXT NOT NULL, 
                guest_name TEXT NOT NULL, 
                number_of_guests INTEGER NOT NULL, 
                check_in_date TEXT NOT NULL, 
                check_out_date TEXT NOT NULL
            )
        """)
        conn.commit()


def add_reservation(connection, reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO reservations (reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date) VALUES (?, ?, ?, ?, ?, ?)
        """, (reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def get_all_reservations(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * from reservations
        """)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def get_reservation_by_reservation_id(connection, reservation_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM reservations WHERE reservation_id = ?
        """, (reservation_id,))
        return cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise e

def update_reservation(connection, db_id, reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE reservations
            SET reservation_id = ?, room_number = ?, guest_name = ?, number_of_guests = ?, check_in_date = ?, check_out_date = ?
            WHERE id = ?
            """, (reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date, db_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def delete_reservation(connection, db_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM reservations WHERE id = ?
        """, (db_id,))
        connection.commit()
    except sqlite3.OperationalError as e:
        raise e
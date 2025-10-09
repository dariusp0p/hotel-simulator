"""
Database Operations for Hotel Simulator
This module provides functions to create and manipulate the database schema of the hotel simulator application.
"""

import sqlite3


# Create Tables
def create_hotel_simulator_model(connection):
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
            price_per_night REAL,
            FOREIGN KEY (floor_id) REFERENCES floors(id)
        );
            
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            reservation_id TEXT UNIQUE NOT NULL, 
            room_id INTEGER NOT NULL, 
            guest_name TEXT NOT NULL, 
            number_of_guests INTEGER NOT NULL, 
            check_in_date TEXT NOT NULL, 
            check_out_date TEXT NOT NULL
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


# Elements Table
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
            INSERT INTO elements (element_type, floor_id, x, y, number, capacity, price_per_night) VALUES (?, ?, ?, ?, ?, ?, ?)            
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

def update_element(connection, element_id, new_number, new_capacity, new_price_per_night):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE elements SET number = ?, capacity = ?, price_per_night = ? WHERE id = ?
        """, (new_number, new_capacity, new_price_per_night, element_id))
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


# Reservations Table
def select_all_reservations(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * from reservations
        """)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise e

def select_reservation_by_reservation_id(connection, reservation_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM reservations WHERE reservation_id = ?
        """, (reservation_id,))
        return cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise e

def insert_reservation(connection, reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO reservations (reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date) VALUES (?, ?, ?, ?, ?, ?)
        """, (reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.OperationalError as e:
        raise e

def update_reservation(connection, db_id, reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE reservations
            SET reservation_id = ?, room_id = ?, guest_name = ?, number_of_guests = ?, check_in_date = ?, check_out_date = ?
            WHERE id = ?
            """, (reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date, db_id))
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

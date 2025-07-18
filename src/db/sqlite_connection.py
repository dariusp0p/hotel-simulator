import sqlite3



def get_sqlite_connection(db_path: str):
    return sqlite3.connect(db_path)

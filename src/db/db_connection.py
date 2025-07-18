from src.db.sqlite_connection import get_sqlite_connection



def get_connection(db_path):
    return get_sqlite_connection(db_path)
